from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from typing import List

from .routers import post, user , auth , vote
from app.db.database import engine , metadata
from app.shared import settings

# NOTE: This should be here when you start the app it will run main.py so to create models
#! No longer need when you have alembic
# metadata.create_all(bind = engine)


# /doc => swagger
# /redoc => redoc

# Link: https://fastapi.tiangolo.com/how-to/configure-swagger-ui/
# Theme: obsidian
app = FastAPI(swagger_ui_parameters = {"syntaxHighlight.theme": "nord"})

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

@app.get('/')
async def root():
    return {"message": "hello there"}

