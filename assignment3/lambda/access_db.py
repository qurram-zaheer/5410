import json
import boto3
import urllib
from datetime import datetime

s3 = boto3.client('s3')
db = boto3.client('dynamodb', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    # TODO implement
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        
        file_content = json.loads(response['Body'].read())
        
        ne = list(file_content.values())[0]
        
        print("NE: ", ne)
        print('TABLES: ', db.list_tables())
        
        table = dynamodb.Table('b00902314')
        for key, value in ne.items():
            table.update_item(
                Key={
                    'NameEntity': key 
                },
                UpdateExpression="SET Frequency = if_not_exists(Frequency, :start) + :inc",
                ExpressionAttributeValues={
                    ':inc': 1,
                    ':start': 0,
                },
            )
    
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
