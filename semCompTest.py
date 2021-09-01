# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:06:02 2021

@author: Admin
"""

def sentComp(verb, verbType, subj, obj =''):
    if verbType == 'vi':
        print(f"{verb}的語意是：lambda x [{verb}(x)]")
        print("VP的語意是：同上")
        print(f"句子的語意是：[{verb}({subj})]")
    elif verbType == 'vt':
        if obj:
            print(f"{verb}的語意是：lambda x lambda y [{verb}(y, x)]")
            print(f"VP的語意是：lambda y [{verb}({obj}, x)]")
            print(f"句子的語意是：[{verb}({obj}, {subj})]")
        