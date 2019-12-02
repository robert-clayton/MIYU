import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    screen_name = db.Column(db.String(15), nullable=False)
    url = db.Column(db.String(250))
    description = db.Column(db.String(250))
    location = db.Column(db.String(250))
    created_at = db.Column(db.String(250))

    @staticmethod
    def new(data):
        return User(
            id=data['user']['id'], 
            name=data['user']['name'], 
            screen_name=data['user']['screen_name'], 
            url=data['user']['url'], 
            description=data['user']['description'], 
            location=data['user']['location'],
            created_at=data['user']['created_at'],
        )

class Tweet(Base):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    created_at = db.Column(db.String(250))
    content = db.Column(db.String(280), nullable=False)
    # longitude = db.Column(db.Float)
    # latitude = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reply_to_id = db.Column(db.Integer)
    reply_to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    retweet_count = db.Column(db.Integer)
    user = relationship(User, foreign_keys=user_id)
    reply_to_user = relationship(User, foreign_keys=reply_to_user_id)

    @staticmethod
    def new(data):
        # if data['coordinates']:
        #     longitude = data['coordinates']['coordinates'][0]
        #     latitude = data['coordinates']['coordinates'][1]
        # else:
        #     longitude, latitude = None, None
        return Tweet(
            id=data['id'],
            created_at=data['created_at'],
            content=data['text'],
            # longitude=longitude,
            # latitude=latitude,
            user_id=data['user']['id'],
            reply_to_id=data['in_reply_to_status_id'],
            reply_to_user_id=data['in_reply_to_user_id'],
            retweet_count=data['retweet_count'],
        )

Engine = db.create_engine('sqlite:///data.db')
Base.metadata.bind = Engine
Base.metadata.create_all(Engine)
