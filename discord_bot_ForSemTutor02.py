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

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
    
DISCORD_TOKEN=accountDICT["discord_token"]

# 取得多輪對話資訊

client = discord.Client()

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
            mscDICT[client.user.id] = templateDICT
            
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
                if k == "action":
                    mscDICT[client.user.id]["action"] = lokiResultDICT["action"]
                elif k == "type":
                    mscDICT[client.user.id]['type'] = lokiResultDICT["type"]
                
        print("mscDICT =")
        pprint(mscDICT)
 
        if mscDICT[client.user.id]["term"] == None:  # 多輪對話的問句。
            replySTR = '請問，你想問什麼形式語意的問題呢？'
            await message.reply(replySTR)
            
        elif mscDICT[client.user.id]['action'] == "DefineTerm" and mscDICT[client.user.id]['type']==None:
            if mscDICT[client.user.id]['term'] not in userDefinedDICT:
                for key in userDefinedDICT:
                    if mscDICT[client.user.id]['term'] in userDefinedDICT[key]:
                        query = mscDICT['client.user.id']['term']
            else:
                query = mscDICT[client.user.id]['term']
                
            if query  == "動詞":
                replySTR = '請問是及物動詞還是不及物動詞？'
                await message.reply(replySTR)
                    
            elif query == "名詞":
                replySTR = "請問是專有名詞還是普通名詞？"
                await message.reply(replySTR)
                    
            elif query == '形容詞':
                replySTR = '請問是謂語形容詞還是屬性形容詞？'
                await message.reply(replySTR)
                          
                    
        elif mscDICT[client.user.id]['action'] == "comp":
            if mscDICT[client.user.id]['term'] == "句子":
                await messeage.reply(sComp)
            elif mscDICT[client.user.id]['term'] == "動詞":
                await message.reply(vpComp)
            elif mscDICT[client.user.id]['term'] == "名詞":
                await message.reply(npComp)
            
            
        elif mscDICT[client.user.id]['action'] == "DefineTerm" and mscDICT[client.user.id]['type']:
            query = mscDICT[client.user.id]['type']
            replySTR = f"{query}的語意是：{termDICT[query]}"
            
        del mscDICT[client.user.id]
        
if __name__ == "__maiin__":
    client.run(DISCORD_TOKEN)
                    
                    
                    