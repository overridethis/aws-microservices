import json
from datetime import datetime, timezone
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f'Event: {event}')
    return {
        'statusCode': 200,
        'contentType': 'application/json',
        'body': json.dumps({
            'message': 'Hello World!',
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    }

def authorizer(event, context):
    logger.info(f'Event: {event}')
    token = event['headers']['x-api-key']

    return {
        'isAuthorized': token == os.environ['TOKEN']
    }