import pandas as pd

input_file = "/tmp/data.csv"
output_file = "/tmp/clean_data.csv"

def transform():

    df = pd.read_csv(input_file)

    # remove duplicates
    df = df.drop_duplicates()

    # remove null rows
    df = df.dropna()

    df.to_csv(output_file, index=False)

    print("Rows after transform:", len(df))

if __name__ == "__main__":
    transform()