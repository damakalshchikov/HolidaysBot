import requests
from requests import Response
import logging
from logging import Logger

import load_data

logger: Logger = logging.getLogger(__name__)


def fetch_holidays(params: dict) -> dict:
    url: str = load_data.api.base_url
    params["api_key"]: dict[str: str] = load_data.api.key

    logger.info(f"Requesting URL: {url}. Params: {params}")

    response: Response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        error_message: str = response.text
        logging.error(f"API error {response.status_code}: {error_message}")
        return {}

