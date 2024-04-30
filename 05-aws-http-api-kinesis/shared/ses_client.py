import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION_NAME = os.environ.get('REGION', 'us-east-2')
SENDER = os.environ.get('SENDER', '"MicroServices" <microservices@overridethis.com>')
CHARSET = "UTF-8"

SES_CLIENT = None

class SESClient:
    def __init__(self) -> None:
        global SES_CLIENT
        if SES_CLIENT is None:
            SES_CLIENT = boto3.client('ses', region_name=REGION_NAME)

    def send_email(self,
                   email: str,
                   subject: str,
                   body: str) -> None:
            
        logger.info(f'Sending email to {email}')
        SES_CLIENT.send_email(
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER
        )
        return True

    @staticmethod
    def simple_body(title: str,
                    message: str) -> None:
        body = f"""<html>
        <head></head>
        <body>
            <h3>{title}</h3>
            <p>{message}</p>
        </body>
        </html>
        """
        return body
