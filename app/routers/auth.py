from fastapi import APIRouter,Depends,status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from .. import models,schemas,utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(tags = ['Authentication API\'s'])


'''Continuous ERROR: 127.0.0.1:40538 - "POST /login HTTP/1.1" 404 Not Found
because app.include_router(auth.router) was not present in main.py file it gave 404detail not found error
which occurs when the route is not found or invalid
'''
@router.post("/login",response_model=schemas.Token)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    ''' print(creds.model_dump()) # to debug a pydantic schema 
    Oauth2PasswordRequestform will take in the parameters as username and password
    Thus when we construct our db query we use models.User.email == creds,username'''

    user = db.query(models.User).filter(models.User.email == creds.username).first()
    '''
    user obj gives us id, email,hashed password and created_at timestamp 
    '''

    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    '''user.password is the hashed password in the db
    utils.verify() returns bool value'''
    if not utils.verify(creds.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":str(user.id)})
    return {"access_token": access_token,"token_type":"bearer"}
