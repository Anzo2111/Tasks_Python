import boto3

s3 = boto3.client('s3')

def print_my_bucket():
    response = s3.list_buckets()

    # print(response)

    print('List of buckets:')
    for buck in response['Buckets']:
        print(f'{buck["Name"]}')


def main():
    print_my_bucket()


if __name__ == "__main__":
    main()