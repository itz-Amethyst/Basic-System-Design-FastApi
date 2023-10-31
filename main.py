from fastapi import FastAPI
from fastapi.params import Body
from models import Post


app = FastAPI()

@app.get('/')
async def root():
    return {"message": "hello there"}

#! Note: never reach to this so it will always run first one
# @app.get('/')
# async def root():
#     return {"message": "hello there 2"}

@app.get('/posts')
def get_posts():
    return{"data": "test"}


@app.post('/createpost')
def create_Post(new_post: Post):
    # print(new_post)
    print(new_post.model_dump())
    return{"data": "new post ? !!"}