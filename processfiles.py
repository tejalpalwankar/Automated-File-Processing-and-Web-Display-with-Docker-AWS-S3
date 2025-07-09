import boto3

def lambda_handler(event=None, context=None):
    s3 = boto3.client('s3')
    bucket = 'file-processor-bucket'  # Replace with your actual bucket name
    prefix = 'uploaded/'

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key == prefix:
            continue

        # Download
        file_obj = s3.get_object(Bucket=bucket, Key=key)
        text = file_obj['Body'].read().decode('utf-8')

        # Process
        processed_text = text.upper()
        new_key = key.replace('uploaded/', 'processed/')

        # Upload
        s3.put_object(Bucket=bucket, Key=new_key, Body=processed_text)

if __name__ == "__main__":
    lambda_handler()
