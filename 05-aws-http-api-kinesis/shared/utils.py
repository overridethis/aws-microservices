import json
from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def default_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'X-Frame-Options': 'DENY',
        'Content-Type': 'application/json'
    }

def get_body(event):
    if 'body' not in event:
        return None
    return json.loads(event['body']) if 'body' in event else None

def set_response(status_code, body, serialized=False):
    serialized_body = body if serialized else json.dumps(body, default=decimal_default)
    return {
        'statusCode': status_code,
        'body': serialized_body,
        'headers': default_headers()
    }