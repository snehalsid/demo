import boto3
import pandas as pd

bucket_name = "source-bucket"
file_key = "incoming/data.csv"
local_file = "/tmp/data.csv"

s3 = boto3.client("s3")

def extract():
    print("Downloading file from S3...")

    s3.download_file(bucket_name, file_key, local_file)

    df = pd.read_csv(local_file)

    print("Rows extracted:", len(df))

if __name__ == "__main__":
    extract()