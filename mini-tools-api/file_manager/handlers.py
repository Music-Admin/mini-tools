import json
import boto3
import os
import base64
from datetime import datetime

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
if S3_ENDPOINT:
    s3 = boto3.client("s3", endpoint_url=S3_ENDPOINT, region_name="us-east-1")
else:
    s3 = boto3.client("s3", region_name="us-east-1")

BUCKET = os.getenv("UPLOAD_BUCKET", "mini-tools")

def handle_file(event, context):
    method = event["httpMethod"]
    path = event["path"]

    if method == "POST" and path == "/file-manager/generate-upload-url":
        return generate_presigned_upload(event)
    elif method == "POST" and path == "/file-manager/upload":
        return upload_file(event, context)
    elif method == "GET" and path.startswith("/file-manager/download-url/"):
        return generate_presigned_url(event)
    elif method == "DELETE" and path.startswith("/file-manager/delete/"):
        return delete_file(event)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid route"})
        }

def generate_presigned_upload(event):
    body = json.loads(event["body"])
    file_name = body["file_name"]
    folder = "uploads"
    key = f"{folder}/{datetime.utcnow().isoformat()}_{file_name}"

    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=600,
    )

    print("BUCKET:", BUCKET)
    print("🧠 Upload key:", key)
    print("✅ Upload URL:", url)

    return {
        "statusCode": 200,
        "body": json.dumps({"upload_url": url, "key": key})
    }

def upload_file(event, context):
    body = json.loads(event["body"])
    file_content = base64.b64decode(body["file_base64"])
    file_name = body.get("file_name", f"uploaded_{context.aws_request_id}.csv")
    prefix = "uploads"
    key = f"{prefix}/{file_name}"

    s3.put_object(Bucket=BUCKET, Key=key, Body=file_content)

    return {
        "statusCode": 200,
        "body": json.dumps({"key": key})
    }

def generate_presigned_url(event):
    try:
        key = event["pathParameters"]["key"]
    except (KeyError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing key parameter"})
        }

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=3600
    )
    return {
        "statusCode": 200,
        "body": json.dumps({"download_url": url})
    }

def delete_file(event):
    key = event["pathParameters"]["key"]
    s3.delete_object(Bucket=BUCKET, Key=key)
    return {
        "statusCode": 200,
        "body": json.dumps({"deleted": key})
    }
