import boto3
from decimal import Decimal
from datetime import datetime, timezone
import time
import os
import uuid

REGION = os.environ.get('REGION', 'us-east-2')

class DbUtils:
    def __init__(self):
        self.__client = boto3.resource('dynamodb', region_name=REGION)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4())

    def put_item(self, item, table_name):
        table = self.__client.Table(table_name)

        if 'id' not in item:
            item['id'] = DbUtils.generate_key()
            item['timestamp'] = datetime.now(timezone.utc).isoformat()
        table.put_item(Item=item)

        return item

    def get_item(self, key: dict, table_name):
        table = self.__client.Table(table_name)
        response = table.get_item(Key=key)

        if 'Item' not in response:
            return None

        return response['Item']

    def query_for_items(self, query: dict, table_name):
        table = self.__client.Table(table_name)
        response = table.query(**query)
        
        if 'Items' not in response:
            return []
        
        items = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return response['Items']

    def scan_for_items(self, table_name):
        table = self.__client.Table(table_name)
        response = table.scan()
        
        if 'Items' not in response:
            return []
        
        items = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return response['Items']