import boto3
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['ResourceProperties']['BucketName']
    source_path = event['ResourceProperties']['SourcePath']

    # Upload index.html
    with open(source_path, 'rb') as file_data:
        s3_client.put_object(Bucket=bucket_name, Key='index.html', Body=file_data)
    
    return {
        'statusCode': 200,
        'body': f"File {source_path} uploaded to {bucket_name}/index.html"
    }
