from typing import Optional , List

from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy import update , func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app import schemas

from app.managers.auth import AuthManager

from app.db.models import Post , Vote

router = APIRouter(
    prefix = '/post',
    tags = ['Posts']
)

@router.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    return {"message": db.query(Post).all()}

# @router.get('/', response_model = list[schemas.PostView])
@router.get('/', response_model = List[schemas.PostViewWithVotes], dependencies = [Depends(AuthManager.get_current_user)])
def get_posts( db: Session = Depends(get_db) , Limit: int = 10 , skip: int = 0 , search: Optional[str] = "" ):
    print(search)

    # Two different query
    results = (db.query(Post, func.count(Vote.post_id).label('votes'))
               .join(Vote, Vote.post_id == Post.id, isouter = True)
               .filter(Post.title.contains(search) , Post.content.contains(search))
               .group_by(Post.id).limit(Limit).offset(skip)
               .all())

    # , == or no difference
    # posts = db.query(Post).filter(Post.title.contains(search) , Post.content.contains(search)).limit(Limit).offset(skip).all()

    # return list(dict(results))

    return results

@router.get("/specific_posts", response_model = list[schemas.PostViewWithVotes])
def get_current_user_posts( db:Session = Depends(get_db) , current_user = Depends(AuthManager.get_current_user) ):

    posts = (db.query(Post, func.count(Vote.post_id).label('votes'))
               .join(Vote, Vote.post_id == Post.id, isouter = True)
               .filter(Post.owner_id == current_user.id)
                .group_by(Post.id)
               .all())


    # Without Votes
    # posts = db.query(Post).filter(Post.owner_id == current_user.id).all()

    if len(posts) == 0:
        return Response(content = f"No Post Created for user {current_user.id}")

    return posts


@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.PostView)
def create_Post( post: schemas.CreatePost , db: Session = Depends(get_db) , current_user: str = Depends(
    AuthManager.get_current_user) ):

    #? Old way
    # new_post = models.Post(title = post.title, content = post.content, published = post.published, rating = post.rating)

    #! Shorter way
    #* Note: ** -> unpack
    print(current_user)
    new_post = Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model = schemas.PostView)
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    # post = db.query(models.Post).filter(models.Post.title == title).first()
    post2 = db.query(Post).get(id)

    if not post2:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    return post2


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post( id:int , db: Session = Depends(get_db) , current_user = Depends(AuthManager.get_current_user) ):

    post = db.query(Post).get(id)


    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN ,
                            detail = f"Not Authorized to perform requested action")

    db.delete(post)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT,)

@router.put('/{id}', response_model = schemas.PostView)
def update_post( id:int , post: schemas.UpdatePost , db: Session = Depends(get_db) , current_user = Depends(
    AuthManager.get_current_user) ):

    post = db.query(Post).get(id)


    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN ,
                            detail = f"Not Authorized to perform requested action")

    # you can put exclude here later
    db.execute(update(Post).where(Post.id == id), post.dict())
    db.commit()

    return post

