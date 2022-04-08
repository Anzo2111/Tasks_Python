import boto3

s3 = boto3.client('s3')

def print_my_bucket_by_name_prod():
    response = s3.list_buckets()

    print('buckets:')
    for buck in response['Buckets']:
        if buck["Name"].startswith('prod'):
            print(f'{buck["Name"]}')

def main():
    print_my_bucket_by_name_prod()

if __name__ == "__main__":
    main()

