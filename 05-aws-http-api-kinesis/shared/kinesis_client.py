import boto3
import json
import os
import logging

from utils import decimal_default

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get('REGION', 'us-east-2')
KINESIS_CLIENT = None

class KinesisClient:
    @staticmethod
    def get_client():
        global KINESIS_CLIENT
        if KINESIS_CLIENT is None:
            KINESIS_CLIENT = boto3.client('kinesis', region_name=REGION)
        return KINESIS_CLIENT

    @staticmethod
    def send_record(stream_arn: str, data: dict):
        kinesis_client = KinesisClient.get_client()
        stream_name = stream_arn.split('/')[-1]

        record = {
            'Data': json.dumps(data, default=decimal_default),
            'PartitionKey': 'partition_key'
        }

        kinesis_client.put_records(
            StreamName=stream_name,
            Records=[record]
        )


