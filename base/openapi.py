import json

import requests
from openapi_parser import parse
from openapi_parser.specification import Specification


def from_json(file: str, encoding: str = "utf-8") -> dict:
    with open(file, encoding=encoding) as fd:
        return json.load(fd)


def from_uri(uri: str) -> dict:
    response = requests.get(uri)
    response.raise_for_status()
    return json.loads(response.text)


def get_apis(uris: list[str]) -> list[Specification]:
    if uris is None or len(uris) == 0:
        print('==init by api-docs.json==')
        return [parse('./base/api-docs.json')]
    specifications = []
    for uri in uris:
        specification = parse(uri)
        specifications.append(specification)
    return specifications
