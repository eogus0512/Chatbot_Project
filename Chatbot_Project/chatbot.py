from utils.Database import Database
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer
from tkinter import *
# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

# 질문/답변 학습 디비 연결 객체 생성
db = Database(
    host="localhost", user="root", password="0000", db_name="food"
)
db.connect()    # 디비 연결

def sendMessage():
    query = input.get(1.0, END)
    input.delete(1.0, END)
    messageLog.configure(state="normal")
    messageLog.insert(END, "\n\nUSER : "+query)
    messageLog.configure(state="disabled")

    intent = IntentModel(model_name='models/intent/intent_model.h5', proprocess=p)
    predict = intent.predict_class(query)
    intent_name = intent.labels[predict]

    ner = NerModel(model_name='models/ner/ner_model.h5', proprocess=p)
    predicts = ner.predict(query)
    ner_tags = ner.predict_tags(query)

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
        answer_image = " "

    messageLog.configure(state="normal")
    messageLog.insert(END, "\n\nChatbot : " + answer + "\n" + answer_image)
    messageLog.configure(state="disabled")

tk = Tk()

tk.title("동국대학교 맛집추천 챗봇")
tk.geometry("692x600")
tk.option_add("*Font", "맑은고딕 10")

masterFrame = Frame(tk)
masterFrame.pack(fill=X)

frame = Frame(masterFrame, background="orange")
image = PhotoImage(file='SideBar.png')
label = Label(masterFrame, image=image)
label.pack(side=LEFT)

frame1 = Frame(masterFrame)
frame1.pack(fill=X)

messageLog = Text(frame1)
scrollbar = Scrollbar(frame1, command=messageLog.yview)
messageLog.configure(width=70, height=40, state="disabled", yscrollcommand=scrollbar.set)
messageLog.grid()
scrollbar.grid(row=0, column=1, sticky='ns')
messageLog.configure(state="normal")
messageLog.insert(END, "Chatbot : 동국대학교 주변 맛집을 찾아주는 챗봇입니다.\n어떤 음식을 먹을지 고민되거나 해당 음식에 대한 "
                       "맛집을 추천받고 싶다면 자유롭게 질문해 주세요!\n")
messageLog.configure(state="disabled")

frame2 = Frame(masterFrame)
frame2.pack(fill=X)
input = Text(frame2, width=63, height=5)
input.pack(side=LEFT)
send = Button(frame2, text="보내기", width=7, height=5, command=sendMessage, background="LightCyan")
send.pack(side=RIGHT)


tk.mainloop()
