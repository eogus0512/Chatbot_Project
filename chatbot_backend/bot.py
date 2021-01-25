import threading
import json

from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer

#전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
                userdic='utils/user_dic.tsv')

def to_client(conn, addr, params):
    db = params['db']
    try:
        db.connect()

        read = conn.recv(2048) # 수신 데이터가 있을 때까지 블로킹
        print('==========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            print('클라이언트 연결 끊어짐')
            exit(0) #스레드 강제 종료

        #json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ",recv_json_data)
        query = recv_json_data['Query']

        #의도 파악
        intent = IntentModel(model_name='models/intent/intent_model.h5', proprocess=p)
        predict = intent.predict_class(query)
        intent_name = intent.labels[predict]

        #개체명 파악
        ner = NerModel(model_name='models/ner/ner_model.h5', proprocess=p)
        predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)

        #답변 검색
        try:
            if intent_name == "음식점추천" and ner_tags == None:
                answer = "해당 음식 맛집을 찾지 못했어요 ㅠㅠ 다른 음식을 입력해주세요"
                answer_image = ' '

            else:
                f = FindAnswer(db)
                answer_text, answer_image = f.search(intent_name, ner_tags, predicts)
                answer = f.tag_to_word(predicts, answer_text)
        
        except:
            answer = "죄송해요… 무슨 말씀이신지 모르겠어요…!!"
            answer_image = None

        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "NER" : str(predicts)
        }
        message = json.dumps(send_json_data_str) #json 객체를 전송 가능한 문자열로 변환
        conn.send(message.encode()) #응답 전송
    
    except Exception as ex:
        print(ex)
    
    finally:
        if db is not None: #db 연결 끊기
            db.close()
        conn.close()

if __name__ == '__main__':
    # 질문/ 답변 학습 db 연결 객체 생성
    db = Database(
        host="localhost", user="root", password="tjwjdeogus369!", db_name="food"
    )

    print("DB 접속")

    # 봇 서버 동작

    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db" : db
        }
        print(conn, addr)
        client = threading.Thread(target=to_client, args=(
            conn, #클라이언트 연결 소켓
            addr, #클라이언트 연결 주소 정보
            params 
        ))
        client.start() # 스레드 시작