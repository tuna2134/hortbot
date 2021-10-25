from discord.ext import commands
from sanic import Sanic
from sanic.exceptions import SanicException
import discord
from sanic.log import logger
from jinja2 import Environment, FileSystemLoader
from sanic.response import html
import os
import aiomysql
from inspect import getmembers
import time
from functools import wraps
from module.web_manager import web_manager
from flask_misaka import Misaka
import aiohttp
import ujson

dbword = os.getenv("db_password")

class HortBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.web_manager = web_manager()
        self.app = Sanic("hortbot")
        self.app.static('/static', './static')
        self.app.register_listener(self.setup,"main_process_start")
        self.app.register_listener(self.setout, "before_server_stop")
        self._env = Environment(loader=FileSystemLoader('./templates/', encoding='utf8'), enable_async=True)
        self._env.filters.setdefault("markdown", Misaka(autolink=True, wrap=True).render)
        self.__args = args
        self.__kwargs = kwargs
        commands.route = self.route
        self.data = {}
        commands.web_cooldown = self.cooldown
        self._slash = {}
        self.ws_list = []

    async def send_ws(self, data):
        for ws in self.ws_list:
            await ws.send(ujson.dumps(data))
        
    async def template(self, filename, **kwargs):
        template = self._env.get_template(filename)
        content = await template.render_async(kwargs)
        #print(content)
        return html(content)
        
    async def setup(self, app, loop):
        self.pool = await aiomysql.create_pool(host="public-cbsv1.net.rikusutep.xyz", user="dms", password=dbword, loop=loop, db="b3vad_", autocommit=True)
        self.session = aiohttp.ClientSession(loop=loop)
        self.db = await self.pool.acquire()
        super().__init__(*self.__args, **self.__kwargs)
        loop.create_task(self.start(self.token, reconnect=self.reconnect))
        await self.wait_until_ready()
        logger.info("Bot is starting...")
        
    async def setout(self, app, loop):
        self.db.close()
        await self.close()
        
    def run(self, token, reconnect:bool=True, *args, **kwargs):
        self.token = token
        self.reconnect = reconnect
        self.app.run(*args, **kwargs)
        
    @property
    def web(self):
        return self.app
    
    def route(self, *args, **kwargs):
        def decoreator(coro):
            coro._route = args
            return coro
        return decoreator

    def slash(self, name):
        def deco(coro):
            self.slash[name] = coro
        return deco
        
    def cooldown(self, time_:float):
        def deco(coro):
            @warps(coro)
            async def request(self, request, *args, **kwargs):
                if self.web_manager.cooldown(request, time_):
                    raise SanicException("リクエストのしすぎです", 429)
                else:
                    return await coro(self, request, *args, **kwargs)
        
before = commands.Cog._inject
        
def new(self, bot, *args, **kwargs):
    for n, coro in getmembers(self):
         if hasattr(coro, "_route"):
             bot.web.add_route(coro, *coro._route)
    return before(self, bot)
commands.Cog._inject=new