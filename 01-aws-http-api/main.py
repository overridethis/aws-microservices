from datetime import datetime, timezone

def handler(event, context):
    return {
        'statusCode': 200,
        'body': {
            'message': 'Hello World!',
            'timestamp': datetime.now(timezone.utc).isoformat()
        } 
    }