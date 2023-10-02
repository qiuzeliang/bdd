import argparse
import glob
import json
import os
import shutil

import pytest

from base.openapi import from_json, parse_json
from env import get_config, configs


def fix_allure_results(path: str):
    files = glob.iglob(os.path.join(path, "**", "*.json"), recursive=True)
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "parameters" in data:
                del data["parameters"]
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f)


if __name__ == '__main__':
    print(parse_json(from_json('./base/api-docs.json')))
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, required=True, default='dev', choices=configs.keys())
    args = parser.parse_args()
    config = get_config(args.env)
    pytest.main(['--env', args.env, '--clean-alluredir', f'--alluredir={config.allure_dir}'])
    fix_allure_results(config.allure_dir)
    shutil.copy('categories.json', config.allure_dir)
    os.system(f'allure generate {config.allure_dir} --clean -o ./report')
