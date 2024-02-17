from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy import True_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas,oauth2
from ..database import get_db
from typing import List

router = APIRouter(tags = ['Posts']) # we can also give prefix here


#=========================================================================================== 
''' We have included list from the Typing library to allow us to return a list of posts,
    because if we simply set response_model to schemas.PostResponse we can only handle a single post
    and can't handle multiple posts which the query.all() operation spits out.

    ..limit,skip are query string parameters.we can also search using *contains*

    ..Our initial response schema was schema.PostResponse. Once we join the votes table
    and posts table we use PostWithVotes as our pydantic repsonse schema'''
#=========================================================================================== 

# @router.get("/posts") 
@router.get("/posts",response_model=List[schemas.PostWithVote])
def get_all_posts(limit: int = 10,skip: int=0, db: Session = Depends(get_db)):
    
    '''
    Anytime we use SQL Alchemy we have to pass db object into 
    the path operation function. The db: Session creates a dependency of 
    get_db function, search for dependency injection etc
    
    to get all posts
    posts = db.query(models.Post).all() OR WE CAN USE
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    print(f"\n\nThe type of posts received is {type(posts)}")

    db.query().all() results are in the format ***(<app.models.Post object at 0x7f411b762050>, 0)***
    this is a tuple of post object and the votes from the AGGREGATE FUNC AND OUTER LEFT JOIN
    '''
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # we format the SQL alchemy orm object into a 
    post_with_votes = [{
            "id": post.id,
            "title":post.title,
            "content":post.content,
            "published":post.published,
            "created_at":post.created_at,
            "owner_id":post.owner_id,
            "votes":votes
        } for post,votes in results]
    
    return post_with_votes


# HTTP POST method to create a media post
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse) 
def create_new_post(post: schemas.PostCreate,db: Session = Depends(get_db),
                    current_user : int = Depends(oauth2.get_current_user)): 
    print(f"\ncurrent_user from the get_current_user func() extracted after decoding JWT is {current_user}\n")
  
    '''
    ..: post.title comes from the api request
    here post is from post: schemas.PostCreate i/e pydantic class from schemas file
    new_post = models.Post(title=post.title,content=post.content,published=post.published)
    '''

    teste = post.model_dump()

    teste.update({"owner_id":current_user.id})
    print(f"printing the create post dictionary below")
    print(teste)
    new_post = models.Post(**teste)
    '''
    ..: unpack dict and pass each key value as argument 
    models.Post is the actual table which we have created a
    instead of doing post.title,post.content etc we can use ** to unpack dict{}
    ''' 
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post



'''always ensure that the path variable in the decorator matches 
the arg we pass to the fucntion below'''
@router.get("/posts/{post_id}",response_model=schemas.PostWithVote) # post_id is path parameter var 
def get_one_post(post_id: int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    print(f"post_id is {post_id}")
    # models.Post is essentially the DB Table described in a pythonic way
    # here we check the Id column is equal to the post_id we get from path param
    # one_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    '''we have use .first() because we know there is only one entry with the ID
    as the id we have picked is unique
    we can use .all() if we want to find all the possible entries'''
    
    one_post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    print(one_post)

    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} does not exist")
    post_with_votes = {
            "id": one_post[0].id,
            "title":one_post[0].title,
            "content":one_post[0].content,
            "published":one_post[0].published,
            "created_at":one_post[0].created_at,
            "owner_id":one_post[0].owner_id,
            "votes":one_post.votes
        }

    return post_with_votes


@router.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(post_id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)): 
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    one_post = post_query.first()
    if one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} does not exist")
    
    ''' current_user returns us an obj hence the != current user evaluates to false
    and we get a not authorized error. We must use **current_user.id** to get integer value
    '''
    if one_post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you are not authorized ")

    post_query.delete(synchronize_session=False)
    db.commit() # because we are actually altering the Database

    return Response(status_code=status.HTTP_204_NO_CONTENT)






# passing the status code into the decorator allows us to customize our status codes based on the operation
@router.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.PostResponse)
def update_post(post_id:int,post: schemas.PostBase,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    
    print(post) # prints the JSON we get from the route
    post_query = db.query(models.Post).filter(models.Post.id == post_id) # this is the prepared Query for finding post
    one_post = post_query.first() # this fetches the actual post

    # This will only run if post is none i.e. doesn't exist
    if one_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post w/ id {post_id} doesn't exist")
    
    ''' current_user returns us an obj hence the != current user evaluates to false
    and we get a not authorized error. We must use **current_user.id** to get integer value
    '''
    print(f"current user is {current_user.id}")
    if one_post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you are not authorized ")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    '''this will send whatever we receive in the api request
    into the update func which takes a dict{}
    this is already verified by pydantic'''
    db.commit()

    return post_query.first()