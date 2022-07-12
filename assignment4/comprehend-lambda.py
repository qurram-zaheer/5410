import urllib
import re

import json
import boto3

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')


def clean_the_tweets(tweet):
    return re.sub(r"[^a-zA-Z0-9]+", ' ', tweet)


def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        file = s3.get_object(Bucket=bucket, Key=key)
        lines = file['Body'].read().decode('utf-8').splitlines()

        raw_tweets = [clean_the_tweets(x) for x in lines]
        tweets = [x for x in raw_tweets if len(x) > 0]

        results = []
        n = len(tweets)

        for idx, tweet in enumerate(tweets):
            if len(tweet) == 0:
                continue

            result = {"tweet": tweet}

            sentiment = comprehend.detect_sentiment(Text=tweet, LanguageCode='en')
            sentiment.pop('ResponseMetaData', None)
            result.update(sentiment)

            entities = comprehend.detect_entities(Text=tweet, LanguageCode='en')
            entities.pop('ResponseMetaData', None)
            result.update(entities)

            keyphrases = comprehend.detect_key_phrases(Text=tweet, LanguageCode='en')
            keyphrases.pop('ResponseMetaData', None)
            result.update(keyphrases)

            results.append(result)

            print(idx)

        results = bytes(json.dumps(results).encode('utf-8'))
        print('Results: ', results)
        s3.put_object(Bucket='a4-sentimentanalysis-b00902314', Key='sa-output.json', Body=results)
        return True


    except Exception as e:
        print('Something went wrong ', e)
        raise e
