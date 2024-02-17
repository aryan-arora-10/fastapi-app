from datetime import datetime, timedelta,timezone
from fastapi import Depends,HTTPException,status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from .config import settings

'''
1. We'll require a SECRET_KEY to verify the tokens
2. Algo to be used HS256(HMAC with SHA-256)
3. Expiration time
'''

SECRET_KEY = settings.SECRET_KEY
# **terminal run to generate a key**: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  
"""The URL to obtain the OAuth2 token. This would be the *path operation*
   that has `OAuth2PasswordRequestForm` as a dependency."""



def create_access_token(data: dict):
    to_encode = data.copy()# dict{} type
    '''
        we want to prserve the data dict input so we edit the copy
        Set the JWT expiration time to 30 minutes from time of token generation.
    
        set value of expire to 30 minutes after datetime.now() w/ timezone as utc.
        This done because "datetime.now()" will take local time i.e IST as arg
        which the JWt func encodes as UTC and then adds + 5:30 GMT and 0:30 so we get time of expiry
        which is wrong by 6 hours'''

    # print(f"\nprinting datetime now() {datetime.now()}")
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # print(f"printing var expire: {expire}")
    to_encode.update({"exp":expire})# append expiration time to the claims/payload

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)

    return encoded_jwt #creates the JSON WEB TOKEN as str

''' 
    The arguments for the params of this function come from the "def get_current_user().
    Here we will decode the jwt, extract the ID if there is no id we will throw an error
    token_data is validated from out TokenData pydantic schema.
'''
def verify_access_token(token: str,credentials_exception): 
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) 
        '''
        checks the "exp" time claim in the payload. Calculates if the JWT is expired.
        if exp < (timenow - leeway):
            raise ExpiredSignatureError("Signature has expired.") # from jwt.py
        '''
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id) # check whether all the data we want is actually in the token 

    except JWTError:
        ''' The above statement excepts any error of JWTError class or class which extends JWTError
        '''
        raise credentials_exception
    
    return token_data # token data for the time being is the ID of the user extracted from payload


''' We can pass this as a dependency into any one of our path operations. Which wil
    Take the token from our request automatically verify if token is correct extract the id.
    ***Read up about FastAPI dependencies***
'''
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
 