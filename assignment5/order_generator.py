import json
import os
import random
import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta

import boto3
from dotenv import load_dotenv

from datetime_handler import random_date

load_dotenv()
SQS_URL = os.environ.get('SQS_URL')

sqs = boto3.client('sqs', region_name='us-east-1')

with open('vehicles.json') as fp:
    VEHICLES = json.load(fp)

random_selection = random.randrange(0, len(VEHICLES))
print(f"random index: {random_selection}")
selected_vehicle = VEHICLES[random_selection]

today = datetime.now()
start_date = random_date(today, today + relativedelta(years=1))
end_date = random_date(start_date, start_date + relativedelta(weeks=4))
selected_vehicle['dates'] = {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat()}

response = sqs.send_message(
    QueueUrl=SQS_URL,
    MessageAttributes={
        'Title': {
            'DataType': 'String',
            'StringValue': 'Order'
        },
        'Author': {
            'DataType': 'String',
            'StringValue': 'Qurram Zaheer'
        }
    },
    MessageBody=json.dumps(selected_vehicle),
    MessageGroupId="order",
    MessageDeduplicationId=str(uuid.uuid4())
)

print(response['MessageId'])

