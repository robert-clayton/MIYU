import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

user_followers_association = db.Table('user_followers_association', Base.metadata,
    db.Column('follower_id', db.Integer, db.ForeignKey('twitter_users.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('twitter_users.id')),
)

hashtag_tweet_association = db.Table('hashtag_tweet_association', Base.metadata,
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtags.id')),
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.id')),
)

class TwitterUser(Base):
    __tablename__  = 'twitter_users'
    id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    handle = db.Column(db.String(50), nullable=False)
    icon_path = db.Column(db.String(250), nullable=False)
    bio = db.Column(db.String(250))
    location = db.Column(db.String(250))
    created_on = db.Column(db.String, nullable=False)
    followers_count = db.Column(db.Integer, nullable=False)
    following_count = db.Column(db.Integer, nullable=False)
    tweets_per_day = db.Column(db.Float)
    replies_per_day = db.Column(db.Float)
    url = db.Column(db.String(250))
    tweets = relationship('Tweet', back_populates='twitter_users')
    followers = relationship(
        'TwitterUser', 
        secondary=user_followers_association, 
        primaryjoin=id == user_followers_association.c.follower_id,
        secondaryjoin=id == user_followers_association.c.following_id,
        backref='following',
    )

    @staticmethod
    def new(data, media_directory):
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)
        return TwitterUser(
            id=data['user']['id'], 
            name=data['user']['name'], 
            handle=data['user']['screen_name'], 
            icon_path=media_directory + data['user']['id_str'],
            bio=data['user']['description'], 
            location=data['user']['location'],
            created_on=data['user']['created_at'],
            followers_count=data['user']['followers_count'],
            following_count=data['user']['following_count'],
            url=data['user']['url'], 
        )

class RedditUser(Base):
    __tablename__ = 'reddit_users'
    id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon_path = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.String, nullable=False)
    posts_per_day = db.Column(db.Float)
    comments_per_day = db.Column(db.Float)
    # subreddits = relationship('')

class Tweet(Base):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    is_retweet = db.Column(db.Integer, nullable=False)
    response_to = db.Column(db.Integer)
    content = db.Column(db.String(280))
    media_path = db.Column(db.String)
    created_on = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    twitter_user_id = db.Column(db.Integer, db.ForeignKey('twitter_users.id'))
    twitter_user = relationship('TwitterUser', back_populates='tweets')
    hashtags = relationship(
        'Hashtag',
        secondary=hashtag_tweet_association,
        back_populates='hashtags',
    )

    @staticmethod
    def new(data, media_directory):
        return Tweet(
            id=data['id'],
            is_retweet=hasattr(data, 'retweeted_status'),
            content=data['text'],
            media_path=media_directory + data['id_str'],
            created_on=data['created_at'],
            user_id=data['user']['id'],
            reply_to_id=data['in_reply_to_status_id'],
            reply_to_user_id=data['in_reply_to_user_id'],
            retweet_count=data['retweet_count'],
        )

class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)
    tweets = relationship(
        'Tweet',
        secondary=hashtag_tweet_association,
        back_populates='tweets',
    )

Engine = db.create_engine('sqlite:///data.db')
Base.metadata.bind = Engine
Base.metadata.create_all(Engine)
