from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import instance_dict
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
# the code that is commented below are the raw sql code
# Which is used when we do not want to use any ORM and we are comfortable with sql


@router.get("/")
def read_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cur.execute("""SELECT * FROM posts""")
    # posts=cur.fetchall()
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts_dict = []
    for post, count in posts:
        post_dict = instance_dict(post)
        post_dict["votes"] = count
        posts_dict.append(post_dict)

    return posts_dict


@router.get("/{id}", response_model=schemas.PostResponse)
def read_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # cur.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post=cur.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id}not found")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    print(current_user)

    # cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) Returning *"""
    #             ,(post.title,post.content,post.published))
    # post = cur.fetchone()
    # conn.commit()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    # deleted_post=cur.fetchone()
    # conn.commit()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id {id}not found")
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot delete this")
    post_query.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(post: schemas.PostCreate, id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s Returning *""",
    #             (post.title, post.content, post.published, id,))
    # updated_post=cur.fetchone()
    # conn.commit()

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The message with id {id}not found")
    if post_query.first().owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot delete this")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
