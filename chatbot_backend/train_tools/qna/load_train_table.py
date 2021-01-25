import pymysql
import openpyxl


# 학습 데이터 초기화
def all_clear_train_data(db):
    # 기존 학습 데이터 삭제
    sql = '''
            delete from train_table
        '''
    with db.cursor() as cursor:
        cursor.execute(sql)

    # auto increment 초기화
    sql = '''
    ALTER TABLE train_table AUTO_INCREMENT=1
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)


# db에 데이터 저장
def insert_data(db, xls_row):
    intent, ner, food, answer, answer_img_url = xls_row

    sql = '''
        INSERT train_table(intent, ner, food, answer, answer_image) 
        values(
         '%s', '%s', '%s', '%s', '%s'
        )
    ''' % (intent.value, ner.value, food.value, answer.value, answer_img_url.value)

    # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
    sql = sql.replace("'None'", "null")

    with db.cursor() as cursor:
        cursor.execute(sql)
        print('{} 저장'.format(food.value))
        db.commit()


train_file = 'C:/Users/ghk78/WORKSPACE/github/Chatbot_API/Chatbot_Project/train_tools/qna/train_data.xlsx'
db = None
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        passwd="tjwjdeogus369!",
        db="food",
        charset='utf8'
    )

    # 기존 학습 데이터 초기화
    all_clear_train_data(db)

    # 학습 엑셀 파일 불러오기
    wb = openpyxl.load_workbook(train_file)
    sheet = wb['Sheet1']
    for row in sheet.iter_rows(min_row=2): # 해더는 불러오지 않음
        # 데이터 저장
        insert_data(db, row)

    wb.close()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()