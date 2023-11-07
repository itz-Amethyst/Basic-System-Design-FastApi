from fastapi import FastAPI


# from typing import List

from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind = engine)

# /doc => swagger
# /redoc => redoc

# Link: https://fastapi.tiangolo.com/how-to/configure-swagger-ui/
# Theme: obsidian
app = FastAPI(swagger_ui_parameters = {"syntaxHighlight.theme": "nord"})
app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
async def root():
    return {"message": "hello there"}

