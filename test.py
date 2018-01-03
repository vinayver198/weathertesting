from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import pandas as pd

from flask import Flask, request, make_response

# Flask app should start in global layout
app = Flask(__name__)

users = pd.read_csv('Status.csv')

Status = users.loc[users['EmpId'] == 134256]

RESULT = Status.loc[users['RequestType']=='Desktop Allocation']

RequestId,Status = RESULT['RequestId'].values[0], RESULT['Status'].values[0]
print(RequestId,Status)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print('inside webhook')
    print("Request:")
    print(json.dumps(req, indent=4))
    

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    print('inside makeWebhookResult')
    if req.get("result").get("action") != 'DesktopStatusCheck':
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    RequestType = parameters.get("Desktop")
    EmpId       = parameters.get("EmpId")
    print('Above read_csv commannd')
    users = pd.read_csv('Status.csv')
    print('Below read_csv command')
    Status = users.loc[users['EmpId'] == 134256]
    RESULT = Status.loc[users['RequestType']=='Desktop Allocation']
    RequestId,Status = RESULT['RequestId'].values[0], RESULT['Status'].values[0]
    #query = data.get('query')
    print("Response:")
    
    speech = "The status for you request is "+str(Status)+"and requestId is "+str(RequestId) + " https://www.google.com"
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "TicketMgmtSystem"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
