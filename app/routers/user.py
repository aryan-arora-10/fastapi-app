from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, utils
from app.utils import hasher
from ..database import get_db

'''once we define prefix for routes we don't have to mention it in each decorator
    We can simply refence the routes as "/" later on'''

router = APIRouter(tags = ['User API\'s'])

#===========================================================================================
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut) 
def create_new_user(user: schemas.UserCreate,db: Session = Depends(get_db)): 
    hashed_password = hasher(user.password) 
    user.password = hashed_password # set user genearted password back to paswd attr of USER obj

    teste = user.model_dump()#CONVERT TO DICT()
    print("this is user dict was being printed during pytest") 
    # print(teste)
    new_user = models.User(**teste)
    '''**teste unpacks the dict and puts it into the db.add(models.User(**teste))
    sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint
    "users_email_key" DETAIL:  Key (email) already exists. to fix this cleanly we wil try except integrity error
    whenever user hits the API again with the same '''
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already in use")


@router.get("/users/{user_id}",response_model=schemas.UserOut)
def get_user(user_id: int,db: Session = Depends(get_db)):
    one_user = db.query(models.User).filter(models.User.id == user_id).first() 
    print(one_user)
    # user = db.query(<tablename model>).filter(<table>.<column_name> == user_id).first()     
    if not one_user: # something we will get if db.query returns None
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return one_user
    