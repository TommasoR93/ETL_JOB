import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from dotenv import load_dotenv
import os
from config.config import load_config
import time
import pandas as pd
from utils.logging import create_log

load_dotenv()
logger = create_log()

conf = load_config()["API"]
BASE_URL = f"http://api.adzuna.com/v1/api/jobs/{conf.get("country", "")}/search/{conf.get("page", "")}"
params = {
    "app_id" : os.getenv("APP_ID"),
    "app_key" : os.getenv("APP_KEY"),
    "results_per_page" : conf.get("results_per_page", "")
}
last_request_time = 0

def create_session():
    retry_strategy = Retry(
        total=2,
        backoff_factor=1,
        allowed_methods=["GET"],
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def rate_limit(last_request_time, interval = 6 ):   
    now = time.time()
    elapsed = now - last_request_time
    if elapsed < interval:
        time.sleep(interval - elapsed)
    return time.time()

def make_request(session, url, last_request_time, params):    
    last_request_time =  rate_limit(last_request_time)
    response = session.get(url, params=params)
    return response, last_request_time

def pagination(session):
    all_results = []
    page = 1
    last_request_time = 0
    while True:
        response, last_request_time = make_request(session, BASE_URL, last_request_time, params)
        if response.status_code != 200:
            logger.info(f"Error {response.status_code}")       
        data = response.json()
        result = data.get("results", "")
        if not result:
            break
        all_results.extend(result)
        page += 1
        return all_results

def create_df(session):
    result = pagination(session)
    if not result:
        logger.info(f"{result} empty")
    else:
        df = pd.json_normalize(result)
    return df

def main():
    session = create_session()
    logger.info(f"{session} created")
    all_result = pagination(session)
    logger.info(f"{all_result} paginated")
    df = create_df(session)
    logger.info(f"{df} created")
    return df

if __name__ == "__main__":
    main()









