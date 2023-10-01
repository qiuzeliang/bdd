import glob
import json
import os
import shutil

import pytest


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
    allure_dir = './allure-results'
    pytest.main([f'--clean-alluredir, --alluredir={allure_dir}'])
    fix_allure_results(allure_dir)
    shutil.copy('categories.json', allure_dir)
    os.system(f'allure generate {allure_dir} --clean -o ./report')