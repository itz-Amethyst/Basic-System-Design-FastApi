from fastapi import FastAPI
from fastapi.params import Body

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
async def create_Post(payload: dict = Body):
    print(payload)
    return{"new_post": f"successfuly created post {payload['tittle']} content: {payload['content']}"}