import os
import time
import logging
import json
from groq import Groq
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return Groq(api_key=api_key)


def call_groq(messages, temperature=0.3, max_tokens=1000, retries=3):
    client = get_client()
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"Calling Groq API — attempt {attempt + 1} of {retries}")
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            result = response.choices[0].message.content
            logger.info("Groq API call successful")
            return result
        except Exception as e:
            attempt += 1
            wait_time = 2 ** attempt
            logger.error(f"Groq API error on attempt {attempt}: {str(e)}")
            if attempt < retries:
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("All retry attempts failed. Returning None.")
                return None


def parse_json_response(raw_response):
    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"JSON parsing failed: {str(e)}")
        logger.error(f"Raw response was: {raw_response}")
        return None