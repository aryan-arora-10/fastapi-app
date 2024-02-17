from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2,database


router = APIRouter(tags = ['Vote'])

@router.post("/vote",status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user : int = Depends(oauth2.get_current_user)):
    
    '''this checks if the post_id has been upvoted by the current user
    ADD logic for when post_id is invalid and use outer joins for post and user table 
    '''
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post_exist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"POST_ID {vote.post_id} does not exist")
    

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                                   models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1): # ie user wants to set an upvote
        if found_vote: # user has already updated the particular post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted")
        else: # user wants to vote on a post and hasn't already done that
            new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message":"successfully added vote"} 
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"} 



