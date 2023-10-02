import json
from dataclasses import dataclass, field

import requests
from dataclasses_json import dataclass_json


@dataclass
class Info:
    title: str


@dataclass_json
@dataclass
class Server:
    url: str
    description: str


@dataclass_json
@dataclass
class Tag:
    name: str
    description: str


@dataclass_json
@dataclass
class Properties:
    type: str
    description: str
    format: str
    enum: list[str]


@dataclass
class Schema:
    name: str
    properties: dict[str, Properties]


@dataclass
class MediaType:
    schema: Schema


@dataclass
class Content:
    content: dict[str, MediaType]


@dataclass
class RequestBody:
    content: Content
    description: str = field(default_factory=str)
    required: bool = field(default_factory=bool)


@dataclass
class Response:
    description: str
    content: Content


@dataclass
class Responses:
    response: dict[str, Response]


@dataclass
class PathItem:
    method: str
    tags: list[str]
    summary: str
    description: str
    requestBody: RequestBody
    responses: Responses | None


@dataclass
class Path:
    paths: dict[str, PathItem]


@dataclass
class Components:
    schemas: dict[str, Schema]


@dataclass
class Api:
    version: str
    info: Info
    servers: list[Server]
    tags: list[Tag]
    path: Path
    components: Components


def from_json(file: str, encoding: str = "utf-8") -> dict:
    with open(file, encoding=encoding) as fd:
        return json.load(fd)


def from_uri(uri: str) -> dict:
    response = requests.get(uri)
    response.raise_for_status()
    return json.loads(response.text)


def get_apis(uris: list[str]) -> list[Api]:
    apis = []
    for uris in uris:
        content = from_uri(uris)
        api = parse_json(content)
        apis.append(api)
    return apis


def parse_json(docs: dict) -> Api:
    paths = {}
    for name, path in docs['paths'].items():
        path_item = PathItem(
            method='post',
            tags=path['post']['tags'],
            summary=path['post']['summary'],
            description=path['post']['description'],
            requestBody=RequestBody(
                description=path['post']['requestBody'].get('description', ''),
                required=path['post']['requestBody']['required'],
                content=Content(
                    content={path['post']['requestBody']['content']: MediaType(
                        schema=S
                    )}
                )
            ),
            responses=None
        )
        paths[name] = path_item
    schemas = {}
    for name, schema in docs['components']['schemas'].items():
        _schema = Schema(name=name, properties={})
        for _field, properties in schema['properties'].items():
            _properties = Properties(
                type=properties['type'],
                format=properties['format'],
                description=properties.get('description', ''),
                enum=properties.get('enum', []))
            _schema.properties[_field] = _properties
        schemas[name] = _schema

    return Api(
        version=docs['openapi'],
        info=Info(title=docs['info']['title']),
        servers=[Server.from_dict(server) for server in docs['servers']],
        tags=[Tag.from_dict(tag) for tag in docs['tags']],
        path=Path(paths=paths),
        components=Components(schemas=schemas)
    )
