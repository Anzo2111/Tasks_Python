import boto3
import argparse

s3 = boto3.client('s3')

def get_unique_suffix(bucket_name):
    result = s3.list_objects(Bucket=bucket_name)
    unique_list = []

    for obj in result.get("Contents", []):
        if obj.get("Key").split('.')[1] not in unique_list:
            unique_list.append(obj.get("Key").split('.')[1])

    return unique_list

def count_suffix(bucket_name,suffix):
    result = s3.list_objects(Bucket=bucket_name)
    counter = 0

    for obj in result.get("Contents", []):
        if obj.get("Key").split('.')[1] == suffix:
            counter+=1

    return counter

def get_files_suffix_counter(bucket_name):
    suffix_array= get_unique_suffix(bucket_name)

    for obj in suffix_array:
        suffix_count = count_suffix(bucket_name,obj)
        print(obj, suffix_count)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket_name')
    parsed = parser.parse_args()
    get_files_suffix_counter(parsed.bucket_name)

if __name__ == "__main__":
    main()