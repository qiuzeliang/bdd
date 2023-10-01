from __future__ import annotations

import glob
import os

from base.feature import Feature, ScenarioTemplate


def get_feature(path: str, encoding: str = "utf-8") -> Feature:
    feature = Feature(
        filename=path,
        name=None,
        description="",
        background=None,
        tags=set(),
        scenarios=list()
    )

    with open(path, encoding=encoding) as f:
        content = f.read()
        feature.parse(content)
    return feature


def get_features(paths: list[str]) -> list[Feature]:
    features = []
    for path in paths:
        if os.path.isdir(path):
            sub_path = glob.iglob(os.path.join(path, "**", "*.feature"), recursive=True)
            features.extend(get_features(list(sub_path)))
        else:
            feature = get_feature(path)
            features.append(feature)
    features.sort(key=lambda f: f.name)
    return features


def get_scenario(paths: list[str]) -> list[ScenarioTemplate]:
    scenarios = []
    for feature in get_features(paths):
        for scenario in feature.scenarios:
            scenarios.append(scenario)
    return scenarios
