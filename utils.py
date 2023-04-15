from typing import Any, Dict
import requests
import os
import sys

from config import retrivalAPI_IP, retrivalAPI_Port

SEARCH_TOP_K = 3

DATABASE_INTERFACE_BEARER_TOKEN = os.environ["BEARER_TOKEN"]


def upsert(id: str, content: str):
    """
    Upload one piece of text to the database.
    """
    url = f"http://{retrivalAPI_IP}:{retrivalAPI_Port}/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + DATABASE_INTERFACE_BEARER_TOKEN,
    }

    data = {
        "documents": [{
            "id": id,
            "text": content,
        }]
    }
    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        print("uploaded successfully.")
    else:
        print(f"Error: {response.status_code} {response.content}")

def build_postgrs_uri(url, port, user, password, db):
    return f"postgresql://{user}:{password}@{url}:{port}/{db}"
