# '''using sqlalchemy now
# Pydantic schemas for post: have been moved to schemas file 
# PostBase and PostCreate.'''
# from typing import Optional
# from fastapi import  FastAPI, HTTPException,Response,Depends,status
# import fastapi
# import time
# from fastapi.params import Body
# from pydantic import BaseModel
# import psycopg2 
# from psycopg2.extras import RealDictCursor
# import models, schemas 
# from sqlalchemy.orm import Session
# from database import engine,get_db,SessionLocal

# # . means import models.py from current dir
# models.Base.metadata.create_all(bind=engine)
# # upon running uvicorn this ^ creates the Tables

# app = FastAPI()


# rds_url = "db-url.rds.amazonaws.com"

# '''if we don't use a while loop whin establishing a connection to a server
# the server connection will FAIL but our WSGI server will be up and running for no reason
# Thus we use a while loop and break out of it once connection is successful'''

# # try:
# #     conn = psycopg2.connect(host = rds_url,database='fastapi',
# #                             user = 'postgres', password='sd;klfcvmd;lm', cursor_factory= RealDictCursor)
# #     # RealDictCursor gives us the Column name and Columns
# #     cursor=conn.cursor()
# #     print("Database connection to rds was successful")

# # except Exception as error:
# #     time.sleep(2) # retry in 2
# #     print("Connection to your rds was unsuccessful")
# #     print(f"\n {error}")


# # @app is the decorator with get method
# @app.get("/") # path operation or route
# def root():
#     return {"message": "Hello from World"} # converts dict to json
# # we will use uvicorn main:app 
# # the --reload flag in uvicorn allows us to auto start the server when we change the code

# # gets all the posts at once
# @app.get("/posts")
# def get_all_posts(db: Session = Depends(get_db)):
#     '''Anytime we use SQL Alchemy we have to pass db object into 
#     the path operation function. The db: Session creates a dependency of 
#     get_db function, search for dependency injection etc'''
#     # cursor.execute("""SELECT * FROM posts""")
#     # all_posts = cursor.fetchall()
#     posts = db.query(models.Post).all()
#     return posts


# # HTTP POST method
# @app.post("/posts",status_code=status.HTTP_201_CREATED) 
# def create_new_post(post: schemas.PostCreate,db: Session = Depends(get_db)): 
#     # # SANITIZE YOUR SQL pass in %s first and then the variables that are the columns
#     # # THIS PREVENTS SQL Injection
#     # cursor.execute("""INSERT INTO posts (title, content, published) 
#     #                VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
#     # new_post = cursor.fetchone() # this give us values from the RETURNING SQL keyword
#     # conn.commit() # to commit the staged changes into our we make into our db
#     # print(type(new_post))
#     # # return{f"New post created is {new_post}"}
#     # # both of these ^ give different responses
    
#     # post.title comes from the api request
#     # here post is from post: schemas.PostCreate i/e pydantic class from schemas file
#     new_post = models.Post(title=post.title,content=post.content,published=post.published)
#     # models.Post is the actual table which we have created a
#     # instead of doing post.title,post.content etc 
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post



# '''always ensure that the path variable in the decorator matches 
# the arg we pass to the fucntion below'''
# @app.get("/posts/{post_id}") # post_id is path parameter var 
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
# @app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
# def update_post(post_id:int,post: schemas.PostBase,db: Session = Depends(get_db)):
    
#     print(post) # prints the JSON we get from the route
#     post_query = db.query(models.Post).filter(models.Post.id == post_id) # this is the prepared Query for finding post
#     one_post = post_query.first() # this fetches the actual post

#     # This will only run if post is none i.e. doesn't exist
#     if one_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail = f"Post w/ id {post_id} doesn't exist")
    
#     post_query.update(post.dict(),synchronize_session=False)
#     # this will send whatever we receive in the api request
#     # into the update func which takes a dict{}
#     # this is already verified by pydantic
#     db.commit()

#     return {f"Post w/ id {post_id} now has the data": post_query.first()}










