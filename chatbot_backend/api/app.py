from flask import Flask, request, jsonify, abort
import socket
import json
from flask_cors import CORS, cross_origin

#챗봇 엔진 서버 접속 정보
host = "127.0.0.1"
port = 5050

app = Flask(__name__)

#챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    #챗봇 엔진 서버 연결
    myApiSocket = socket.socket()
    myApiSocket.connect((host, port))

    #챗봇 엔진 질의 요청
    json_data = {
        'Query': query,
        'BotType': "MyService"
    }
    print(json_data)
    message = json.dumps(json_data)
    myApiSocket.send(message.encode())

    #챗봇 엔진 답변 출력
    data = myApiSocket.recv(2048).decode()
    ret_data = json.loads(data)

    print("socket 확인")
    #챗봇 엔진 서버 연결 소켓 닫기
    myApiSocket.close()
    print(ret_data)
    return ret_data

@app.route('/query/<bot_type>', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def query(bot_type):
    print("왜안돼")
    body = request.get_json()
    print(bot_type)

    try:
        if bot_type == 'TEST':
            #챗봇 API 테스트
            print("여긴")
            print(body['query'])
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)

        else:
            # 정의되지 않은 bot type 인 경우 404 오류
            abort(404)

    except Exception as ex:
        print(ex)
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)