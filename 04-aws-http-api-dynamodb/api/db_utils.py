import boto3
from decimal import Decimal
from datetime import datetime, timezone
import os
import uuid

EXPENSES_TABLE = 'Expenses'
REGION = os.environ.get('REGION', 'us-east-2')

def get_client():
    return boto3.resource('dynamodb', region_name=REGION)

def put_item(item, table_name=EXPENSES_TABLE):
    dynamodb = get_client()
    table = dynamodb.Table(table_name)

    item['amount'] = Decimal(item['amount'])
    if 'id' not in item:
        item['id'] = str(uuid.uuid4())
        item['timestamp'] = datetime.now(timezone.utc).isoformat()
    table.put_item(Item=item)

    return item

def get_item(key: dict, table_name=EXPENSES_TABLE):
    dynamodb = get_client()
    table = dynamodb.Table(table_name)

    response = table.get_item(Key=key)

    if 'Item' not in response:
        return None

    return response['Item']

def get_items(table_name=EXPENSES_TABLE):
    dynamodb = get_client()

    table = dynamodb.Table(table_name)
    response = table.scan()
    
    if 'Items' not in response:
        return []
    
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return response['Items']