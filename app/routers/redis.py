from math import inf

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


class UserData:
    def __init__(self, data):
        self._data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}

    def __getattr__(self, name):
        return self._data.get(name, '')

    def __getitem__(self, name):
        return self._data.get(name, '')


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
range_table_name = 'UserLogins_count'


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
    redis.hset(user_key , user_data)

    return {"message": "Registration successful"}

@router.post('/login')
def login_user(email: EmailStr, password: str):
    user_key = f'User:{email}'
    # stored_user_data = redis.hgetall(user_key)

    #region mess
    # stored_password = stored_user_data.get(b'password' , b'').decode('utf-8')
    # lock_acc = stored_user_data.get(b'lock_account' , b'').decode('utf-8')
    #endregion

    user_data = UserData(redis.hgetall(user_key))


    if not user_data or password != user_data.password:
        return HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Invalid Credentials")

    if user_data.lock_account == 'True':
        return HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Your account has been locked due multiple login")

    # Increase login count
    redis.zincrby(name = range_table_name,amount = 1,  value = str({user_key}))

    # stored_password = stored_user_data['password']

    return {"message": "Login successful"}

@router.get('/get_logins_count')
def get_user_logins_count():
    #! ordering asc / des

    # data = redis.zrange('UserLogins_count', start = 0, end = -1)
    data = redis.zrevrange(range_table_name, start = 0, end = -1, withscores = True)

    #? get UserLogins_count and check if it was greater than 10 lock the account
    locked_user = redis.zrangebyscore(range_table_name, min = 5, max = +inf)

    for user_key_bytes in locked_user:
        user_key = user_key_bytes.decode('utf-8')  # Convert bytes to string
        # user_key = ast.literal_eval(user_key)
        user_key = user_key.strip("'{}'")
        user_data = redis.hgetall(user_key)

        # Check if the user_data contains the 'lock_field' key
        if b'lock_field' not in user_data:
            # Set the 'lock_field' to True for the user
            redis.hset(user_key , 'lock_account' , 'True')



    return {"message": data}

