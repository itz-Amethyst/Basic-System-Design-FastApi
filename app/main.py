
from fastapi import FastAPI , Response , status , HTTPException, Depends
from models import Post

from . import models
from .database import engine , get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "hello there"}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"message": db.query(models.Post).all()}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):


    return{"data": db.query(models.Post).all()}


@app.post('/createpost', status_code = status.HTTP_201_CREATED)
def create_Post(post: Post, db: Session = Depends(get_db)):

    #? Old way
    # new_post = models.Post(title = post.title, content = post.content, published = post.published, rating = post.rating)

    #! Shorter way
    #* Note: ** -> unpack
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return{"data": "test"}

@app.get("/posts/{id}")
def get_post_by_id(id:int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # post2 = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND ,
                            detail = f"post with this id: {id} was not found")

    return {'data': post}


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):




    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id:int, post:Post):

    return {'data': "test"}