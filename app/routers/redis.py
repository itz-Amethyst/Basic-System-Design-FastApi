
from fastapi import APIRouter, Response, HTTPException
from pydantic import EmailStr
from redis.commands.search.field import TextField , TagField , NumericField
from redis.commands.search.indexDefinition import IndexDefinition , IndexType
from redis.commands.json.path import Path
from starlette import status

from app.db.redis import redis

router = APIRouter(
    tags = ['Redis'],
    prefix = '/redis'
)

user1 = {
    "name": "Paul John",
    "email": "paul.john@example.com",
    "age": 42,
    "city": "London"
}
user2 = {
    "name": "Eden Zamir",
    "email": "eden.zamir@example.com",
    "age": 29,
    "city": "Tel Aviv"
}
user3 = {
    "name": "Paul Zamir",
    "email": "paul.zamir@example.com",
    "age": 35,
    "city": "Tel Aviv"
}

schema = (
    TextField("$.name", as_name="name"),
    TagField("$.city", as_name="city"),
    NumericField("$.age", as_name="age")
)

@router.get('/')
def test():
    redis.set('foo', 'bar')

    us = redis.ft('idx:users')
    us.create_index(
        schema,
        definition = IndexDefinition(
            prefix = ["user:"], index_type = IndexType.JSON
        )
    )

    redis.json().set("user:1", Path.root_path(), user1)
    redis.json().set("user:2", Path.root_path(), user2)
    redis.json().set("user:3", Path.root_path(), user3)

    redis.hset('user:', mapping = {
        'email': 'test@gmail.com',
        'password': '123'
    })


    redis.hset('user-session123', mapping = {
        'name': 'test',
        'role': 'god',
        'age': 12
    })
    # print(redis.get('foo'))
    print(redis.hgetall('user-session123'))
    return Response(content = f"{redis.hgetall('user-session123')}", status_code = 200)


@router.post('/register')
def register_user(email: EmailStr, password: str):

    # You can put try catch if you want
    user_key = f'User:{email}'
    if redis.exists(user_key):
        return HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "User already registered")


    user_data = {
        'email': email ,
        'password': password
    }
    redis.hmset(user_key , user_data)

    return {"message": "Registration successful"}

@router.post('/login')
def login_user(email: EmailStr, password: str):
    user_key = f'User:{email}'
    stored_user_data = redis.hgetall(user_key)
    stored_password = stored_user_data.get(b'password' , b'').decode('utf-8')

    if not stored_user_data or password != stored_password:
        return HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Invalid Credentials")

    # stored_password = stored_user_data['password']

    return {"message": "Login successful"}