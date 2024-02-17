"""
    FastAPI freecodecamp sanjeev the venv folder is the virtual environment named venv. It's localized to this folder directory
    change interpreter path in vscode Command palette then use virtual env in the terminal as well
    "python3 -m venv venv" to create a virtual env in terminal
    "source venv/bin/activate" to activate in the terminal using the file in bin/ in venv/
    we put main.py in app folder amd make an empty __init__.py file to let pyhton know that this is a package
    "pip install psycopg2-binary" cuz just install psycopg2" didn't work
"""

from typing import Optional
from fastapi import FastAPI, HTTPException,Response,status
import fastapi
import time
from fastapi.params import Body
from httpx import post
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor

app = FastAPI()
rds_url = "db-url.rds.amazonaws.com"

#if we don't use a while loop whin establishing a connection to a server
# the server connection will FAIL but our WSGI server will be up and running for no reason
# Thus we use a while loop and break out of it once connection is successful

try:
    conn = psycopg2.connect(host = rds_url,database='fastapi',
                            user = 'postgres', password='dkchgdk', cursor_factory= RealDictCursor)
    # RealDictCursor gives us the Column name and Columns
    cursor=conn.cursor()
    print("Database connection to rds was successful")

except Exception as error:
    time.sleep(2) # retry in 2
    print("Connection to your rds was unsuccessful")
    print(f"\n {error}")
    




class Posts(BaseModel): # Class for social media posts extends Pydantic BasModel
    # we set title and content to stringtype
    title: str
    content: str
    published: bool = True # published allows for bool values and default set to True
    rating: Optional[int] = None # This field takes an optional int value and defulats to none
    # ie it send nothing back if not in the request

# Hardcoded my_posts a list with dict
my_posts = [{"title": "test","content":"This is fun","id":1},
            {"title": "vehicles","content":"I like cars","id":2}]

# @app is the decorator with get method
@app.get("/") # path operation or route
def root():
    return {"message": "Hello from World"} # converts dict to json
# we will use uvicorn main:app 
# the --reload flag in uvicorn allows us to auto start the server when we change the code


def find_post(id): # id should be integer type
    for p in my_posts:
        if p['id']==id:
            return p # return the post where ID matches

def find_index_post(id): # This func finds index of id in post which is used to delete said post
    for i,p in enumerate(my_posts): # enumerate allows us to work with both index and iterable use gpt 4 
        if p["id"] == id:
            return i

# gets all the posts at once
@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    return{"data":all_posts}


# HTTP POST method
@app.post("/posts",status_code=status.HTTP_201_CREATED) 
def create_new_post(post: Posts): # create a pydantic object from Posts class called 'post'
    # SANITIZE YOUR SQL pass in %s first and then the variables that are the columns
    # THIS PREVENTS SQL Injection
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone() # this give us values from the RETURNING SQL keyword
    conn.commit() # to commit the staged changes into our we make into our db
    print(type(new_post))
    # return{f"New post created is {new_post}"}
    # both of these ^ give different responses
    return{f"New post created is":new_post}



# Cleaner way is to raise HTTPException
@app.get("/posts/{id}") # path parameter var
def get_one_post(id: int):
    post_id=id
    print(type(post_id))
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(post_id,))
    
    '''cursor.execute requires a tuple when giving params
    thus we pass it as (post_id,) which is a tuple, we can also pass post_id as a string
    post_id is of the type int'''
    one_post =cursor.fetchone()
    '''WHEN AN INVALID ID IS ENTERED cursor.fetchone() returns None
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html'''
    
    if one_post == None: ## if not one_post also works
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post w/ id {post_id} doesn't exist")
    conn.commit()
    return(f"post with id {post_id} is {one_post}")




@app.delete("/posts/{id}",status_code=status.HTTP_202_ACCEPTED) 
def delete_post(id: int): # pass id which we get from path parameters
    # find index in the array which has the required id
    post_id = id
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(post_id),))
    del_post=cursor.fetchone()
    conn.commit()
    if del_post == None:
        # raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail = f"Post w/ id {id} doesn't exist")
        return{Response(status_code=status.HTTP_404_NOT_FOUND, content=f"Post w/ id {id} doesn't exist")}
    '''we send back 204 error code using repsonse class since fastapi
        normally does not send back the Json message in return statement'''
    return{Response(status_code=status.HTTP_204_NO_CONTENT,content=f"Post w/ id {id} has been deleted")}


# passing the status code into the decorator allows us to customize our status codes based on the operation
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int,post: Posts):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title,post.content,post.published,id))
    updated_post=cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post w/ id {id} doesn't exist")
    
    return {f"Post w/ id {id} now has the data": updated_post}










