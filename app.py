from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    s3 = boto3.client('s3')
    bucket = 'file-processor-bucket'  # Replace with your actual bucket name
    prefix = 'processed/'
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files = [obj['Key'].replace(prefix, '') for obj in response.get('Contents', []) if obj['Key'] != prefix]
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
