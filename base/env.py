from dataclasses import dataclass


@dataclass
class Config:
    env: str
    base_url: str

    def to_dict(self) -> dict:
        return {
            u'目标环境': self.env,
            u'服务地址': self.base_url
        }


configs = {
    'dev': Config(env='开发环境', base_url="http://dev:8080/"),
    'sit': Config(env='测试环境', base_url="http://sit:8080/"),
    'uat': Config(env='验收环境', base_url="http://uat:8080/")
}


def get_config(env: str) -> Config:
    config = configs.get(env)
    return config
