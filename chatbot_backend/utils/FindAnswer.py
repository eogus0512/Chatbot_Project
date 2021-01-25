class FindAnswer:
    def __init__(self, db):
        self.db = db

    # 검색 쿼리 생성
    def _make_query(self, intent_name, ner_tags, ner_predicts):
        sql = "select * from train_table"
        if intent_name != None and ner_tags == None:
            sql = sql + " where intent='{}' ".format(intent_name)

        elif intent_name != None and ner_tags != None:
            where = ' where intent="%s" ' % intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
                for word, tag in ner_predicts:
                    if tag == 'B_FOOD':
                        where += " and ( food like '%{}%' )".format(word)

            sql = sql + where

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        return sql

    # 답변 검색
    def search(self, intent_name, ner_tags, ner_predicts):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags, ner_predicts)
        answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            if intent_name == '음식점추천':
                answer['answer'] = "해당 음식 맛집을 찾지 못했어요 ㅠㅠ 다른 음식을 입력해주세요"
                answer['answer_image'] = ' '
            else:
                sql = self._make_query(intent_name, None, None)
                answer = self.db.select_one(sql)

        return (answer['answer'], answer['answer_image'])

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_FOOD':
                answer = answer.replace(tag, word)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
