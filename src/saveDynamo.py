from ast import Expression
from datetime import datetime
from urllib import response
import boto3


client = boto3.client('dynamodb')
dbtable = 'tickets'
def save_records(data):  
    count = 0
    for elem in data:
        count += 1
        print(elem)
        newItem = {
            'id': {},
            'identifier': {},
            'email':{},
            'ticket-number': {},
            'used': {},
            'createdAt': {},
            'usedTime': {}
        }
        newItem['id']['S']= elem['id']
        newItem['identifier']['S']= elem['identifier']      
        newItem['email']['S']= elem['email']
        newItem['ticket-number']['S']= str(count)
        newItem['used']['BOOL']= False
        newItem['createdAt']['S']= str(datetime.now())
        newItem['usedTime']['S']= str(datetime.now())
        response = client.put_item(
            TableName = dbtable,
            Item= newItem
        )
    print(response)

def validate_ticket(token):
    try :
        response = client.get_item(TableName = dbtable , Key = {'id': {'S':str(token)}})
        if response['Item']:
            if response['Item']['used']['BOOL'] == True : return False, f"USADA {response['Item']['usedTime']['S']}"
            response_update = client.update_item(
                TableName = dbtable,
                Key = {'id': {'S':str(token)}},
                UpdateExpression = "set used = :r, usedTime = :time",
                ExpressionAttributeValues = {
                    ':r': {'BOOL' : True},
                    ':time': {'S': str(datetime.now())}
                },
                ReturnValues = "UPDATED_NEW"
            )
            print(response_update)
            return True, "GOOD"
        else:
            return False, "NO TICKET"
    except Exception as e:
        print(e)
        print("no ticket")
        return False, "ERROR"
    