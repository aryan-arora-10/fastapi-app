# '''This file now contains all the posts operations and getuser and createuser operations
# Using sql alchemy and pydantic request and response schemas
# which are put unto the decorators. After this we will split the files into posts.py and user.py
# and use routers  '''
# from typing import Optional,List
# from typing_extensions import deprecated
# from fastapi import  FastAPI, HTTPException,Response,Depends,status
# import fastapi
# from fastapi.params import Body
# from pydantic import BaseModel
# import psycopg2 
# from psycopg2.extras import RealDictCursor
# import models, schemas 
# from utils import hasher
# from database import engine,get_db,SessionLocal
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError


# models.Base.metadata.create_all(bind=engine)
# # upon running uvicorn this ^ creates the Tables

# app = FastAPI()


# # @app is the decorator with get method
# @app.get("/") # path operation or route
# def root():
#     return {"message": "Hello from World"} # converts dict to json
# # we will use uvicorn main:app 
# # the --reload flag in uvicorn allows us to auto start the server when we change the code

# '''We have included list from the Typing library to allow us to return a list of posts,
# because if we simply set response_model to schemas.PostResponse we can only handle a single post
# and can't handle multiple posts which the query.all() operation spits out'''
# @app.get("/posts",response_model=List[schemas.PostResponse])
# def get_all_posts(db: Session = Depends(get_db)):
#     '''Anytime we use SQL Alchemy we have to pass db object into 
#     the path operation function. The db: Session creates a dependency of 
#     get_db function, search for dependency injection etc'''
#     posts = db.query(models.Post).all()
#     print(posts)
#     # print(f"\n\nThe type of posts received is {type(posts)}")
#     return posts


# # HTTP POST method
# @app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse) 
# def create_new_post(post: schemas.PostCreate,db: Session = Depends(get_db)): 
  
#     '''post.title comes from the api request
#     here post is from post: schemas.PostCreate i/e pydantic class from schemas file
#     new_post = models.Post(title=post.title,content=post.content,published=post.published)'''
#     teste = post.dict()
#     print(teste)
#     new_post = models.Post(**teste)#unpack dict and pass each key value as argument 
#     # models.Post is the actual table which we have created a
#     # instead of doing post.title,post.content etc we can 
#     db.add(new_post)
#     db.commit() 
#     db.refresh(new_post)
#     return new_post



# '''always ensure that the path variable in the decorator matches 
# the arg we pass to the fucntion below'''
# @app.get("/posts/{post_id}",response_model=schemas.PostResponse) # post_id is path parameter var 
# def get_one_post(post_id: int,db: Session = Depends(get_db)):
#     print(f"post_id is {post_id}")
#     # models.Post is essentially the DB Table described in a pythonic way
#     # here we check the Id column is equal t
#     one_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     '''we have use .first() because we know there is only one entry with the ID
#     as the id we have picked is unique
#     we can use .all() if we want to find all the possible entries'''
#     if not one_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {post_id} does not exist")
#     return one_post




# @app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT) 
# def delete_post(post_id: int, db: Session = Depends(get_db)): 
#     one_post = db.query(models.Post).filter(models.Post.id == post_id)
#     if one_post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {post_id} does not exist")
#     one_post.delete(synchronize_session=False)
#     db.commit() # because we are actually altering the Database

#     return Response(status_code=status.HTTP_204_NO_CONTENT)






# # passing the status code into the decorator allows us to customize our status codes based on the operation
# @app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.PostResponse)
# def update_post(post_id:int,post: schemas.PostBase,db: Session = Depends(get_db)):
    
#     print(post) # prints the JSON we get from the route
#     post_query = db.query(models.Post).filter(models.Post.id == post_id) # this is the prepared Query for finding post
#     one_post = post_query.first() # this fetches the actual post

#     # This will only run if post is none i.e. doesn't exist
#     if one_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail = f"Post w/ id {post_id} doesn't exist")
    
#     post_query.update(post.model_dump(),synchronize_session=False)
#     '''this will send whatever we receive in the api request
#     into the update func which takes a dict{}
#     this is already verified by pydantic'''
#     db.commit()

#     return post_query.first()

# #~~~~$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$~~~~~~~~$$$$$$$$$$$$~~~~~~~$$$$$$$$$$$$$$$$$
# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut) 
# def create_new_user(user: schemas.UserCreate,db: Session = Depends(get_db)): 
#     hashed_password = hasher(user.password) 
#     user.password = hashed_password # set user genearted password back to paswd attr of USER obj

#     teste = user.model_dump()#CONVERT TO DICT()
#     print(teste)

#     new_user = models.User(**teste)
#     # **teste unpacks the dict and puts it into the db.add(models.User(**teste))
#     ''' sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint
#     "users_email_key" DETAIL:  Key (email) already exists. to fix this cleanly we wil try except integrity error
#     whenever user hits the API again with the same '''
#     try:
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already in use")


# @app.get("/users/{user_id}",response_model=schemas.UserOut)
# def get_user(user_id: int,db: Session = Depends(get_db)):
#     one_user = db.query(models.User).filter(models.User.id == user_id).first() 
#     # user = db.query(<tablename model>).filter(<table>.<column_name> == user_id).first()     
#     if not one_user: # something we will get if db.query returns None
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
#     return one_user
    






