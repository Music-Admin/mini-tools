#!/bin/bash

set -e

echo "📦 Setting up local resources in LocalStack..."

# Config
REGION="us-east-1"
BUCKET_NAME="mini-tools"
TABLE_NAME="Sessions"
LOCALSTACK_ENDPOINT="http://localhost:4566"

# Create S3 bucket
echo "🪣 Creating S3 bucket: $BUCKET_NAME"
aws s3api create-bucket \
  --bucket "$BUCKET_NAME" \
  --region "$REGION" \
  --endpoint-url "$LOCALSTACK_ENDPOINT" \
  || echo "✅ Bucket already exists"

# Apply CORS config to S3
echo "🌐 Applying CORS to $BUCKET_NAME"
aws s3api put-bucket-cors \
  --bucket "$BUCKET_NAME" \
  --region "$REGION" \
  --endpoint-url "$LOCALSTACK_ENDPOINT" \
  --cors-configuration '{
    "CORSRules": [
      {
        "AllowedOrigins": ["http://localhost:5173"],
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["PUT", "GET", "POST", "DELETE", "HEAD"],
        "ExposeHeaders": ["ETag"],
        "MaxAgeSeconds": 3000
      }
    ]
  }'

# Create DynamoDB table
echo "🗂️  Creating DynamoDB table: $TABLE_NAME"
aws dynamodb create-table \
  --table-name "$TABLE_NAME" \
  --attribute-definitions AttributeName=sessionId,AttributeType=S \
  --key-schema AttributeName=sessionId,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region "$REGION" \
  --endpoint-url "$LOCALSTACK_ENDPOINT" \
  || echo "✅ Table already exists"

echo "✅ Local resources created!"
