""" Module for loading parsed data from bitcointalk into PostgreSQL. """
import bitcointalk
import codecs
from datetime import datetime
import os
import pg

memo = {
    'boards': set(),
    'members': set(),
    'topics': set()
}


def _insertBoardPage(data):
    """Insert just the board."""
    del data['topic_ids']
    pg.insertBoard(data)


def _insertTopicPage(data):
    """Insert data as topic and messages and splice off messages."""
    pg.insertMessages(data.pop('messages'))
    pg.insertTopic(data)

entityFunctions = {
    'board': {
        'requestor': bitcointalk.requestBoardPage,
        'parser': bitcointalk.parseBoardPage,
        'inserter': _insertBoardPage,
        'selector': pg.selectBoard
    },
    'member': {
        'requestor': bitcointalk.requestProfile,
        'parser': bitcointalk.parseProfile,
        'inserter': pg.insertMember,
        'selector': pg.selectMember
    },
    'topic': {
        'requestor': bitcointalk.requestTopicPage,
        'parser': bitcointalk.parseTopicPage,
        'inserter': _insertTopicPage,
        'selector': pg.selectTopic
    }
}


def _saveToFile(html, fileType, fileDescriptor):
    """Save given entity to a file."""
    f = codecs.open("{0}/data/{1}_{2}_{3}.html".format(
        os.path.dirname(os.path.abspath(__file__)),
        fileType, fileDescriptor,
        int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())),
        'w', 'utf-8')
    f.write(html)
    f.close()


def remember():
    """Remember what's already in the database to avoid re-scraping."""
    global memo
    cursor = pg.cursor()
    for key in memo.keys():
        cursor.execute("SELECT sid FROM {0}".format(pg.tables[key[:-1]]))
        rows = cursor.fetchall()
        for row in rows:
            memo[key].add(row[0])
    return True


def _scrape(entity, entityId):
    global memo
    global entityFunctions
    entityPlural = "{0}s".format(entity)
    if entityId in memo[entityPlural]:
        return entityFunctions[entity]['selector'](entityId)
    else:
        html = entityFunctions[entity]['requestor'](entityId)
        _saveToFile(html, entity, entityId)
        datum = entityFunctions[entity]['parser'](html)
        entityFunctions[entity]['inserter'](datum)
        memo[entityPlural].add(entityId)
        return datum


def scrapeBoard(boardId):
    """Scrape information on the specified board."""
    return _scrape('board', boardId)


def scrapeTopicIds(boardId, pageNum):
    """Scrape topic IDs from a board page. Will not store values."""
    offset = (pageNum-1)*40
    html = bitcointalk.requestBoardPage(boardId, offset)
    _saveToFile(html, "boardpage", "{0}.{1}".format(boardId, offset))
    data = bitcointalk.parseBoardPage(html)
    data = data['topic_ids']
    return data


def scrapeMember(memberId):
    """Scrape the profile of the specified member."""
    return _scrape('member', memberId)


def scrapeMessages(topicId, pageNum):
    """Scrape all messages on the specified topic, page combination."""
    """CAVEAT: Messages are not memoized."""
    offset = (pageNum-1)*20
    html = bitcointalk.requestTopicPage(topicId, offset)
    _saveToFile(html, "topicpage", "{0}.{1}".format(topicId, offset))
    data = bitcointalk.parseTopicPage(html)
    data = data['messages']
    pg.insertMessages(data)
    return data


def scrapeTopic(topicId):
    """Scrape information on the specified topic."""
    return _scrape('topic', topicId)
