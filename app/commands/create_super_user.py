import asyncclick as click
from pydantic import EmailStr
from fastapi import Request

from app.db.models.user import RoleOptions
from app.managers.user import UserManager


#! Need to work on it
@click.command()
@click.option("-e", "--email", type=str, required = True)
@click.option("-p", "--password", type=str, required = True)
@click.option("-r", "--role", type=RoleOptions, required = True)
async def create_user(email: EmailStr, password: str, role: RoleOptions):

    user_data = {"email": email, "password": password, "role": RoleOptions.value, "profile_picture": "https://cdn.discordapp.com/attachments/921633563810627588/1175350979202400267/image.png?ex=656ae9e6&is=655874e6&hm=002a637e7bcbf71940f99b778a16e15f6d7487ddd05d11be3020bf04eebae2e0&"}

    await UserManager.register(user_data = user_data , request = Request)




if __name__ == "__main__":
    create_user(_anyio_backend = "asyncio")