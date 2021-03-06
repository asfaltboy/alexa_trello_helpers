import logging
import os

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, create_engine)
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)
Base = declarative_base()


class SaveMixin(object):
    """ Implement a helpful save method to create or update a record """
    def save(self, force_update=False):
        """
        Use force_update to always flag the instance as dirty and commit
        to database.
        """
        try:
            if not self.id:
                session.add(self)
            session.commit()  # NOTE: we may not need to call this
        except DBAPIError as exc:
            logger.exception(f'Could not save AlexaUser instance in DB: {exc}')
            session.rollback()
        return self


class AlexaUser(SaveMixin, Base):
    __tablename__ = 'alexa_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), unique=True)
    trello_user_id = Column(Integer, ForeignKey('trello_users.id'))
    trello_user = relationship("TrelloUser", backref='alexa_users')
    ctime = Column(DateTime, server_default=func.now())

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f'<AlexaUser {self.id}>'

    @staticmethod
    def get_user(user_id):
        return session.query(AlexaUser).filter_by(user_id=user_id).first()


class TrelloUser(SaveMixin, Base):
    __tablename__ = 'trello_users'

    id = Column(Integer, primary_key=True)
    auth_token = Column(String(255), unique=True)
    auth_api_key = Column(String(255))
    auth_api_secret = Column(String(255), nullable=True)
    auth_token_secret = Column(String(255), nullable=True)

    default_board = Column(String(255), nullable=True)

    def __init__(self, auth_token, auth_api_key,
                 auth_api_secret=None, auth_token_secret=None):
        self.auth_token = auth_token
        self.auth_api_key = auth_api_key
        self.auth_api_secret = auth_api_secret
        self.auth_token_secret = auth_token_secret

    @staticmethod
    def get_user(alexa_user_id):
        return session.query(TrelloUser).join(AlexaUser).filter(
            AlexaUser.user_id == alexa_user_id).first()

    def __repr__(self):
        return f'<TrelloUser {self.id}>'


# an Engine, which the Session will use for connection
# resources
DEFAULT_DATABASE_URL = 'sqlite:///alexa_trello_skill.db'
engine = create_engine(os.environ.get('DATABASE_URL') or DEFAULT_DATABASE_URL)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
