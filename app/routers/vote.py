from fastapi import APIRouter , status , Depends , HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db.database import get_db
from app.deps.auth import user_required
from app.db.models import Vote , Post
from app.deps import rate_limit

# you can define dependency here either to apply on all apis

router = APIRouter(
    prefix = '/vote',
    tags = ['Vote'],
    dependencies = [Depends(user_required), rate_limit('vote', 60, 30, use_id = False)]
)


@router.post('/', status_code = status.HTTP_201_CREATED)
def vote( vote: schemas.Vote , db : Session = Depends(get_db) , current_user: schemas.TokenData = Depends(user_required)):

    found_vote: Vote = db.query(Vote).filter(Vote.post_id == vote.post_id , Vote.user_id == current_user.id).first()

    check_exists = db.query(Post).filter(Post.id == vote.post_id).first()

    if check_exists is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Post with id {vote.post_id} does not exists!!!')

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")

        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {'message': "successfully added vote!"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Vote does not exists")

        db.delete(found_vote)
        db.commit()

        return {'message': "Successfully deleted vote!"}
