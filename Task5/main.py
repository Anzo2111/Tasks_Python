import boto3
from pathlib import Path
from botocore.exceptions import ClientError
import time

s3 = boto3.client('s3')
client = boto3.client('lambda')
iam = boto3.client('iam')
file_extensions = ['.jpg', '.jpeg', '.png']


def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
    except Exception as ex:
        print(ex)

def convert_to_bytes(zip_file):
    with open(zip_file, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content


def create_function(function_name, iam_role, zip_file):
    try:
        client.create_function(
            FunctionName=function_name,
            Runtime='python3.8',
            Role=iam.get_role(RoleName=iam_role)['Role']['Arn'],
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': convert_to_bytes(zip_file)
            },
        )
        print(f'function {function_name} has been created')
    except ClientError as e:
        print(e)

def add_permission(function_name, bucket_name):
    client.add_permission(
        FunctionName=function_name,
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}',
    )


def s3_trigger(bucket_name, function_name):
    lambda_foreach = []
    for extension in file_extensions:
        lambda_foreach.append({
            'LambdaFunctionArn': client.get_function(
                FunctionName=function_name)['Configuration']['FunctionArn'],
            'Events': [
                's3:ObjectCreated:*'
            ],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': extension
                        },
                    ]
                }
            }
        },)
    try:
        add_permission(function_name, bucket_name)
        s3.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': lambda_foreach,
            }
        )
        print(f'{function_name} has been added to {bucket_name}')
    except ClientError as e:
        print(e)

def upload_file(file_name, bucket_name, file):
    s3.upload_file(file_name, bucket_name, file)


def read_file(bucket_name, file):
    try:
        time.sleep(50)
        data = s3.get_object(Bucket=bucket_name, Key=file.replace('.jpeg', '.json'))
        contents = data['Body'].read()
        print(contents)
    except Exception as ex:
        print(f"Something went wrong :( {ex}")


def main(function_name, iam_role, zip_file, bucket_name, file_name):
    file = file_name
    create_bucket(bucket_name)
    create_function(function_name, iam_role, zip_file)
    s3_trigger(bucket_name, function_name)
    upload_file(file_name, bucket_name, file)
    read_file(bucket_name, file)

if __name__ == '__main__':
    main('lambda-function', 'LabRole',
                     './lambda_function.zip', 'bucketname1234', 'dogs.jpeg')
