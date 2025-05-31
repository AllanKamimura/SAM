import json
import logging
import os

import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

eventbridge = boto3.client("events")


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    try:
        # Get environment variable
        EVENT_BUS_NAME = os.getenv("EVENT_BUS_NAME")
        EVENT_SOURCE_NAME = os.getenv("EVENT_SOURCE_NAME")

        if not EVENT_BUS_NAME:
            logger.error("Missing EVENT_BUS_NAME environment variable")
            raise EnvironmentError("EVENT_BUS_NAME environment variable not set")

        if not EVENT_SOURCE_NAME:
            logger.error("Missing EVENT_SOURCE_NAME environment variable")
            raise EnvironmentError("EVENT_SOURCE_NAME environment variable not set")

        # Parse request body
        request_data = json.loads(event.get("body", "{}"))
        logger.info("Parsed request data: %s", request_data)

        # Validate required fields
        required_fields = ["type", "data", "language"]
        missing_fields = [
            field for field in required_fields if field not in request_data
        ]
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Prepare EventBridge event
        params = {
            "Entries": [
                {
                    "Detail": json.dumps(request_data),
                    "DetailType": request_data["type"],
                    "Source": EVENT_SOURCE_NAME,
                    "EventBusName": EVENT_BUS_NAME,
                }
            ]
        }

        # Send event
        response = eventbridge.put_events(**params)
        logger.info("Successfully pushed event to EventBridge")
        logger.debug("EventBridge put_events params: %s", json.dumps(params))
        logger.debug("EventBridge response: %s", response)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "data received", "data": request_data}),
        }

    except Exception as e:
        logger.exception("Error processing event")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error submitting data", "error": str(e)}),
        }
