from dataclasses import dataclass

from openapi_parser.specification import Specification

from base.openapi import get_apis


@dataclass
class Config:
    env: str
    base_url: str
    specifications: list[Specification]
    allure_dir: str = './allure-results'

    def __init__(self, env: str, base_url: str, api_docs: list[str]):
        self.env = env
        self.base_url = base_url
        self.specifications = get_apis(api_docs)

    def to_dict(self) -> dict:
        return {
            u'目标环境': self.env,
            u'服务地址': self.base_url
        }


dev_config = Config(
    env='开发环境',
    base_url="http://dev:8080/",
    api_docs=["http://localhost:8080/v3/api-docs"]
)

sit_config = Config(
    env='测试环境',
    base_url="http://sit:8080/",
    api_docs=[]
)

uat_config = Config(
    env='验收环境',
    base_url="http://uat:8080/",
    api_docs=["http://localhost:8080/v3/api-docs"]
)

configs = {
    'dev': dev_config,
    'sit': sit_config,
    'uat': uat_config
}


def get_config(env: str) -> Config:
    config = configs.get(env)
    return config
