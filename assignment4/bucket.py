from pathlib import Path

from google.cloud.storage import Client, Blob
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import nltk
nltk.download('stopwords')
nltk.download('punkt')

client = Client()


def get_bucket(bucket_name):
    return client.get_bucket(bucket_or_name=bucket_name)


def create_bucket(bucket_name):
    return client.create_bucket(bucket_name, location='us-central1')


def upload_file(bucket, file_path):
    blob_name = Path(file_path).stem
    blob = bucket.blob(blob_name=blob_name)
    blob.upload_from_filename(filename=file_path)


def print_test_blob(bucket):
    blob = bucket.get_blob(blob_name='001')
    blob_content = blob.download_as_bytes().decode('utf-8')
    # print(f'Blob: {blob_content}')
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(blob_content)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    print(filtered_sentence)