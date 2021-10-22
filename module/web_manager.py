from sanic import exceptions
import time

class web_manager:
    def __init__(self):
        self.data = {}
        
    def cooldown(self, request, time_):
        ip = request.ip
        if ip in self.data:
            if round(time.time() - self.data[ip]) < time_:
                return True
            else:
                self.data[ip] = time.time()
                return False
        else:
            self.data[ip] = time.time()
            return False