#!/bin/bash

# Build the app
echo "📦 Building Vite project..."
npm run build

# Sync to S3
echo "🚀 Deploying to S3..."
aws s3 sync dist/ s3://mini-tools-react/ --delete

# Done
echo "✅ Deployed to S3: https://mini-tools-react.s3-website-us-east-1.amazonaws.com"
