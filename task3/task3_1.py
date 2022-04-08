import boto3
import argparse

s3 = boto3.client('s3')

def put_file(bucket_name,file_name):
    try:
        with open(file_name, "rb") as file:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=file.read())
            print('Success')
    except Exception as ex:
        print(ex)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket_name')
    parser.add_argument('-f', '--file_name')
    parsed = parser.parse_args()
    put_file(parsed.bucket_name,parsed.file_name)

if __name__ == "__main__":
    main()