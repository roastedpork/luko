import apiai
import json

ACCESS_TOK = "82e816725d8b41c0aae0248eb1116e67"


def queryDialogflow(query):
    ai = apiai.ApiAI(ACCESS_TOK)
    request = ai.text_request()
    request.session_id = 1
    request.query = query
    return request.getresponse()


def queryAction(query):
    response = queryDialogflow(query).read()
    res_json = json.loads(' '.join(response.split()))
    print response
    print
    print res_json['result']['action']
    print
    print json.dumps(res_json['result']['parameters'])

