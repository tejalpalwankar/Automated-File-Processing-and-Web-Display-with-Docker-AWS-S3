# 🚀 Automated File Processing and Web Display with Docker & AWS S3

This project demonstrates a cloud-based file processing pipeline where uploaded files are automatically processed and displayed via a web interface running on Docker, integrated with AWS services.

---

## 🎯 Objective

To build a scalable, cloud-based system where:

- Files uploaded to an **AWS S3 bucket** are automatically processed.
- A **Flask web app** running inside a **Docker container** on an **AWS EC2** instance fetches and displays the processed files.
- The solution mimics a serverless workflow using lightweight services.

---

## 🧱 Tech Stack

- **AWS EC2** – Hosts the Flask app using Docker  
- **AWS S3** – Stores uploaded and processed files  
- **Docker** – Containerizes the Flask app  
- **Python + Flask** – Web application and file processing logic  
- **IAM** – Access control for EC2-S3 communication  

---

## 🛠 Project Architecture

```
[S3 Bucket - uploaded folder] → [File Processor (Flask)] → [S3 - processed folder]
                                       ↓
                              [Dockerized Flask App]
                                       ↓
                          [Web UI on EC2 - Flask renders output]
```

---

## 🧪 Prerequisites

✅ AWS Account  
✅ AWS CLI configured  
✅ EC2 key-pair and basic familiarity with SSH  
✅ IAM Role for EC2 with S3 access  
✅ Python (3.7+) and Docker installed on EC2  

---

## 🧰 Step-by-Step Setup Guide

### 🔸 1. Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance.
2. Choose Amazon Linux 2 or Ubuntu.
3. Create a new **security group** allowing:
   - SSH (Port 22)
   - HTTP (Port 80)
4. Assign an IAM Role with **S3 Full Access**.
5. Launch the instance and connect via SSH.

---

### 🔸 2. Install Docker and Python

SSH into EC2 and run:

```bash
# Update and install Docker
sudo apt update && sudo apt install -y docker.io python3-pip
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Reconnect or run newgrp docker to apply group changes
```

---

### 🔸 3. Setup AWS S3 Bucket

1. Create an S3 bucket (e.g., `file-processor-bucket`).
2. Inside it, create two folders:
   - `uploaded/`
   - `processed/`
3. Enable **public access** if files will be viewed publicly.
4. Ensure your IAM role or user has permissions to `GetObject`, `PutObject`.

---

### 🔸 4. Create Flask App

Here’s a basic `app.py`:

```python
from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    s3 = boto3.client('s3')
    bucket = 'file-processor-bucket'
    prefix = 'processed/'
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files = [obj['Key'].replace(prefix, '') for obj in response.get('Contents', []) if obj['Key'] != prefix]
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

Template (`templates/index.html`):

```html
<!DOCTYPE html>
<html>
<head><title>Processed Files</title></head>
<body>
<h2>Processed Files</h2>
<ul>
  {% for file in files %}
    <li>{{ file }}</li>
  {% endfor %}
</ul>
</body>
</html>
```

---

### 🔸 5. File Processing Script (`processfiles.py`)

```python
import boto3

def lambda_handler(event=None, context=None):
    s3 = boto3.client('s3')
    bucket = 'file-processor-bucket'
    prefix = 'uploaded/'

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key == prefix: continue

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
```

---

### 🔸 6. Dockerize the Flask App

Create a `Dockerfile`:

```Dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install flask boto3

EXPOSE 80
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t flask-s3-app .
docker run -d -p 80:80 flask-s3-app
```

---

### 🔸 7. Test the Workflow

1. Upload a `.txt` file (all lowercase) to `uploaded/` in S3.
2. Run `processfiles.py` manually or simulate S3 event.
3. Visit `http://<EC2-Public-IP>/` to view the processed files.

---

## 🐞 Troubleshooting

- ❌ **Access Denied?**
  - Check EC2 IAM Role permissions.
  - Ensure bucket policy allows actions.
- ❌ **Web not loading?**
  - Check if EC2 security group allows Port 80.
  - Try restarting Docker container.

---

## 📂 Sample I/O

| File | Content Before | Content After |
|------|----------------|----------------|
| `uploaded/sample.txt` | hello world     | HELLO WORLD     |
| `processed/sample.txt` | ✅            | ✅              |


## 🧠 Key Learning

- Emulated a **serverless pipeline** without Lambda.
- Dockerized application for cloud portability.
- Practical IAM and AWS S3 integration.
