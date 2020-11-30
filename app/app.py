import pandas as pd
import requests
import datetime
import json
import os
import time
import pymsteams


import pymongo
connection = pymongo.MongoClient("35.230.140.179")
db = connection['datawarehouse']
db.authenticate('jbohutska',
                '1d515677a3f83f5580df',
                mechanism='MONGODB-CR')

webhook = "https://outlook.office.com/webhook/54823c1d-ccb2-4196-a1e9-644807ac95f8@1935502e-c3e5-4fdf-b27a-bd26fdbdcf3a/IncomingWebhook/695a0619ea0741a5803e4315640ac426/73d97a6d-0a93-479b-9305-713fe59f2353"

def tostamp(date):
    return datetime.datetime.timestamp(date)


def todate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1e3)


def post_message_to_teams(webhook,color,title,text):
    myTeamsMessage = pymsteams.connectorcard(webhook)
    myTeamsMessage.color(color)
    myTeamsMessage.title(title)
    myTeamsMessage.text(text)
    myTeamsMessage.send()


post_message_to_teams(webhook,'green','status update', 'success')
print("HELLO THERE")