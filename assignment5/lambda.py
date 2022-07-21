import json

import boto3

TOPIC_ARN = "arn:aws:sns:us-east-1:403180102075:halifax_cars"

sns_client = boto3.client('sns', region_name='us-east-1')


def lambda_handler(event, context):
    records = event['Records']
    for record in records:
        print(f'Message body: {record["body"]}')
        print(f'Bob has successfully processed message {record["messageId"]}')
        response = sns_client.publish(TopicArn=TOPIC_ARN, Message=record['body'], Subject='HalifaxCars rental order')

    return f'Successfully processed {len(records)} messages'