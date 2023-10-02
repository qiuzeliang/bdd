import json

import requests


def send_request(method: str, url: str, headers: dict, data: dict) -> json:
    response = requests.request(method=method, url=url, headers=headers, data=data)
    assert response.status_code == 200
    return response.json()
