import pandas as pd
import psycopg2
import os
import boto3

input_file = "/tmp/clean_data.csv"

conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="password",
    port="5432"
)

def load():

    df = pd.read_csv(input_file)

    cursor = conn.cursor()

    chunk_size = 1000

    for i in range(0, len(df), chunk_size):

        chunk = df.iloc[i:i+chunk_size]

        for _, row in chunk.iterrows():

            cursor.execute(
                """
                INSERT INTO customers (id, name, email)
                VALUES (%s,%s,%s)
                """,
                (row["id"], row["name"], row["email"])
            )

        conn.commit()

    print("Data loaded successfully")

    cursor.close()
    conn.close()

    cleanup()


def cleanup():

    s3 = boto3.client("s3")

    source_bucket = "source-bucket"
    dest_bucket = "processed-bucket"

    source_key = "incoming/data.csv"
    dest_key = "Done/data.csv"

    s3.copy_object(
        Bucket=dest_bucket,
        CopySource={"Bucket": source_bucket, "Key": source_key},
        Key=dest_key
    )

    os.remove("/tmp/data.csv")
    os.remove("/tmp/clean_data.csv")

    print("Files cleaned and moved to Done folder")


if __name__ == "__main__":
    load()