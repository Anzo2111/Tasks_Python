import boto3
import argparse

s3 = boto3.client('s3')

def delete_file(bucket_name,file_name):
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print('file was succesfully deleted')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket_name')
    parser.add_argument('-f', '--file_name')
    parsed = parser.parse_args()
    delete_file(parsed.bucket_name,parsed.file_name)

if __name__ == "__main__":
    main()