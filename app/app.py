from google.cloud import storage
import pandas as pd
import requests
import datetime
import json
import os
import time
import pymsteams
import pymongo


webhook = "https://outlook.office.com/webhook/54823c1d-ccb2-4196-a1e9-644807ac95f8@1935502e-c3e5-4fdf-b27a-bd26fdbdcf3a/IncomingWebhook/695a0619ea0741a5803e4315640ac426/73d97a6d-0a93-479b-9305-713fe59f2353"

def tostamp(date):
    return datetime.datetime.timestamp(date)


def todate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1e3)

def post_message_to_teams(webhook,title,text):
    myTeamsMessage = pymsteams.connectorcard(webhook)
    myTeamsMessage.title(title)
    myTeamsMessage.text(text)
    myTeamsMessage.send()

def run_pipeline(param):
    max_date = tostamp(datetime.datetime.now().replace(microsecond=0))*1e3
    min_date = tostamp((datetime.datetime.now() - datetime.timedelta(3)).replace(hour=0, minute=0, second=0, microsecond=0))*1e3

    payload = {
                "card": {
                    "rangeName": "custom",
                    "fromDate": min_date,
                    "toDate": max_date,
                    "subType": "line",
                    "type": "line",
                    "startDayOfWeek": param['startDayOfWeek'],
                    "selectedFrequency": param['frequency'], # here it has to be "daily", "weekly" or "monthly"
                    "dataSets": [{"metric": {"id": int(param['metric_id'])},
                                 "virtualId": 1,
                                 "name": "not_used",
                                 "letter":"A",
                                 "isIncrease":param['increase_good']
                                 }
                                 ],
                    "filters": {},
                    "owner": {"id": 1},
                    "letters": {"1": "A"},
                    "size": 2000,
                },
                "organisation": param['organisation'],
                "uuid": 1111,
                "showWeekEndDate": param['showWeekEndDate'],
                "backend_env": "api.app.avora.com",
                "user email": "julia.bohutska",
                "userId": "FP remover",
                "token": param['token']
            }
    try:
        headers =  {"Content-type": "application/json", "Authorization": "Bearer " +payload['token']}
        response = requests.post('https://{}/avora/card/loadData'.format(payload['backend_env']), data=json.dumps(payload), headers=headers)
        print(response)

        df = pd.DataFrame(json.loads(response.text)['data']['results'], columns=['Date', 'Value'])

        return df, max_date, str(response), True

    except:
        df = pd.DataFrame([[str(max_date), 0],[str(min_date), 0]], columns=['Date', 'Value'])
        return df, max_date, str(response), False

def get_meta(row): 
    p={}
    cur = db.metric.find({"_id":row['metricID']})
    q=[]
    for i in iter(cur):
        q.append(i)

    p['metric_id'] = row['metricID']
    p['organisation'] = q[0]['organisation']
    p['increase_good'] = q[0]['isIncrease']

    cur = db.organisation.find({"_id": q[0]['organisation']})
    for i in iter(cur):
        q.append(i)

    p['showWeekEndDate'] = q[1]['showWeekEndDate']
    p['startDayOfWeek'] = q[1]['startDayOfWeek']

    p['frequency']  = row['frequency']
 
    cur = db.authenticationToken.find({"username":row["username"]})
    token = list(cur)[0]['tokenValue']
    p['token'] = token

    return p

metrics_df = pd.read_csv("metrics_table.csv") ## table headers: metricID, username, frequency

## getting metric params 
connection = pymongo.MongoClient("35.230.140.179")
db = connection['datawarehouse']
db.authenticate('jbohutska',
                '1d515677a3f83f5580df',
                mechanism='MONGODB-CR')

params_list = metrics_df.apply(lambda x: get_meta(x), axis=1).tolist()
connection.close()


#client = storage.Client()

update=[]
for param in params_list:

    try:

        data, time, response, succes = run_pipeline(param)

        if succes:
            bucket = client.get_bucket('julia-bucket')
            bucket.blob('{}_{}.csv'.format(str(param[metric_id]), str(max_date))).upload_from_string(df.to_csv(), 'text/csv')
            update.append([str(param['metric_id']),"Succes"])
        else:
            update.append([str(param['metric_id']), response])

    except Exception as e:
        print(e)
        update.append([str(param['metric_id']), "Failed"])

textList = [": ".join(x) for x in update]
text = "\r- ".join(textList)
text = "- "+text
post_message_to_teams(webhook,"Update @ {}".format(todate(time)),text)




















