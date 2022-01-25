import asyncio
import hashlib
import time

import uvicorn
from fastapi import FastAPI, Body

from tasks import Menu, checkSignature

app = FastAPI()

@app.get("/")
def check(signature,timestamp,nonce,echostr):
    print("进入1343")
    temp = checkSignature(signature, timestamp, nonce)
    if temp:
        return int(echostr)
    else:
        return ""

@app.post("/")
def getData():
    # temp = checkSignature(signature, timestamp, nonce, echostr)
    temp= 123
    print("侧入式",temp)
    print("123",temp)
    resp_dict = {
        "xml": {
            'ToUserName': 123,
            'FromUserName': 123,
            'CreateTime': int(time.time()),
            'MsgType': 'text',
            'Content': 123,
        }
    }
    if temp:
        return resp_dict
    else:
        return ""


@app.get("/add_menu")
def addMenu():
    menu = Menu()
    menu.addMenu()
    return True

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
