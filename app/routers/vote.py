from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db
from app.oauth2 import get_current_user
from app.config import settings 


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/",status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}
    
        

