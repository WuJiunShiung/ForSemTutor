#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import logging
import discord
import re
import datetime

from ForSemTutor import *
from intent.Loki_Basics import userDefinedDICT
from pprint import pprint

logging.basicConfig(level=logging.INFO)

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())

DISCORD_TOKEN=accountDICT["discord_token"]

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

#多輪對話資訊
templateDICT = {"term":None,
                "action":None,
                "type":None,
                #"completed":False,
                "time":datetime.datetime.now()}

mscDICT = {
    # "userID":{templateDICT}
    }

punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")

def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Loki Result => {}".format(resultDICT))
    return resultDICT

class BotClient(discord.Client):
    def getNewConversationTemplate(self):
        #多輪對話資訊：對話完成後，就再重新呼叫一次 getNewConversationTemplate() 以便把該使用者的前一輪對話資訊清空。
        templateDICT = {"term":None,
                        "action":None,
                        "type":None,
                        "completed":False,
                        "time":datetime.datetime.now()}
        return templateDICT

    async def on_ready(self):
        print('Logged on as {} with id {}'.format(self.user, self.user.id))


    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        print("收到來自 {} 的訊息".format(message.author))
        print("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            print("本 bot 被叫到了！")
            msgSTR = message.content.replace("<@!{}> ".format(self.user.id), "")
            if msgSTR == 'ping':
                await message.reply('pong')
            elif msgSTR == 'ping ping':
                await message.reply('pong pong')
            elif msgSTR in ("","哈囉","嗨","嗨嗨","你好","您好","在嗎","Hi","hi","hello","Hello","安安"):
                replySTR = "有什麼形式語意的問題嗎？我可以幫你！"
                await message.reply(replySTR)
            else:
                lokiResultDICT=getLokiResult(msgSTR)    # 取得 Loki 回傳結果
                print(lokiResultDICT)

                if message.author not in mscDICT:    # 判斷 User 是否為第一輪對話
                    mscDICT[message.author] = templateDICT

                # 處理時間差
                datetimeNow = datetime.datetime.now()  # 取得當下時間
                timeDIFF = datetimeNow - mscDICT[message.author]["time"]
                if timeDIFF.total_seconds() <= 300:    # 以秒為單位，5分鐘以內都算是舊對話
                    mscDICT[message.author]["time"] = datetimeNow


                #多輪對話
                if lokiResultDICT:
                    for k in lokiResultDICT:    # 將 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
                        if k == "term":
                            mscDICT[message.author]["term"] = lokiResultDICT["term"]
                        if k == "action":
                            mscDICT[message.author]["action"] = lokiResultDICT["action"]
                        elif k == "type":
                            mscDICT[message.author]['type'] = lokiResultDICT["type"]

                print("mscDICT =")
                pprint(mscDICT)

                if mscDICT[message.author]["term"] == None:  # 多輪對話的問句。
                    replySTR = '請問，你想問什麼形式語意的問題呢？'
                    await message.reply(replySTR)

                elif mscDICT[message.author]['action'] == "DefineTerm" and mscDICT[message.author]['type']==None:
                    if mscDICT[message.author]['term'] not in userDefinedDICT:
                        for key in userDefinedDICT:
                            if mscDICT[message.author]['term'] in userDefinedDICT[key]:
                                query = mscDICT[message.author]['term']
                    else:
                        query = mscDICT[message.author]['term']

                    if query  == "動詞":
                        replySTR = '請問是及物動詞還是不及物動詞？'
                        await message.reply(replySTR)

                    elif query == "名詞":
                        replySTR = "請問是專有名詞還是普通名詞？"
                        await message.reply(replySTR)

                    elif query == '形容詞':
                        replySTR = '請問是謂語形容詞還是屬性形容詞？'
                        await message.reply(replySTR)


                elif mscDICT[message.author]['action'] == "comp":
                    if mscDICT[message.author]['term'] == "句子":
                        await message.reply(sComp)
                    elif mscDICT[message.author]['term'] == "動詞":
                        await message.reply(vpComp)
                    elif mscDICT[message.author]['term'] == "名詞":
                        await message.reply(npComp)


                elif mscDICT[message.author]['action'] == "DefineTerm" and mscDICT[message.author]['type']:
                    query = mscDICT[message.author]['type']
                    replySTR = f"{query}的語意是：{termDICT[query]}"

                del mscDICT[message.author]


if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])


