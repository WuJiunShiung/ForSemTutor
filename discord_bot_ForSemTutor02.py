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

logging.basicConfig(level=logging.CRITICAL)

# 取得多輪對話資訊

client = discord.Client()

templateDICT = {"term":None,
                "action":None,
                "type":None}

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

@client.event
async def on_ready():
    logging.info("[READY INFO] {} has connected to Discord!".format(client.user))
    print("[READY INFO] {} has connected to Discord!".format(client.user))
    
@client.event

async def on_message(message):
    if not re.search("<@[!&]{}> ?".format(client.user.id), message.content):    
        # 只有 @Bot 才會回應
        return

    if message.author == client.user:
        return
    
    # Greetings
    print("client.user.id =", client.user.id, "\nmessage.content =", message.content)
    msgSTR = re.sub("<@[!&]{}> ?".format(client.user.id), "", message.content)    # 收到 User 的訊息，將 id 取代成 ""
    logging.info(msgSTR)
    #print("msgSTR =", msgSTR)
    replySTR = ""    # Bot 回應訊息
    
    if msgSTR in ("","哈囉","嗨","嗨嗨","你好","您好","在嗎","Hi","hi","hello","Hello","安安"):
        replySTR = "有什麼形式語意的問題嗎？我可以幫你！"
        await message.reply(replySTR)
        
    else:
        lokiResultDICT=getLokiResult(msgSTR)    # 取得 Loki 回傳結果
        print(lokiResultDICT)
        
        if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
            mscDICT[client.user.id] = {"term":'',
                                       "action":'',
                                       "type":'',
                                       "completed": False,
                                       "updatetime": datetime.datetime.now()}
            
        # 處理時間差
        datetimeNow = datetime.datetime.now()  # 取得當下時間
        timeDIFF = datetimeNow - mscDICT[client.user.id]["updatetime"]
        if timeDIFF.total_seconds() <= 300:    # 以秒為單位，5分鐘以內都算是舊對話
            mscDICT[client.user.id]["updatetime"] = datetimeNow 
            
        # 清空templateDICT還沒做，得想想清空的時機
            
        
         #多輪對話
        if lokiResultDICT:
            for k in lokiResultDICT:    # 將 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
                if k == "term":
                    mscDICT[client.user.id]["term"] = lokiResultDICT["term"]
                elif k == "action":
                    mscDICT[client.user.id]["action"] = lokiResultDICT["action"]
                
        print("mscDICT =")
        pprint(mscDICT)
 
        if mscDICT[client.user.id]["term"] == "":  # 多輪對話的問句。
            replySTR = '請問，你想問什麼形式語意的問題呢？'
            
        elif mscDICT[client.user.id]['action'] == "DefineTerm":
            if mscDICT[client.user.id]['term'] not in userDefinedDICT:
                for key in userDefinedDICT:
                    if mscDICT[client.user.id]['term'] in userDefinedDICT[key]:
                        query = mscDICT['client.user.id']['term']
                
                if querry  == "動詞":
                    replySTR = '請問是及物動詞還是不及物動詞？'
                    