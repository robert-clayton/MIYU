from Declarative import Base, User, Tweet, Engine
from Credentials import TWITTER
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from twython import TwythonStreamer
import time

DBSession = sessionmaker(bind=Engine)
session = DBSession()

class Birdwatcher(TwythonStreamer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total = 0
        self._startTime = time.time()

    def on_success(self, data):
        if not data['lang'] == 'en':
            return 
        self.process_tweet(data)
        
    def on_error(self, status_code, data):
        print(f'Error occurred. {status_code} - {data}')
        session.commit()
        self.disconnect()

    def on_timeout(self):
        session.commit()
        self.disconnect()

    def process_tweet(self, data):
        # Update original tweet's RT count if RT/add entry if not exists
        if 'retweeted_status' in data:
            tweet = session.query(Tweet).filter(Tweet.id == data['retweeted_status']['id']).first()
            if tweet:
                tweet.retweet_count = data['retweeted_status']['retweet_count']
            else:
                session.add(Tweet.new(data['retweeted_status']))
            session.commit()
            return

        # Add user if not exists
        if not session.query(User).filter(User.id == data['user']['id']).scalar():
            session.add(User.new(data))

        # Add tweet if not exists
        if not session.query(Tweet).filter(Tweet.id == data['id']).scalar():
            session.add(Tweet.new(data))

        session.commit()

watcher = Birdwatcher(TWITTER['consumer_key'], TWITTER['consumer_secret'], TWITTER['access_token'], TWITTER['access_secret'])

try:
    watcher.statuses.filter(track='python')
except KeyboardInterrupt:
    watcher.disconnect()
