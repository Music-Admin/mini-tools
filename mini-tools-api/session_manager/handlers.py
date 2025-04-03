import json
import time
import traceback
import boto3
import os
import uuid
from decimal import Decimal

# dynamodb = boto3.resource(
#     "dynamodb",
#     endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://host.docker.internal:4566"),
#     region_name="us-east-1"
# )

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

table = dynamodb.Table(os.getenv("SESSION_TABLE_NAME", "Sessions"))


def handle_session(event, context):
    method = event["httpMethod"]
    path = event["path"]
    path_params = event.get("pathParameters", {})

    try:
        if method == "POST" and path == "/session-manager/create-session":
            return create_session(event)
        elif method == "POST" and path.startswith("/session-manager/track-usage/"):
            session_id = path_params.get("session_id")
            return track_usage(session_id, event)
        elif method == "GET" and path.startswith("/session-manager/session-data/"):
            session_id = path_params.get("session_id")
            return get_session_data(session_id)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid route or method"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    return obj

def create_session(event):
    try:
        session_id = str(uuid.uuid4())
        expires_at = int(time.time()) + 7 * 24 * 60 * 60  # 7 days

        body = json.loads(event.get("body", "{}"))
        metadata = {
            "created_at": int(time.time()),
            "expires_at": expires_at,
            "user_agent": body.get("user_agent", ""),
            "ip_address": body.get("ip_address", "")
        }

        table.put_item(Item={
            "sessionId": session_id,
            "metadata": metadata,
            "usage_logs": []
        })

        return {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": session_id,
                "expires_at": expires_at
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def track_usage(session_id, event):
    try:
        body = json.loads(event["body"])
        usage_entry = {
            "timestamp": int(time.time()),
            "tool_name": body.get("tool_name", "unknown"),
            "action": body.get("action", "unknown"),
            "details": body.get("details", {}),
        }

        check = table.get_item(Key={"sessionId": session_id})
        if "Item" not in check:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Session not found"})
            }

        table.update_item(
            Key={"sessionId": session_id},
            UpdateExpression="SET usage_logs = list_append(if_not_exists(usage_logs, :empty), :entry)",
            ExpressionAttributeValues={
                ":entry": [usage_entry],
                ":empty": []
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True})
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def get_session_data(session_id):
    if not session_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing session_id"})
        }

    try:
        response = table.get_item(Key={"sessionId": session_id})
        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Session not found"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps(convert_decimals(response["Item"]))
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
