import logging
import os

from blossom_ai import (APIError, AuthenticationError, Blossom, BlossomError,
                        NetworkError, RateLimitError, ValidationError,)
from dotenv import load_dotenv


load_dotenv()
ai = Blossom(api_token=os.getenv("TOKEN_AI"))

async def text_generated(message_list: str):
    try:
        response = await ai.text.chat(
            messages=message_list)
        return response
    except AuthenticationError as e:
        logging.error(f"Auth failed: {e.message}")
        logging.info(f"Suggestion: {e.suggestion}")
        # Output: Visit https://auth.pollinations.ai to get an API token

    except ValidationError as e:
        logging.error(f"Invalid parameter: {e.message}")
        logging.info(f"Context: {e.context}")

    except NetworkError as e:
        logging.error(f"Connection issue: {e.message}")
        logging.info(f"Suggestion: {e.suggestion}")

    except RateLimitError as e:
        logging.error(f"Too many requests: {e.message}")

    except APIError as e:
        logging.error(f"API error: {e.message}")
        logging.info(f"Status: {e.context.status_code if e.context else 'unknown'}")

    except BlossomError as e:
        # Catch-all for any Blossom error
        logging.error(f"Error type: {e.error_type}")
        logging.info(f"Message: {e.message}")
        logging.info(f"Suggestion: {e.suggestion}")
        if e.original_error:
            logging.error(f"Original error: {e.original_error}")



