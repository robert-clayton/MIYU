# MIYU: My Internet Yanking Unicorn

A tool for scraping data from popular social media websites. Currently only grabs random images from Imgur.

[![](https://badgen.net/github/license/robert-clayton/ILYA)](https://github.com/robert-clayton/MIYU/master/LICENSE.txt) [![](https://badgen.net/github/last-commit/robert-clayton/ILYA)](https://github.com/robert-clayton/MIYU/commits/master)

# Requirements

- Python 3.6

# How to Use

- Open/cd terminal into repo directory
- Run as module, e.g. `python -m miyu`
- Left click image to get new random image
- Right click to save image
- R key to get/save 10,000 random images

# DB Architecture
Twitter User
- ID (int primary key unique)
- Name (str)
- Handle (str)
- IconPath (str)
- Bio (str)
- Location (str)
- Created On (str)
- Tweets Per Day (int)
- Replies Per Day (int)
- URL (str)

Hashtag
- ID (int primary key foreign key unique)
- Tag (str)

Tweet
- ID (int primary key foreign key unique)
- IsRetweet (bool)
- Content (str)
- MediaPath (str)
- Date (DATETIME)
- URL (str)

UserFollowers
- UserID (int primary key foreign key)
- FollowerID (int foreign key)

TweetReplies
- TweetID (int primary key foreign key)
- ReplyID (int foreign key)

HashtagTweet
- HashtagID (int primary key foreign key)
- TweetID (int foreign key)

