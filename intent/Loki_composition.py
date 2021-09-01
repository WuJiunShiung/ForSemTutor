#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for composition

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_composition = True
userDefinedDICT = {"lambda": [""], "動詞": ["verb"], "句子": ["S", "sentence"], "名詞": ["noun"], "短語": [""], "形容詞": ["adj", "adjective"], "全稱量詞": ["for all", "universal quantifier"], "及物動詞": ["transitive verb"], "可數名詞": ["countable noun"], "存在量詞": ["there is", "existential quantifier"], "專有名詞": ["proper noun"], "不及物動詞": ["intransitive verb"], "屬性形容詞": ["attribute adjective"], "謂語形容詞": ["predicate adjective"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_composition:
        print("[composition] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[句子]是幹什麼的":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "[句子]的意思怎麼來的":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "[句子]的意思是什麼":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "[句子]的語意怎麼來的":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "[句子]的語意是什麼":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "[名詞]短語是幹什麼的":
        resultDICT['term'] = args[0]
        resultDICT['action'] = 'comp'

    if utterance == "[名詞]短語的意思怎麼來的":
        resultDICT['term'] = args[0]
        resultDICT['action'] = 'comp'

    if utterance == "[名詞]短語的意思是什麼":
        resultDICT['term'] = args[0]
        resultDICT['action'] = 'comp'

    if utterance == "[名詞]短語的語意是什麼":
        resultDICT['term'] = args[0]
        resultDICT['action'] = 'comp'

    if utterance == "什麼是[句子]的意思":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "什麼是[句子]的語意":
        if args[0] == '句子':
            resultDICT['term'] = args[0]
            resultDICT['action'] = 'comp'

    if utterance == "什麼是[名詞]短語的意思":
        resultDICT['term'] = args[0]
        resultDICT['action'] = 'comp'

    if utterance == "什麼是[名詞]短語的語意":
        resultDICT['term'] = args[0]
        resultDICT['action'] = 'comp'

    return resultDICT