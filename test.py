from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import pandas as pd

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

users = pd.read_csv('C:\\Users\\vinayver\\Desktop\\Status.csv')

Status = users.loc[users['EmpId'] == 134256]
RESULT = Status.loc[users['RequestType']=='Desktop Allocation']
RequestId,Status = RESULT['RequestId'], RESULT['Status']
print('1')


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    action = req.get("result").get("action")
    print(action)

    if action == 'DesktopStatusCheck':
        data = DesktopStatusCheck(req)
        res  = makeWebhookResult(data)
    else:
        return {}
    return res

def DesktopStatusCheck(req):
   users = pd.read_csv()
   yql_query = makeYqlQuery(req)
   if yql_query is None:
       return {}
   else:
       data = json.loads(yql_query)
       print(data)
       return data

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    RequestType = parameters.get("Desktop")
    EmpId       = parameters.get("EmpId")
    users = pd.read_csv('C:\\Users\\vinayver\\Desktop\\Status.csv')
    Status = users.loc[users['EmpId'] == 134256]
    RESULT = Status.loc[users['RequestType']=='Desktop Allocation']
    RequestId,Status = RESULT['RequestId'], RESULT['Status']
    value = {RequestId,Status}
    return value

def makeWebhookResult(data):
    query = data.get('query')
    print("Response:")
    print('Vinay')
    speech = "The status for you request is"+Status+"and requestId is "+RequestId
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')