import boto3
from botocore.exceptions import ClientError
import logging
import os
import time

def create_bucket(bucket_name, region=None):
    buckets = list_buckets()
    if bucket_name in buckets:
        logging.debug(msg="Bucket already exists, skipping creation...")
        return True
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False

    return True


def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    return [bucket['Name'] for bucket in response['Buckets']]


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    return True


def list_tables():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    response = dynamodb.list_tables()

    return response['TableNames']


def create_table(table_name, attribute_defs, key_schema):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    tables = list_tables()

    if table_name not in tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_defs,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        return True

    return True


if __name__ == '__main__':
    print(create_bucket('sourceb00902314'))
    print(create_bucket('tagsb00902314'))
    print(create_table(table_name='b00902314', 
            attribute_defs=[{'AttributeName': 'NameEntity', 'AttributeType': 'S'}],
            key_schema=[{'AttributeName': 'NameEntity', 'KeyType': 'HASH'}]
        ))

    file_paths = [f'00{i}.txt' for i in range(1,7)]

    for file_path in file_paths:
        upload_file(os.path.join('tech', file_path), 'sourceb00902314')
        time.sleep(0.2)

    

    