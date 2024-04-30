import json
from datetime import datetime, timezone
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

default_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
    'X-Frame-Options': 'DENY',
    'Content-Type': 'application/json'
}


def handler(event, context):
    logger.info(f'Event: {event}')
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello World!',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }),
        'headers': default_headers
    }
