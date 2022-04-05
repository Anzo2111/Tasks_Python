import boto3
import argparse

s3 = boto3.client('s3')

def print_my_bucket_by_name(bucket_name):
    response = s3.list_buckets()
    bucket_exists = False

    for buck in response['Buckets']:
        if buck["Name"] == bucket_name:
            bucket_exists = True

    if bucket_exists == True:
            bucket_delete(bucket_name)
    else:
        print(f"Bucket {bucket_name} not exists")

def bucket_delete(bucket_name):
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} was successfully deleted")
    except Exception as ex:
        print(ex)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    parsed = parser.parse_args()
    print_my_bucket_by_name(parsed.name)

if __name__ == "__main__":
    main()