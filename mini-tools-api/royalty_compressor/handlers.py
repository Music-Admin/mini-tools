import json
import pandas as pd
import boto3
import os
from io import StringIO
import traceback    

# s3 = boto3.client(
#     "s3",
#     endpoint_url=os.getenv("S3_ENDPOINT", "http://host.docker.internal:4566"),
#     region_name="us-east-1"
# )

s3 = boto3.client("s3", region_name="us-east-1")

BUCKET_NAME = os.getenv("UPLOAD_BUCKET", "mini-tools")

def handle_compression(event, context):
    method = event["httpMethod"]
    path = event["path"]

    try:
        if method == "POST" and path == "/royalty-compressor/compress":
            return compress_report(event, context)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid route"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def compress_report(event, context):
    print("💡 Lambda started")
    print("Event body:", event.get("body")) 
    try:
        body = json.loads(event["body"])
        if "s3_key" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing s3_key"})
            }

        s3_key = body["s3_key"]
        s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        csv_data = StringIO(s3_object["Body"].read().decode("utf-8"))

        print("✅ S3 file fetched")

        first_line = csv_data.readline()
        csv_data.seek(0)
        skiprows = 1 if first_line.strip().startswith("Asset Summary") else 0
        df = pd.read_csv(csv_data, skiprows=skiprows, low_memory=False)

        print("✅ CSV loaded into Pandas")

        if "Adjustment Type" in df.columns:
            df["Adjustment Type"] = df["Adjustment Type"].fillna("None").astype(str)

        df.columns = df.columns.str.strip().str.replace("\u00A0", " ").str.replace(r"\s+", " ", regex=True)

        sum_columns = [
            "Owned Views",
            "Monetized Views : Audio",
            "Monetized Views : Audio Visual",
            "Monetized Views",
            "YouTube Revenue Split",
            "YouTube Revenue Split : Auction",
            "YouTube Revenue Split : Reserved",
            "YouTube Revenue Split : Partner Sold YouTube Served",
            "YouTube Revenue Split : Partner Sold Partner Served",
            "Partner Revenue",
            "Partner Revenue : Auction",
            "Partner Revenue : Reserved",
            "Partner Revenue : Partner Sold YouTube Served",
            "Partner Revenue : Partner Sold Partner Served",
            "Partner Revenue : Pro Rata : Audio",
            "Partner Revenue : Pro Rata : Audio Visual",
            "Partner Revenue : Pro Rata",
            "Partner Revenue : Per Sub Min"
        ]

        existing_sum_cols = [col for col in sum_columns if col in df.columns]
        if not existing_sum_cols:
            raise Exception("No expected revenue columns found in CSV")

        print("✅ Found these columns for sum:", existing_sum_cols)

        df[existing_sum_cols] = df[existing_sum_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        non_sum_cols = [col for col in df.columns if col not in existing_sum_cols + ["Asset ID"]]

        agg_dict = {col: "first" for col in non_sum_cols}
        agg_dict.update({col: "sum" for col in existing_sum_cols})

        df = df.groupby("Asset ID", as_index=False).agg(agg_dict)

        ordered_cols = (
            ["Asset ID"] +
            [col for col in df.columns if col in non_sum_cols] +
            [col for col in df.columns if col in existing_sum_cols]
        )

        df = df[ordered_cols]

        print("✅ File compressed")

        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        output_key = f"processed_reports/royalty_report_{context.aws_request_id}.csv"
        s3.put_object(Bucket=BUCKET_NAME, Key=output_key, Body=output.getvalue(), ContentType="text/csv")

        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": output_key},
            ExpiresIn=3600,
        ).replace("host.docker.internal", "localhost")

        print("✅ Upload complete, returning URL")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "download_url": presigned_url,
                "output_key": output_key,
                "input_key": s3_key
            })
        }

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
