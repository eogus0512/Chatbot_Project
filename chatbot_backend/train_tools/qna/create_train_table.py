import pymysql

db = None
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        passwd="tjwjdeogus369!",
        db="food",
        charset='utf8'
    )

    # 테이블 생성 sql 정의
    sql = '''
      CREATE TABLE IF NOT EXISTS `train_table` (
      id INT UNSIGNED NOT NULL AUTO_INCREMENT,
      intent VARCHAR(45) NULL,
      ner VARCHAR(1024) NULL,
      food TEXT NULL,
      answer TEXT NOT NULL,
      answer_image VARCHAR(2048) NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB DEFAULT CHARSET=utf8
    '''

    # 테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
