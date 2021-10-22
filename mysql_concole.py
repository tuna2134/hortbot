import aiomysql
import os
import asyncio
import time

dbword = os.getenv("db_password")

async def main():
    print("MySQLコンソールシステム")
    while True:
        print("コマンドを入力してください")
        cmd = input(">>")
        async with aiomysql.connect(host="public-cbsv1.net.rikusutep.xyz", user="dms", password=dbword, loop=loop, db="b3vad_", autocommit=True) as conn:
            async with conn.cursor() as c:
                #await c.execute("INSERT INTO captcha_url VALUES(%s,%s,%s)",("aaa", 9999999, time.time()))
                await c.execute(cmd)
                if cmd.upper().startswith("SELECT"):
                    print(await c.fetchall())
                    
loop = asyncio.get_event_loop() 
loop.run_until_complete(main())