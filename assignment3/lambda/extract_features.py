import json
import urllib
import boto3
import re
from string import punctuation
from collections import defaultdict

from stop_words import get_stop_words

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    stop_words = get_stop_words('en')
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        
        file_content = response['Body'].read().decode('utf-8')
        file_content = " ".join(file_content.split())
        print('File: ', file_content)
        
        words_arr = file_content.split(' ')
        
        
        words_arr = [x.strip(punctuation) for x in words_arr]
        words_arr = [x for x in words_arr if x.lower() not in stop_words]
        
        ne_list = [x for x in words_arr if x[0].upper() == x[0]]

        print(ne_list)
        
        fq= defaultdict( int )
        for w in ne_list:
            fq[w]+=1
            
        print(fq)
        filename = key.split('.')[0]
        
        s3.put_object(Body=json.dumps({f'{filename}ne': fq}), Bucket='tagsb00902314', Key=f'{filename}ne.txt')
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    return {
        'statusCode': 200,
    }
