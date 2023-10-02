import pytest

from env import get_config, Config


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", choices=["dev", "sit", "uat"], help="请选择环境")


@pytest.fixture(scope='session')
def config(request, metadata):
    env = request.config.getoption("--env")
    config = get_config(env)
    write_environment(config, metadata)
    return config


def write_environment(config: Config, metadata: dict):
    with open(f'{config.allure_dir}/environment.properties', 'wb') as f:
        kvs = {**config.to_dict(), **metadata}
        for key, value in kvs.items():
            if key not in ['JAVA_HOME', 'Packages', 'Plugins', 'allure_dir']:
                _bytes = (key + '=' + value).encode('unicode_escape') + '\n'.encode('utf-8')
                f.write(_bytes)
