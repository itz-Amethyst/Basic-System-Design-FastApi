from fastapi import FastAPI

# from typing import List

from .routers import post, user , auth



# /doc => swagger
# /redoc => redoc

# Link: https://fastapi.tiangolo.com/how-to/configure-swagger-ui/
# Theme: obsidian
app = FastAPI(swagger_ui_parameters = {"syntaxHighlight.theme": "nord"})
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {"message": "hello there"}

