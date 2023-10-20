Scraping agent for a Cryptocurrencies forum
===================

Python agent to scrape for members and messages on bitcointalk.org

Installation
=============

a) Install Pipfile

b) Create tables in target PostgreSQL DB

c) Create .pgpass config in top-level of this repo with connection string to the DB from step 2 using the following format:

http://www.postgresql.org/docs/9.1/static/libpq-pgpass.html

d) Create "data" folder within the application folder, or change the _saveToFile method in memoizer.py to point to a different data directory.

Usage
=====

The primary crawler is designed to gather information about boards, members, messages, and topics falling within a user-defined range of topic IDs, as presented on bitcointalk.org. By default, this range encompasses topics from 1 to 50. You can adjust the range by simply editing the "startTopicId" and "stopTopicId" variables within "topic.py." To initiate the crawler, run "python topic.py" when you are ready.

To alleviate server load, the crawler defaults to an average 5-second interval between requests to bitcointalk.org. You can modify this by editing the "interReqTime" variable in bitcointalk.py to your desired value.

The main crawler file, "topic.py," is just one possible implementation of the crawler. The scraping interface, accessed through the memoizer sub-module, accommodates a variety of commands and is designed to avoid scraping the same URL multiple times. You are encouraged to build your own custom crawler using this foundation!