from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts



@router.post("/",status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict(),owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/latest",response_model=schemas.Post)
def get_latest_post(db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).order_by(models.Post.id.desc()).first()
    return post



@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return post




@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()