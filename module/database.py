import aiomysql
import os

dbword = os.getenv("db_password")

class database:
    def __init__(self, loop):
        self.loop = loop
        
    async def __aenter__(self):
        self.__conn = await aiomysql.connect(host="public-cbsv1.net.rikusutep.xyz", user="dms", password=dbword, loop=self.loop)
        return self.__conn
        
    async def __aexit__(self, exc_type, exc, tb):
        self.__conn.close()