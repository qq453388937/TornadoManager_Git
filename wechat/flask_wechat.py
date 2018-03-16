import hashlib

from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/wechat8027', methods=['POST', 'GET'])
def wechat():
    # 获取参数
    data = request.args
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')

    # 对参数进行字典排序,拼接字符串
    temp = [timestamp, nonce, echostr]
    temp.sort()
    temp = ''.join(temp)

    # 加密
    if hashlib.sha1(temp).hexdigest() == signature:
        return make_response(echostr)
    else:
        return 'error', 403


if __name__ == '__main__':
    app.run(port=8027)
