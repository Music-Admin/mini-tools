import json
from file_manager.handlers import handle_file
from royalty_compressor.handlers import handle_compression
from session_manager.handlers import handle_session

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://tools.musicadmin.com",
    "http://mini-tools-react.s3-website-us-east-1.amazonaws.com",
    "https://www.musicadmin.com",  # ✅ Add this
    "https://musicadmin.com",      # ✅ (optional, in case user drops www)
]

def get_origin(event):
    headers = event.get("headers", {}) if isinstance(event, dict) else {}
    return headers.get("origin") or headers.get("Origin")

def cors_options_response(origin):
    if origin in ALLOWED_ORIGINS:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json",
            },
            "body": json.dumps({"message": "CORS preflight OK"}),
        }
    else:
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Origin not allowed"}),
        }

def lambda_handler(event, context):
    try:
        path = event["path"]
        method = event["httpMethod"]
        origin = get_origin(event)

        # Global CORS preflight handler
        if method == "OPTIONS":
            return cors_options_response(origin)

        # Route request
        if path.startswith("/file-manager/"):
            response = handle_file(event, context)
        elif path.startswith("/royalty-compressor/"):
            response = handle_compression(event, context)
        elif path.startswith("/session-manager/"):
            response = handle_session(event, context)
        else:
            response = {
                "statusCode": 404,
                "body": json.dumps({"error": "Not Found"})
            }

        # Inject global CORS headers into final response
        if isinstance(response, dict):
            headers = response.get("headers", {})
            if origin in ALLOWED_ORIGINS:
                headers["Access-Control-Allow-Origin"] = origin
                headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,OPTIONS"
                headers["Access-Control-Allow-Headers"] = "Content-Type"
            headers["Content-Type"] = "application/json"
            response["headers"] = headers
        return response

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "trace": True
            })
        }
