from hashlib import sha3_256

from fastapi import Depends, Request

from app.managers.auth import oauth2_password , AuthManager
from app.shared.errors import credentials_exception, rate_limited
from app.db.redis import rate_limit_get, rate_limit_set


# Check if user is logged in
def user_required( token: str = Depends(oauth2_password) ):
    return AuthManager.verify_access_token(token , credentials_exception)


def get_ip():
    async def decorator(request: Request):
        forwarded = request.headers.get('X-Forwarded-For')

        if forwarded:
            ip = forwarded.split(',')[0]
        else:
            ip = request.client.host

        request.state.ip = ip

        return ip

    return Depends(decorator)

#! Work on this
async def rate_limit(request, path_id):
    period = 3600
    amount = 10

    ip = request.state.ip
    identifier = sha3_256(f'{path_id}:{ip}'.encode('utf-8')).hexdigest()
    key = f'invalid_token:{identifier}'

    value, expire = await rate_limit_get(key)

    if value >= amount:
        raise rate_limited(headers={
            'X-RateLimit-Limit': str(amount),
            'X-RateLimit-Reset-After': str(expire)
        })

    await rate_limit_set(key, period)

#? Shorter version
# def get_ip():
#     async def decorator( request: Request ):
#         ip = request.headers.get('X-Forwarded-For' , request.client.host).split(',')[0]
#         request.state.ip = ip
#         return ip
#
#     return Depends(decorator)