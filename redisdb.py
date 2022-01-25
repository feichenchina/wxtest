import json

import redis
import requests


class RedisDb():
    def __init__(self):
        self.cache = redis.Redis(host="127.0.0.1", port=6379, db=1, decode_responses=True)
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):  # 发送请求得到access_token
        try:
            appId = 'wx273901140850eb09'
            appSecret = '97669578a44e3f18d8992bdf63454a95'
            getUrl = ("http://api.weixin.qq.com/cgi-bin/token?grant_type="
                       "client_credential&appid=%s&secret=%s" % (appId, appSecret))
            # urlResp = urllib.urlopen(postUrl).read()
            urlResp = requests.get(getUrl).content
            print("测试数据",urlResp)
            urlResp = json.loads(urlResp)
            self.__accessToken = urlResp['access_token']
            self.__leftTime = urlResp['expires_in']
        except Exception as e:
            print(e)

    def get_access_token(self):
        if self.__leftTime < 10:
            try:
                if self.cache.exists('access_token'):
                    self.__accessToken = self.cache.get('access_token')
                    if self.__accessToken:
                        self.__real_get_access_token()
                        self.cache.set('access_token', self.__accessToken, 60 * 60)
                else:
                    self.__real_get_access_token()
                    self.cache.set('access_token', self.__accessToken, 60 * 60)
            except Exception as e:
                print(e)
        return self.__accessToken