# api.py

import requests

def get_data_from_api(url, headers):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, f"Failed to fetch data. Status code: {r.status_code}"
    except Exception as e:
        return None, f"An error occurred: {e}"
