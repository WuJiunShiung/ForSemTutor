# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 12:15:34 2021

@author: Admin
"""

from ForSemTutor import *
from intent.Loki_Basics import userDefinedDICT

termDICT = {'lambda':'帶領一個可以用詞代入的變數，用法：lambda x [P(x)',
            '全稱量詞': '帶領一個變數，是全部的意思，用法：forAll x [P(x)->Q(x[)]',
            '存在量詞':'帶領一個變數，是有一個的意思，用法：thereIs x [P(x) and Q(x)]',
            '專有名詞':"指涉叫那個名詞個體，用那個專有名詞來代表其語意",
            '普通名詞':"具該名詞性質的個體所成之群組，用：lambda x [名詞(x)]來表示",
            '及物動詞':"需要一個承受動作實體及一個執行動作實體的動作，寫成：lambda x lambda y [P(y, x)]",
            '不及物動詞':"只需要一個執行動作的實體的動作，寫成：lambda x [P(x)]",
            '謂語形容詞':'需要一個被談論的實體當主語的形容詞，寫成：lambda x [Adj(x)]',
            '屬性形容詞':'修飾普通名詞的形容詞，寫成：lambda N lambda y [N(y) and Adj(y)]'}

vpComp = """及物動詞：用代表承受動作的實體取代第一個 lambda 引領的變數，
假設這個實體用"實體2"來表示，那就是：把 lambda x lambda y [P(y, x)]
變成 lambda y [P(y, 實體2]；
不及物動詞：直接變成動詞短語，這種動詞短語的語意等於不及物動詞語意。
"""

npComp = """專有名詞直接變成名詞短語，兩者語意相等，也就是專有名詞形成的
名詞短語，語意就是專有名詞指涉的實體
"""         

sComp = """句子的語意由主語及動詞短語組合而成；由代表主語的實體取代動詞短語
中的 lambda 引領的變數，如主詞寫為：實體1，動詞短語的語意 lambda y [P(y, 實體2)]
變為：[P(實體1, 實體2)]
"""         

#sent = input('請輸入你的形式語意的問題：\n')
#resultDICT = runLoki([sent], [])

def askQuestion(resultDICT):
    if resultDICT['action'] == 'DefineTerm':
        if resultDICT['term'] not in userDefinedDICT:
            for key in userDefinedDICT:
                if resultDICT['term'] in userDefinedDICT[key]:
                    query = key
                    break    
        else:
            query = resultDICT['term']
   
        if query == '動詞':
            query = input('請問是及物動詞還是不及物動詞？\n')
            if query =='及物':
                query = '及物動詞'
            elif query == '不及物':
                query = '不及物動詞'
            else:
                query = query
            
        elif query == '名詞':
            query = input("請問是專有名詞還是普通名詞？\n")
            if query == '普通':
                query = '普通名詞'
            elif query == '專有':
                query = '專有名詞'
            elif query == '專名':
                query = '專有名詞'
        elif query == '形容詞':
            query = input('請問是謂語形容詞還是屬性形容詞？\n')
            if query == "謂語":
                query = "謂語形容詞"
            elif query == "屬性":
                query = "屬性形容詞"
    
        print()
        print(f"{query}的語意是：\n{termDICT[query]}")
    
    elif resultDICT['action'] == 'comp':
        print()
        if resultDICT['term'] == '句子':
            print(sComp)
        elif resultDICT['term'] == '動詞':
            print(vpComp)
        elif resultDICT['term'] == '名詞':
            print(npComp)
        

if __name__ == "__main__":
    sents = ['動詞的語意是什麼', '什麼是存在量詞的語意', '名詞的意思是什麼', 
             '形容詞是幹什麼的', '名詞短語的意思是什麼', '句子的語意是什麼']
    for sent in sents:
        resultDICT = runLoki([sent], [])
        askQuestion(resultDICT)
        print()