# FastAPI freecodecamp sanjeev the venv folder is the virtual environment named venv. It's localized to this folder directory
# change interpreter path in vscode Command palette then use virtual env in the terminal as well
# "python3 -m venv venv" to create a virtual env in terminal
# "source venv/bin/activate" to activate in the terminal using the file in bin/ in venv/
# we put main.py in app folder amd make an empty __init__.py file to let pyhton know that this is a package


from typing import Optional
from fastapi import FastAPI, HTTPException,Response,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


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
def all_posts():
    return {"data":my_posts} # fastapi will serialize the list into json


# @app.post("/posts") # HTTP POST method
# def create_posts(post: Posts): 
#     # def create_posts(payload: dict = Body(...)):  Extract into dict
#     # extract everything sent in the body of post request
#     # extract that JSON and store as dictionary inside a var payload
#     title = post.title
#     content = post.content

#     print(f"title: {title}, rating is {post.rating}")
#     return{"message":"successfully created post"}

# HTTP POST method
@app.post("/posts",status_code=status.HTTP_201_CREATED) 
def create_posts(post: Posts): # create an object from Posts class
    post_dict = post.dict() # create a dict of post object
    post_dict['id'] = randrange(3,40000) # assigns a random ID makes and id key in the dict
    my_posts.append(post_dict)
    return {"data": post_dict}

# We want to force the client to send data in a schema that we expect
# i.e. they don't send us junk parameters 
# Thus we validate our data using pydantic 

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# CRUD app
# order is very important when working with path parameters
# @app.get("/posts/{id}") # path parameter var
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post: 
#         print("Not a post i.e post is None")
#         response.status_code = 404
#         # we can also import status class from fastapi to get the HTTP code
#         return {"detail":f"{id} doesn't exist"}
#     return {"post_detail":f"post is {post}"} 

# Cleaner way is to raise HTTPException
@app.get("/posts/{id}") # path parameter var
def get_one_post(id: int, ):
    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesn't exist")
    return {"post_detail":f"post is {post}"} 

@app.delete("/posts/{id}") 
# passing the status code into the decorator allows us to customize our status codes based on the operation
def delete_post(id: int): # pass id which we get from path parameters
    # find index in the array which has the required id
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post w/ id {id} doesn't exist")
    my_posts.pop(index)
    return{Response(status_code=status.HTTP_204_NO_CONTENT)}
    # when we send back a 204 error code it does not send back the Json message in return statement
    # this is a feature of FastAPI

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int,post: Posts):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post w/ id {id} doesn't exist")
    post_dict = post.dict()
    post_dict["id"] = id # change the ID key to the id we received from path params
    my_posts[index] = post_dict

    return {"message": f"Post with id {id} has been updated with {post}"}









