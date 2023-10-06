import json
from dataclasses import dataclass

import jsonpath
import requests


@dataclass
class Api:
    name: str
    method: str
    url: str
    headers: dict
    reqeust: dict
    response: dict


def send_request(method: str, url: str, headers: dict, data: dict) -> json:
    response = requests.request(method=method, url=url, headers=headers, data=data)
    assert response.status_code == 200
    return response.json()


def from_json(file: str, encoding: str = "utf-8") -> dict:
    with open(file, encoding=encoding) as fd:
        return json.load(fd)


def from_uri(uri: str) -> dict:
    response = requests.get(uri)
    response.raise_for_status()
    return json.loads(response.text)


def get_apis(uris: list[str]) -> list[Api]:
    apis = []
    for uri in uris:
        apis.extend(parse_json(from_uri(uri)))
    return apis


def parse_json(docs: dict) -> list[Api]:
    paths = jsonpath.jsonpath(docs, '$.paths')
    print(jsonpath.jsonpath(docs, '$.paths.*~'))
    for path in paths:
        print(jsonpath.jsonpath(path, '$.*~'))
        for url, info in path.items():
            post = info['post']
            api = Api(
                name=post['summary'],
                method='post',
                url=url,
                headers={},
                reqeust={},
                response={}
            )
            print(api)
            print(post)

    return []
