from flask import Flask, request, abort
from wechatpy import parse_message
from wechatpy.replies import create_reply
from tasks import checkSignature, qingyunke

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wechat():
    # 获取参数
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    # 校验参数
    if not all([signature, timestamp, nonce]):  # echostr
        abort(400)
    sigin = checkSignature(signature, timestamp, nonce)
    # 签名值对比，相同证明请求来自微信
    # 错误返回403页面
    if not sigin:
        abort(403)
    else:
        # 正确返回echostr字符串
        # 表示是微信请求
        if request.method == 'GET':
            # 第一次接入服务器
            echostr = request.args.get('echostr')
            if not echostr:
                abort(403)
            else:
                return echostr
        elif request.method == 'POST':
            # 表示微信服务器转发消息到本地服务器
            xml_str = request.data
            if not xml_str:
                return abort(403)
            msg = parse_message(xml_str)
            print( msg.type == "text")
            if msg.type == "text":
                response = qingyunke(msg.content)
                print(response)
                reply = create_reply(response, message=msg)
                # 转换成 XML
                resp_xml_str = reply.render()
            else:
                reply = create_reply('我们收到您的消息，谢谢您', message=msg)
                # 转换成 XML
                resp_xml_str = reply.render()
            # # 返回消息字符串
            return resp_xml_str


if __name__ == '__main__':
    app.run(port=80, debug=True)





