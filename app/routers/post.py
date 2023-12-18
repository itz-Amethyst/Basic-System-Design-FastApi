from typing import Optional , List

from fastapi import Depends, HTTPException, status, Response, APIRouter, Request
from sqlalchemy import update , func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app import schemas
from app.deps.auth import user_required , get_current_user_info
from app.deps import rate_limit

from app.db.models import Post , Vote
from Cyrus import cache


router = APIRouter(
    prefix = '/post',
    tags = ['Posts'],
    # dependencies=[rate_limit('post', 60, 30, False)]
    dependencies = [Depends(user_required)]
)

@router.get('/sqlalchemy')
@cache(expire = 60)
def test_posts(db: Session = Depends(get_db)):

    return  db.query(Post).all()

# @router.get('/', response_model = list[schemas.PostView])
@router.get('/', response_model = List[schemas.PostViewWithVotes], dependencies = [rate_limit('posts:get', 60, 30)])
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

# Cache doesn't work on this query cause complicated and data is not ok to read
@router.get("/specific_posts", response_model = list[schemas.PostViewWithVotes])
#! @cache(expire = 20)
def get_get_current_user_posts(request: Request, db:Session = Depends(get_db)):

    current_user = get_current_user_info(request = request)

    posts = (db.query(Post, func.count(Vote.post_id).label('votes'))
               .join(Vote, Vote.post_id == Post.id, isouter = True)
               .filter(Post.owner_id == current_user.id)
                .group_by(Post.id)
               .all())


    # Without Votes
    # posts = db.query(Post).filter(Post.owner_id == get_current_user.id).all()

    if len(posts) == 0:
        return Response(content = f"No Post Created for user {current_user.id}")

    return posts


@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.PostView, dependencies = [rate_limit('posts:create', 60, 30)])
def create_Post(request: Request, post: schemas.CreatePost , db: Session = Depends(get_db)):

    current_user = get_current_user_info(request = request )

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
@cache(expire = 20)
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    # post = db.query(models.Post).filter(models.Post.title == title).first()
    post2 = db.query(Post).get(id)

    if not post2:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    return post2


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(request: Request, id:int , db: Session = Depends(get_db)):

    current_user = get_current_user_info(request = request)
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

@router.put('/{id}', response_model = schemas.PostView, dependencies = [rate_limit('posts:update', 60, 30)])
def update_post(request: Request, id:int , post: schemas.UpdatePost , db: Session = Depends(get_db)):

    current_user = get_current_user_info(request = request)

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

