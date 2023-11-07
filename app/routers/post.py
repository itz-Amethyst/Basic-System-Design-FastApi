from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db
from .. import models
from .. import schemas

router = APIRouter(
    prefix = '/post',
    tags = ['Posts']
)

@router.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):

    return {"message": db.query(models.Post).all()}

@router.get('/', response_model = list[schemas.PostView])
def get_posts(db: Session = Depends(get_db)):

    return db.query(models.Post).all()


@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.PostView)
def create_Post(post: schemas.CreatePost, db: Session = Depends(get_db)):

    #? Old way
    # new_post = models.Post(title = post.title, content = post.content, published = post.published, rating = post.rating)

    #! Shorter way
    #* Note: ** -> unpack
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model = schemas.PostView)
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    # post = db.query(models.Post).filter(models.Post.title == title).first()
    post2 = db.query(models.Post).get(id)

    if not post2:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    return post2


@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):


    post = db.query(models.Post).get(id)


    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    db.delete(post)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT,)

@router.put('/{id}', response_model = schemas.PostView)
def update_post(id:int, post: schemas.UpdatePost, db: Session = Depends(get_db) ):

    post2 = db.query(models.Post).get(id)

    if post2 is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    # you can put exclude here later
    db.execute(update(models.Post).where(models.Post.id == id), post.dict())
    db.commit()

    return post

