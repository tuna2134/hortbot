from logging import Handler
import aiohttp

class Discord_logging(Handler):
    def __init__(self, loop, webhook_url:str):
        self.url = webhook_url
        self.loop = loop
        
    def emit(self, record):
        self.loop.create_task(self.aemit(record))

    def to_dict(self, msg):
        data = {
            "embed": {
                "title": "logging",
                "description": msg
            }
        }
        return data

    async def aemit(self, record):
        msg = self.format(record)
        if len(msg) >= 1900:
            msg_list = [msg[i: i+1900] for i in range(0, len(msg), 1900)]
            for mg in msg_list:
                data = self.to_dict(msg)
                async with aiohttp.request("POST", self.url, data = data):
                    pass
        else:
            data = self.to_dict(msg)
            async with aiohttp.request("POST", self.url, data = data):
                pass