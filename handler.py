import json
import os
import boto3
from src.saveDynamo import save_records, validate_ticket
from src.generateQr import createQR
from src.sendEmail import load_images
sqs = boto3.client('sqs')
sqs_url = os.environ.get("QUEUE_EMAIL_URL")

def redirection(event, context):
    message = ''
    response = {}
    body = '''
    <html><head><link href="https://fonts.googleapis.com/css?family=Nunito+Sans:400,400i,700,900&display=swap" rel="stylesheet"></head><style>body{text-align: center; padding: 40px 0; background: #EBF0F5;}h1{color: #88B04B; font-family: "Nunito Sans", "Helvetica Neue", sans-serif; font-weight: 900; font-size: 40px; margin-bottom: 10px;}p{color: #404F5E; font-family: "Nunito Sans", "Helvetica Neue", sans-serif; font-size:20px; margin: 0;}i{color: #9ABC66; font-size: 100px; line-height: 200px; margin-left:-15px;}.card{background: white; padding: 60px; border-radius: 4px; box-shadow: 0 2px 3px #C8D0D8; display: inline-block; margin: 0 auto;}</style><body><div class="card"><div style="border-radius:200px; height:200px; width:200px; background: #F8FAF5; margin:0 auto;"><i class="checkmark">ok</i></div><h1>Valido</h1> <p>Bienvenido<br/>Disfruta de 'the hottest fest'</p></div></body></html>
    '''
    if 'cookies' in event:
        print(event["cookies"])
        if 'authorized=12345' in event['cookies']:
            valid, message = validate_ticket(event['rawQueryString'].split("=")[1])
            if valid:
                response = {
                    "statusCode": 200, 
                    "body": body,
                    "headers": {'Content-Type': 'text/html'},
                }
            else:
                 response = {
                        "statusCode": 404, 
                        "body": f"<html><body><h1>{message}</h1></body></html>",
                        "headers": {'Content-Type': 'text/html'},
                        #"headers" : {"Location": "https://www.google.com"}
                }
    else:
        response = {
            "statusCode": 404, 
            "body": "<html><body><h1>PLEASE DO NOT SCAN</h1></body></html>",
            "headers": {'Content-Type': 'text/html'},
            #"headers" : {"Location": "https://www.google.com"}
        }

    # response = {
    #     "statusCode": 200, 
    #     "body": "<html><body><h1>OK</h1></body></html>"
    # }
    return response

def generateQr(event, context):
    data = event['Records']
    print(data)
    for elem in data :
        info = json.loads(elem['body'])
        obj = createQR(int(info['number']), info['email'])
        sqs.send_message(
            QueueUrl= sqs_url,
            MessageBody=json.dumps({'data': obj})
        )
        print(obj)
    return  {}

def sendEmail(event, context):
    data = event["Records"]
    try:
        for elem in data:
            body =json.loads(elem['body'])
            print("antes")
            save_records(body['data'])
            print("despues")
            load_images(body['data'])
            
    except Exception as e: 
        print('ex')
        print(e)
    return {}

def setAuthorizedUser(event, contex):
    response = {
        "statusCode": 200, 
        "body": "Authorized",
        "headers": {'Content-Type': 'application/json', 'Set-cookie': "authorized=12345"},
        #"headers" : {"Location": "https://www.google.com"}
    }
    return response

