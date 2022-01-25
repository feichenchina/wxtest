import hashlib
from urllib import parse

import requests

from redisdb import RedisDb


class Menu():
    def addMenu(self):
        data = {
     "button":[
     {
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
           {
               "type":"view",
               "name":"搜索",
               "url":"http://www.soso.com/"
            },
            {
                 "type":"miniprogram",
                 "name":"wxa",
                 "url":"http://mp.weixin.qq.com",
                 "appid":"wx286b93c14bbf93aa",
                 "pagepath":"pages/lunar/index"
             },
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"V1001_GOOD"
            }]
       }]
 }
        cache = RedisDb()
        ACCESS_TOKEN = cache.get_access_token()
        print("tocken",ACCESS_TOKEN)
        url = f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={ACCESS_TOKEN}"
        response = requests.post(url,data=data).content
        print(response)


def checkSignature(signature,timestamp,nonce):
    token = 'syn2022'
    # HE22MiDJvLib7EVAsE6wxfKXY5ZS6Z2m0g3L2ZDOAoi
    check_list = [token, timestamp, nonce]
    check_list.sort()
    s1 = hashlib.sha1()
    s1.update(''.join(check_list).encode())
    hashcode = s1.hexdigest()
    if hashcode == signature:
        return True
    else:
        return False


def qingyunke(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]
