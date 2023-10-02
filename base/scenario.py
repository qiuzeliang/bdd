import allure
import pytest

from env import Config
from base.feature import ScenarioTemplate
from base.features import get_scenario


class BDD:
    scenarios = get_scenario(["./feature"])

    @pytest.mark.parametrize('scenario', scenarios, ids=[scenario.name for scenario in scenarios])
    def run_scenario(self, scenario: ScenarioTemplate, config: Config):
        self._set_allure(scenario)
        for step in scenario.steps:
            with allure.step(step.name):
                print(step.keyword)

    def _set_allure(self, scenario: ScenarioTemplate):
        allure.dynamic.parent_suite(scenario.feature.name)
        allure.dynamic.suite(scenario.feature.description)
        allure.dynamic.sub_suite(scenario.name)
        allure.dynamic.feature(scenario.feature.name)
        allure.dynamic.story(scenario.feature.description)
        allure.dynamic.title(scenario.name)
        if scenario.description:
            allure.dynamic.description(scenario.description)
        for tag in scenario.tags:
            allure.dynamic.tag(tag)
