from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import importlib

from starlette.middleware.sessions import SessionMiddleware

from .routers import post, user , auth , vote , orm , upload
from app.db.database import engine , metadata

#? Let it be here to work
from app.shared import logger , redis
from app.shared import settings
from app.shared.logger import logger_system


from utils.RateLimiter import rate_limited
# NOTE: This should be here when you start the app it will run main.py so to create models
#! No longer need when you have alembic
# metadata.create_all(bind = engine)


# /doc => swagger
# /redoc => redoc

# Link: https://fastapi.tiangolo.com/how-to/configure-swagger-ui/
# Theme: obsidian
app = FastAPI(swagger_ui_parameters = {"syntaxHighlight.theme": "nord"})
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


#? Admin: https://github.com/fastapi-admin/fastapi-admin this one only works with tortoise orm only
# ? Admin: More like a django admin default https://piccolo-admin.readthedocs.io/en/latest/installation/index.html


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # You can use this or otherwise use * to allow all
        # allow_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS] ,
        allow_origins = settings.BACKEND_CORS_ORIGINS,
        allow_credentials = True ,
        allow_methods = ["*"] ,
        allow_headers = ["*"] ,
    )


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(orm.router)
app.include_router(upload.router)

#! Never ever use fastapi-crudrouter not available in sqlalchemy Base Version



#* Note: Conflict when activate both of them in same time
# V1
@app.on_event('startup')
def startup():
    if redis.ping():
        logger_system.info("Connected to redis: Pong")
    admin_module = importlib.import_module('app.admin')
    admin_module.admin.mount_to(app)


# V2
# @app.on_event('startup')
# def startup():
#     admin_module = importlib.import_module('app.sqladmin')



@app.get('/')
#! 10 requests in 60 seconds
@rate_limited(max_calls = 10, time_frame = 60)
async def root():
    return {"message": "hello there"}

