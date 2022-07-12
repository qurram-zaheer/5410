import os
import time

from tqdm import tqdm

from bucket import upload_file


def upload_dir(bucket, folder_path):
    for file in tqdm(os.listdir(folder_path)):
        if file.endswith('.txt'):
            upload_file(bucket=bucket, file_path=os.path.join(folder_path, file))
            time.sleep(1)
