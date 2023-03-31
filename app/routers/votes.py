from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)


@router.post("/")
def vote_me(vote: schemas.Vote, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Votes).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="post not found")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                               models.Votes.users_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="vote already exist")
        new_vote = models.Votes(post_id = vote.post_id, users_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="vote already deleted")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"voted deleted successfully"}
