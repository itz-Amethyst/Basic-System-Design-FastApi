from random import randrange

import psycopg2
import inspect
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from models import Post
from utils.CustomMethods import find_post , find_index_post
import time
print(inspect.getsource(time.sleep(3)))

while True:

    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('Database Connected !')
        break
    except Exception as error:
        print("Connection To Database Failed !")
        print(f"Error: {error}")
        time.sleep(5)


app = FastAPI()

my_posts = [{"title": 'number 1', "content": "lots of bullshits", "rating": 3 , "published": True, "id": 1},
            {"title": 'number 2', "content": "lots of bullshits2", "rating": 3 , "published": True, "id": 2}]

@app.get('/')
async def root():
    return {"message": "hello there"}

#! Note: never reach to this so it will always run first one
# @app.get('/')
# async def root():
#     return {"message": "hello there 2"}

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    return{"data": cursor.fetchall()}


@app.post('/createpost', status_code = status.HTTP_201_CREATED)
def create_Post(new_post: Post):
    # print(new_post.model_dump())
    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)

    # %s kinda variable
    cursor.execute("""INSERT INTO posts(title, content, published, rating) VALUES (%s, %s, %s)""", (post.title, post.content, post.published, post.rating))
    new_post = cursor.fetchone()
    # like -> Save changes ! don't forget
    conn.commit()

    return{"data": new_post}


#? orders matter so first implement static ones than generics
@app.get('/posts/latest')
def get_latest_post():
    latest_post = my_posts[len(my_posts)-1]
    return {'data': latest_post}


@app.get("/posts/{id}")
def get_post_by_id(id:int, response: Response):
    post = find_post(id, my_posts)
    if not post:

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with this id: {id} was not found")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with this id {id} was not found"}
    return {'data': post}


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id, my_posts)

    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with this id {id} does not exists")

    my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    index = find_index_post(id , source = my_posts)

    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with this id {id} does not exists")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}