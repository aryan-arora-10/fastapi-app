from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base): # Class Post extends base
    __tablename__="posts"

    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE',nullable=False) 
    # server deafult updates the constraint in the properties of the table
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    # server_default allows us to insert a timestamp from the DB if we aren't able to do it
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    '''ondelete CASCADE ATTR removes all the posts associated with a user when said user is deleted.
    ********relationships SQL alchemy****'''
    owner = relationship("User")

# USer table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable = False,unique = True)# unique prevents a user from registering twice
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Votes(Base):
    __tablename__ = "votes"

    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)