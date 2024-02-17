from typing import Optional
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime

class PostBase(BaseModel): # Class for social media posts extends Pydantic BasModel
    # we set title and content to stringtype
    title: str
    content: str
    published: bool = True # published allows for bool values and default set to True
'''We create a PostBase class which contains attributes that out pydantic model will validate.
These arguments ar evaluated by pydantic when our api route is hit and api inputs are given.
Eg when title is entered it has to be a string value and not an integer value'''

class PostCreate(PostBase):
    pass # pass allows one class to inherit from the other clas
    # we don't have to provide anything in the PostCreate class
    # it inherits all


class UserOut(BaseModel):
    # we should never send back the password to the user
    id: int
    email: EmailStr
    created_at: datetime

class PostResponse(PostBase):
    # title: str  content: str    published:bool can be inherited from PostBase
    id: int   
    created_at: datetime
    owner_id: int
    '''class Config:
        orm_mode = True # used to be required'''
    # owner: UserOut
    '''owner obj of UserOut class this has been done to test out relationships in SQL Alchemy
    which appends the info of the creator  of the post along with the content of the post 
    when we do a get post or get all post operation'''

class PostWithVote(PostResponse):
    votes: int


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]=None
    '''TO PREVENT ERRORS KEEP DATATYPE OF "id" THE SAME IN 
        THIS SCHEMA AND THE FUNCTION login() PRESENT IN AUTH.PY FILE BECAUSE THIS IS WHERE THE JWT
        IS CREATED. WHEN A PROTECTED ROUTE IS HIT THE JWT IS VERIFIED AND DECODE AND THIS SCHEMA
        IS USED TO VALIDATE  token_data = schemas.TokenData(id = id) present in
        verify_access_token of oauth2.py
        
        def login():
            user = db.query(models.User).filter(models.User.email == creds.username).first()
            access_token = oauth2.create_access_token(data = {"user_id":str(user.id)})
            return {"access_token": access_token,"token_type":"bearer"}
        '''
    
class Vote(BaseModel):
    post_id: int
    dir: conint(ge = 0, le = 1)
    ''' this allows us to validate that the value for dir is only 0 or 1.
    dir is direction of vote 0 is remove and 1 is upvote
    '''
    