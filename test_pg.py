import unittest
from datetime import date
import bitcointalk
import codecs
import os
from pg import *


class TestPg(unittest.TestCase):

    """"Testing suite for pg module."""

    def setUp(self):
        """Setup tables for test."""
        # Swap and sub configuration variables
        global tables
        self.tablesOriginal = tables
        tables = {}
        for key, table in self.tablesOriginal.items():
            tables[key] = "{0}_test".format(table)

        # Create test tables
        cur = cursor()
        for key, table in tables.items():
            cur.execute("""CREATE TABLE IF NOT EXISTS
                {0} (LIKE {1} INCLUDING ALL)""".format(
                table, self.tablesOriginal[key]))
        cur.execute("""COMMIT""")

    def tearDown(self):
        """Teardown tables for test."""
        # Drop test tables
        global tables
        cur = cursor()
        for table in tables.values():
            cur.execute("""DROP TABLE IF EXISTS
                {0}""".format(table))
        cur.execute("""COMMIT""")

        # Undo swap / sub
        tables = self.tablesOriginal

    def testBoard(self):
        """Test insert and select board functions."""
        f = codecs.open("{0}/dummy/dummy_board_2.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        datum = bitcointalk.parseBoardPage(html)
        del datum["topic_ids"]
        insertBoard(datum)
        # Make sure a second insert doesn't cause problems
        insertBoard(datum)
        selectDatum = selectBoard(74)
        self.assertEqual(datum, selectDatum)

    def testMember(self):
        """Test insert and select member functions."""
        f = codecs.open("{0}/dummy/dummy_profile.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        todaysDate = date(2014, 7, 29)
        datum = bitcointalk.parseProfile(html, todaysDate)
        insertMember(datum)
        # Make sure a second insert doesn't cause problems
        insertMember(datum)
        selectDatum = selectMember(12)
        self.assertEqual(datum, selectDatum)

    def testMessages(self):
        """Test insert and select messages functions."""
        f = codecs.open("{0}/dummy/dummy_topic_2.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        data = bitcointalk.parseTopicPage(html)
        data = data['messages']
        insertMessages(data)
        # Make sure a second insert doesn't cause problems
        insertMessages(data)
        selectData = selectMessages(
            [
                8125509,
                8125667,
                8125970,
                8126348,
                8126542,
                8126615,
                8126655,
                8126666
            ])
        datum = data[0]
        self.assertEqual(data, selectData)

    def testTopic(self):
        """Test insert and select topic functions."""
        f = codecs.open("{0}/dummy/dummy_topic.html".format(
            os.path.dirname(os.path.abspath(__file__))), 'r', 'utf-8')
        html = f.read()
        f.close()
        datum = bitcointalk.parseTopicPage(html)
        del datum['messages']
        insertTopic(datum)
        # Make sure a second insert doesn't cause problems
        insertTopic(datum)
        selectDatum = selectTopic(14)
        self.assertEqual(datum, selectDatum)

if __name__ == "__main__":
    unittest.main()
