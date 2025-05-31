import json
import logging

import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Comprehend client
comprehend = boto3.client("comprehend")


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    try:
        detail = event.get("detail")
        if not detail:
            logger.error("Missing 'detail' in event: %s", json.dumps(event))
            raise ValueError("Missing 'detail' in event payload")

        language = detail.get("language")
        text = detail.get("data")

        missing_fields = []
        if not language:
            missing_fields.append("language")
        if not text:
            missing_fields.append("data")

        if missing_fields:
            logger.error(
                "Missing required fields: %s | Detail: %s",
                ", ".join(missing_fields),
                json.dumps(detail),
            )
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        params = {"LanguageCode": language, "Text": text}

        logger.info("Calling Comprehend with: %s", params)
        response = comprehend.detect_sentiment(**params)

        sentiment = response.get("Sentiment")
        logger.info("Detected Sentiment: %s", sentiment)

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "sentiment": sentiment}),
        }

    except Exception as e:
        logger.exception("Error detecting sentiment")
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(e)}),
        }
