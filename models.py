# MODELS

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import json

from sqlalchemy import Column, DECIMAL, BOOLEAN, VARCHAR, inspect
from sqlalchemy.dialects.postgresql import JSON, INTEGER, TEXT, ARRAY, TIMESTAMP, BIGINT
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import validates
from database import BaseModel, engine
from log_functions import log_error


# ---------------------------------------------------------------------------------------------------------------------
# USERS

# users
class User(BaseModel):
    """User model for users of the bot"""
    __tablename__ = 'bot_users'
    id = Column(BIGINT, primary_key=True)
    username = Column(TEXT, nullable=True)
    balance = Column(DECIMAL, default=5.0)
    recurrent_id = Column(TEXT, nullable=True)
    info = Column(JSON, default={})

    def __repr__(self) -> str:
        return str(self.id)


# get_user function
def get_user(data: str | int) -> User | None:
    """:param data: PK or username of User"""
    try:
        try:
            user_by_id = User.get(int(data))
            if user_by_id is not None:
                return user_by_id
        except:
            pass

        for user in User.all():
            try:
                if 'username' in user.info:
                    if user.info['username'] == data:
                        return user
            except:
                ...

        return None
    except Exception as e:
        log_error(e)
        return None


# creating unexisting tables
if __name__ == '__main__':
    print('create tables')
    inspector = inspect(engine)
    for model in BaseModel.__subclasses__():
        if not inspector.has_table(model.__tablename__):
            model.__table__.create(bind=engine, checkfirst=True)