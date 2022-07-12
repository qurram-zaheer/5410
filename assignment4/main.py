from bucket import get_bucket, create_bucket, upload_file, print_test_blob
from google.api_core.exceptions import NotFound

from utils import upload_dir

SOURCE_BUCKET_NAME = 'sourcedatab00902314'
TRAIN_BUCKET_NAME = 'traindatab00902314'
TEST_BUCKET_NAME = 'testdatab00902314'


def bucket_creation(bucket_name):
    bucket = None
    try:
        bucket = get_bucket(bucket_name=bucket_name)
        print(f"Bucket {bucket_name} already exists...")
    except NotFound:
        print(f"Creating bucket {bucket_name}...")
        bucket = create_bucket(bucket_name=bucket_name)
    if bucket is None:
        print(f"Something went horribly wrong when creating bucket {bucket_name}!")
        exit(0)

    return bucket


source_bucket = bucket_creation(SOURCE_BUCKET_NAME)
train_bucket = bucket_creation(TRAIN_BUCKET_NAME)
test_bucket = bucket_creation(TEST_BUCKET_NAME)
# upload_dir(bucket=source_bucket, folder_path='Dataset/Train')
# upload_file(source_bucket, file_path='Dataset/Train/001.txt')

upload_dir(bucket=source_bucket, folder_path='Dataset/Test')
