from fastapi import FastAPI , Response , status , HTTPException, Depends
from models import Post
from . import models
from app.db.database import engine, get_db
from sqlalchemy.orm import Session

# print(inspect.getsource(time.sleep(3)))

#region non_sense



# while True:
#
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print('Database Connected !')
#         break
#     except Exception as error:
#         print("Connection To Database Failed !")
#         print(f"Error: {error}")
#         time.sleep(5)

#endregion

models.Base.metadata.create_all(bind = engine)

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "hello there"}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db())):
    return {"message": "success"}

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
# @app.get('/posts/latest')
# def get_latest_post():
#     latest_post = my_posts[len(my_posts)-1]
#     return {'data': latest_post}


@app.get("/posts/{id}")
def get_post_by_id(id:int, response: Response):

    # NOTE -> id should be parsed to string when you give it to db
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()


    # post = find_post(id, my_posts)
    if not post:

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with this id: {id} was not found")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with this id {id} was not found"}

    return {'data': post}


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # index = find_index_post(id, my_posts)

    cursor.execute("""SELECT * FROM posts WHERE id = %S""", (str(id),))
    index = cursor.fetchone()
    conn.commit()


    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with this id {id} does not exists")

    # my_posts.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    # index = find_index_post(id , source = my_posts)

    cursor.execute("""UPDATE posts SET title = %s content = %s published = %s rating = %s WHERE id = %s RETURNING *""" ,
                   (post.title , post.content , post.published , post.rating, str(id),))
    index = cursor.fetchone()
    conn.commit()

    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with this id {id} does not exists")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {'data': index}