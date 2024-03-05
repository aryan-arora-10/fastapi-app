
from typing_extensions import deprecated
from fastapi import  FastAPI
from . import models, schemas 
from app.database import engine
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

''''Please start using absolute paths and not relative paths. Also run the FastAPI main file using 
uvicorn app.main:app because main file is in the app/  directory.
Running from the app directory i.e. uvicorn main:app --reload will throw errors such as 
no module named app because we have imported certain files e.g from **app.database import engine**
in our main file'''
# models.Base.metadata.create_all(bind=engine)
# upon running uvicorn main:app this ^ creates the Tables

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router) 
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(vote.router) 

# @app is the decorator with get method
@app.get("/") # path operation or route
def root():
    return {"message": "Hello from World after CICD"} # converts dict to json
# we will use uvicorn main:app 
# the --reload flag in uvicorn allows us to auto start the server when we change the code

