
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
def test_posts(db: Session = Depends(get_db())):
    return {"message": "success"}

@app.get('/posts')
def get_posts():

    return{"data":"test"}


@app.post('/createpost', status_code = status.HTTP_201_CREATED)
def create_Post(new_post: Post):


    return{"data": "test"}

@app.get("/posts/{id}")
def get_post_by_id(id:int, response: Response):


    return {'data': ""}


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):


    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id:int, post:Post):

    return {'data': "test"}