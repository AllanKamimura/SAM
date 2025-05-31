import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

translate = boto3.client("translate")


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    try:
        detail = event.get("detail")
        if not detail:
            logger.error("Event missing 'detail': %s", json.dumps(event))
            raise ValueError("Missing 'detail' in event payload")

        source_lang = "auto"
        target_lang = detail.get("language")
        text = detail.get("data")

        missing_fields = []
        if not target_lang:
            missing_fields.append("language")
        if not text:
            missing_fields.append("data")

        if missing_fields:
            logger.error(
                "Missing required fields in event detail: %s | Detail received: %s",
                ", ".join(missing_fields),
                json.dumps(detail),
            )
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        params = {
            "SourceLanguageCode": source_lang,
            "TargetLanguageCode": target_lang,
            "Text": text,
        }

        logger.info("Calling AWS Translate with: %s", params)
        response = translate.translate_text(**params)

        translated_text = response.get("TranslatedText")
        logger.info("Translated Text: %s", translated_text)

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "translated_text": translated_text}),
        }

    except Exception as e:
        logger.exception("Error during translation")
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(e)}),
        }
