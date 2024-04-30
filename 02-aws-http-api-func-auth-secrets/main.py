import boto3
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
    
    secret_key = os.environ['SECRET_KEY']
    secret = GetSecretWrapper().get_secret(secret_key)

    return {
        'isAuthorized': token == secret
    }

class GetSecretWrapper:
    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def get_secret(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
            logging.info("Secret retrieved successfully.")
            return get_secret_value_response["SecretString"]
        except self.client.exceptions.ResourceNotFoundException:
            msg = f"The requested secret {secret_name} was not found."
            logger.info(msg)
            return msg
        except Exception as e:
            logger.error(f"An unknown error occurred: {str(e)}.")
            raise