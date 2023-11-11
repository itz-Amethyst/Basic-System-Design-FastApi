from fastapi import FastAPI

# from typing import List

from .routers import post, user , auth , vote
from app.db.database import engine , metadata

# NOTE: This should be here when you start the app it will run main.py so to create models
metadata.create_all(bind = engine)


# /doc => swagger
# /redoc => redoc

# Link: https://fastapi.tiangolo.com/how-to/configure-swagger-ui/
# Theme: obsidian
app = FastAPI(swagger_ui_parameters = {"syntaxHighlight.theme": "nord"})
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {"message": "hello there"}

