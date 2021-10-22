import aiohttp
from functools import wraps
from sanic.response import redirect
import os

baseurl = "https://discord.com/api/v9"


class User:
    def __init__(self, data):
        self.data = data
        
    @property
    def id(self):
        return self.data["id"]
    
    @property
    def name(self):
        return self.data["username"]

class Oauth:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v8"
        self.client_secret = os.getenv("client_secret")
        
    async def callback(self, request):
        code=request.args.get("code")
        _id = request.args.get("state")
        data = {
            "client_id": "829986743331586048",
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https://hortbot.f5.si/verify/callback"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.baseurl+"/oauth2/token", data=data, headers=headers) as r:
                res = redirect(f"/verify/{_id}")
                api = await r.json()
                token = api["access_token"]
                res.cookies["token"]=token
                return res
                
    async def get_user(self, request):
        token = request.cookies.get("token")
        headers={
            "Authorization": "Bearer {}".format(token)
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.baseurl+"/users/@me", headers=headers) as response:
                return await response.json()
                
    def authorized(self):
        def decorator(f):
            @wraps(f)
            async def authed(request, *args, **kwargs):
                user=await Oauth().get_user(request.cookies.get("token"))
                if user.id:
                    response = await f(request, user, *args, **kwargs)
                    return response
                else:
                    redirect("/login")
            return authed
        return decorator