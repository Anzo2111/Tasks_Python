import json
import boto3
import argparse

import botocore.exceptions

s3 = boto3.client('s3')

def get_policy(bucket_name):
    mypolicy = {"Version": "2012-10-17",
                "Statement": [
             {"Sid": "PublicReadGetObject",
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": [f"arn:aws:s3:::{bucket_name}/dev/*",f"arn:aws:s3:::{bucket_name}/test/*"]
              }
            ]
         }
    return json.dumps(mypolicy)

def create_policy(bucket_name):
    s3.put_bucket_policy(
        Bucket = bucket_name,
        Policy = get_policy(bucket_name)
    )
    print(f'policy on bucket named {bucket_name} has been created')

def check_current_policy(bucket_name):
    try:
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        print('policy exists')
    except botocore.exceptions.ClientError as ex:
        create_policy(bucket_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    parsed = parser.parse_args()
    check_current_policy(parsed.name)

if __name__ == "__main__":
    main()