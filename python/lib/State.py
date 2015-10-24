#!/usr/bin/python
import sqlite3
import json
import HTMLParser
from collections import defaultdict


def id2code(id, db):
    dbActions = db.execute('SELECT code FROM Config WHERE id='+str(id))
    radioCode = dbActions.fetchall()
    try:
        radioCode = radioCode[0][0]
    except:
        radioCode = ""
    return str(radioCode)


def changeState(id, state):
    try:
        db = sqlite3.connect('/user/config/kana/objects/radio.db')
        db.execute('UPDATE Actions SET state='+str(state)+' WHERE id='+str(id))
        db.commit()
        print "KANA : ID="+str(id)+" STATE="+str(state)
    except:
        print "LOCKED"


def getCodes():
    db = sqlite3.connect('/user/config/kana/objects/radio.db')
    dbActions = db.execute('SELECT id,args FROM Actions')
    radioActionsTuples = dbActions.fetchall()
    codes = []
    actions = defaultdict(list)

    HTMLParse = HTMLParser.HTMLParser()
    for radioAction in radioActionsTuples:
        actionID = radioAction[0]

        bufferText = str(radioAction[1])
        bufferText = HTMLParse.unescape(bufferText)
        bufferText = json.loads(bufferText)

        codeOff = id2code(bufferText["code_off"], db)
        codeOn = id2code(bufferText["code_on"], db)

        if codeOn is not "":
            codes.append(codeOn)
            actions[codeOn].append({"id": actionID, "state": 1})

        if codeOff is not "":
            codes.append(codeOff)
            actions[codeOff].append({"id": actionID, "state": 0})

    # Remove duplicate
    codes = list(set(codes))
    return codes, actions


def checkCodes(codes, codeToCheck, actions):
    for code in codes:
        print code+"====="+codeToCheck
        if code == codeToCheck:
            print "Code detected"
            print codeToCheck
            for action in actions[codeToCheck]:
                actionID = action["id"]
                state = action["state"]
                changeState(actionID, state)
