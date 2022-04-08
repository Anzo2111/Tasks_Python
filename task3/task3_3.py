import boto3
import argparse

s3 = boto3.client('s3')

def download_file(bucket_name,file_name,save_path):
    if(save_path == './'):
        save_path=save_path+file_name

    if(key_exists(bucket_name,file_name)):
        s3.download_file(bucket_name,file_name,save_path)
        print('file was succesfully downloaded')
    else:
        print("File doesnt exists")

def key_exists(bucket_name, file_name):
    result = s3.list_objects(Bucket=bucket_name)
    for obj in result.get("Contents", []):
        if(obj.get("Key") == file_name):
            return True
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket_name')
    parser.add_argument('-f', '--file_name')
    parser.add_argument('-p', '--save_path ',default ='./')
    parsed = parser.parse_args()
    download_file(parsed.bucket_name,parsed.file_name,parsed.save_path)

if __name__ == "__main__":
    main()