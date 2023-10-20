import unittest
from bitcointalk import *

class TestBitcointalk(unittest.TestCase):

    """"Testing suite for bitcointalk module."""

    def testRequestBoardPage(self):
        """Method for testing requestBoardPate."""
        html = requestBoardPage(74)
        f = codecs.open("{0}/data/test_dummy_board_2.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'w', 'utf-8')
        f.write(html)
        f.close()
        title = lxml.html.fromstring(html).cssselect("title")[0].text
        errorMsg = "Got unexpected output for webpage title: {0}".format(title)
        self.assertEqual(title, "Legal", errorMsg)

        html = requestBoardPage(5, 600)
        f = codecs.open("{0}/data/test_dummy_board_1.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'w', 'utf-8')
        f.write(html)
        f.close()

    def testRequestProfile(self):
        """Method for testing requestProfile."""
        html = requestProfile(12)
        f = codecs.open("{0}/data/test_dummy_profile.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'w', 'utf-8')
        f.write(html)
        f.close()
        title = lxml.html.fromstring(html).cssselect("title")[0].text
        errorMsg = "Got unexpected output for webpage title: {0}".format(title)
        self.assertEqual(title, "View the profile of nanaimogold", errorMsg)

    def testRequestTopicPage(self):
        """Method for testing requestTopicPage."""
        html = requestTopicPage(14)
        f = codecs.open("{0}/data/test_dummy_topic.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'w', 'utf-8')
        f.write(html)
        f.close()
        title = lxml.html.fromstring(html).cssselect("title")[0].text
        errorMsg = "Got unexpected output for webpage title: {0}".format(title)
        self.assertEqual(title, "Break on the supply's increase", errorMsg)

        html = requestTopicPage(602041, 12400)
        f = codecs.open("{0}/data/test_dummy_topic_2.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'w', 'utf-8')
        f.write(html)
        f.close()

    def testParseBoardPage(self):
        """Method for testing parseBoardPage."""
        f = codecs.open("{0}/dummy/dummy_board_2.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        data = parseBoardPage(html)
        topicIds = data.pop("topic_ids")
        expectedData = {
            'id': 74,
            'name': 'Legal',
            'container': 'Bitcoin',
            'parent': 1,
            'num_pages': 23,
        }
        self.assertEqual(data, expectedData)
        self.assertEqual(len(topicIds), 40)
        self.assertEqual(topicIds[0], 96118)
        self.assertEqual(topicIds[-1], 684343)

        f = codecs.open("{0}/dummy/dummy_board_1.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        data = parseBoardPage(html)
        topicIds = data.pop("topic_ids")
        expectedData = {
            'id': 5,
            'name': 'Marketplace',
            'container': 'Economy',
            'parent': None,
            'num_pages': 128,
        }
        self.assertEqual(data, expectedData)
        self.assertEqual(len(topicIds), 40)
        self.assertEqual(topicIds[0], 423880)
        self.assertEqual(topicIds[-1], 430401)

    def testParseProfile(self):
        """Method for testing parseProfile."""
        f = codecs.open("{0}/dummy/dummy_profile.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        todaysDate = date(2014, 7, 29)
        data = parseProfile(html, todaysDate)
        expectedData = {
            'id': 12,
            'name': 'nanaimogold',
            'position': 'Sr. Member',
            'date_registered': datetime(2009, 12, 9, 19, 23, 55),
            'last_active': datetime(2014, 7, 29, 0, 38, 1),
            'email': 'hidden',
            'website_name': 'Nanaimo Gold Digital Currency Exchange',
            'website_link': 'https://www.nanaimogold.com/',
            'bitcoin_address': None,
            'other_contact_info': None,
            'signature': '<a href="https://www.nanaimogold.com/" ' +
            'target="_blank">https://www.nanaimogold.com/</a> ' +
            '- World\'s first bitcoin exchange service'
        }
        self.assertEqual(data, expectedData)

    def testParseTopicPage(self):
        """Method for testing parseTopicPage."""
        f = codecs.open("{0}/dummy/dummy_topic.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        data = parseTopicPage(html)
        messages = data['messages']
        del data['messages']
        expectedData = {
            'id': 14,
            'name': 'Break on the supply\'s increase',
            'board': 7,
            'count_read': 3051,
            'num_pages': 1
        }
        self.assertEqual(data, expectedData)

        self.assertEqual(len(messages), 2)

        firstMessage = messages[0]
        firstMessageContent = {
            'raw': firstMessage['content'],
            'no_html': firstMessage['content_no_html'],
            'no_quote': firstMessage['content_no_quote'],
            'no_quote_no_html': firstMessage['content_no_quote_no_html']
        }
        del firstMessage['content']
        del firstMessage['content_no_html']
        del firstMessage['content_no_quote']
        del firstMessage['content_no_quote_no_html']

        expectedFirstMessage = {
            'id': 53,
            'member': 16,
            'subject': 'Break on the supply\'s increase',
            'link': 'https://bitcointalk.org/index.php?topic=14.msg53#msg53',
            'topic': 14,
            'topic_position': 1,
            'post_time': datetime(2009, 12, 12, 14, 11, 37)
        }
        self.assertEqual(firstMessage, expectedFirstMessage)

        self.assertEqual(len(firstMessageContent['raw']), 1276)
        self.assertEqual(len(firstMessageContent['no_html']), 1208)
        self.assertEqual(len(firstMessageContent['no_quote']), 1276)
        self.assertEqual(len(firstMessageContent['no_quote_no_html']), 1208)

        f = codecs.open("{0}/dummy/dummy_topic_2.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        data = parseTopicPage(html)
        self.assertEqual(data['num_pages'], 621)
        self.assertEqual(
            data['messages'][0]['post_time'],
            datetime.combine(datetime.utcnow().date(), tm(21, 3, 11)))
        # print "Content of Message 1"
        # print data['messages'][0]['content']
        # print "Content of Message 1, No HTML"
        # print data['messages'][0]['content_no_html']
        # print "Content of Message 1, No Quote"
        # print data['messages'][0]['content_no_quote']
        # print "Content of Message 1, No Quote, No HTML"
        # print data['messages'][0]['content_no_quote_no_html']

if __name__ == "__main__":
    unittest.main()
