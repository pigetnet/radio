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


def getCodes():
    db = sqlite3.connect('/user/config/kana/objects/radio.db')
    dbActions = db.execute('SELECT id,args FROM Actions')
    radioActionsTuples = dbActions.fetchall()
    codesList = []
    actionsDict = defaultdict(list)

    HTMLParse = HTMLParser.HTMLParser()
    for radioAction in radioActionsTuples:
        actionID = radioAction[0]

        bufferText = str(radioAction[1])
        bufferText = HTMLParse.unescape(bufferText)
        bufferText = json.loads(bufferText)

        codeOff = id2code(bufferText["code_off"], db)
        codeOn = id2code(bufferText["code_on"], db)

        if codeOn is not "":
            codesList.append(codeOn)
            actionsDict[codeOn].append({"id": actionID, "state": 1})

        if codeOff is not "":
            codesList.append(codeOff)
            actionsDict[codeOff].append({"id": actionID, "state": 0})

    # Remove duplicate
    codesList = list(set(codesList))
    return codesList, actionsDict

#print codesList
#print actionsDict["/radio/old/490614"]["id"]
#print actionsDict
codes, actions = getCodes()
print codes
print actions["/radio/new/10151594/1/off"][1]
