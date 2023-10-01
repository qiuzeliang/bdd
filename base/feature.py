from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Sequence

FEATURE = "feature"
SCENARIO_OUTLINE = "scenario outline"
EXAMPLES = "examples"
SCENARIO = "scenario"
BACKGROUND = "background"
GIVEN = "given"
WHEN = "when"
THEN = "then"
TAG = "tag"

STEP_TYPES = (GIVEN, WHEN, THEN)

STEP_PREFIXES = [
    ("Feature: ", FEATURE),
    ("Scenario Outline: ", SCENARIO_OUTLINE),
    ("Examples:", EXAMPLES),
    ("Scenario: ", SCENARIO),
    ("Background:", BACKGROUND),
    ("Given ", GIVEN),
    ("When ", WHEN),
    ("Then ", THEN),
    ("@", TAG),
    ("And ", None),
    ("But ", None),
]


@dataclass
class Step:
    type: str
    name: str
    keyword: str


@dataclass
class Background:
    name: str | None
    steps: list[Step] = field(default_factory=list)

    def add_step(self, step: Step) -> None:
        self.steps.append(step)


@dataclass
class Examples:
    name: str | None = field(default=None)
    examples: list[Sequence[str]] = field(init=False, default_factory=list)

    def add_example(self, values: Sequence[str]) -> None:
        self.examples.append(values)


@dataclass
class ScenarioTemplate:
    feature: Feature
    templated: bool
    name: str
    steps: list[Step] = field(default_factory=list)
    tags: set[str] = field(default_factory=set)
    description: list[str] = field(default_factory=list)
    examples: Examples = field(default_factory=lambda: Examples())

    def add_step(self, step: Step) -> None:
        self.steps.append(step)


@dataclass
class Feature:
    filename: str
    name: str | None
    description: str
    background: Background | None
    tags: set[str]
    scenarios: list[ScenarioTemplate]

    def parse(self, content: str) -> None:
        prev_line = None
        prev_mode = None
        mode = None

        for line in content.splitlines():
            clean_line = strip_comments(line)
            if not clean_line:
                continue

            mode = get_step_type(clean_line) or mode
            keyword, parsed_line = parse_line(clean_line)

            if mode == FEATURE:
                if prev_mode is None:
                    self.name = parsed_line
                    self.tags = get_tags(prev_line)
                    prev_mode = mode
                elif prev_mode == FEATURE:
                    if not parsed_line.strip().startswith("#"):
                        self.description = "\n".join([self.description, parsed_line]).strip()
            elif mode == BACKGROUND:
                self.background = Background(name=parsed_line)
                prev_mode = mode
            elif prev_mode == BACKGROUND and mode in STEP_TYPES:
                self.background.add_step(Step(type=mode, name=parsed_line, keyword=keyword))
            elif mode == SCENARIO:
                if keyword == "Scenario:":
                    self.scenarios.append(ScenarioTemplate(feature=self, templated=False, name=parsed_line, tags=get_tags(prev_line)))
                    prev_mode = mode
                elif prev_mode == SCENARIO:
                    self.scenarios[-1].description.append(parsed_line)
            elif prev_mode == SCENARIO and mode in STEP_TYPES:
                self.scenarios[-1].add_step(Step(type=mode, name=parsed_line, keyword=keyword))
            elif mode == SCENARIO_OUTLINE:
                if keyword == "Scenario Outline:":
                    self.scenarios.append(ScenarioTemplate(feature=self, templated=True, name=parsed_line, tags=get_tags(prev_line)))
                    prev_mode = mode
                elif prev_mode == SCENARIO_OUTLINE:
                    self.scenarios[-1].description.append(parsed_line)
            elif prev_mode == SCENARIO_OUTLINE and mode in STEP_TYPES:
                self.scenarios[-1].add_step(Step(type=mode, name=parsed_line, keyword=keyword))
            elif prev_mode == SCENARIO_OUTLINE and mode == EXAMPLES:
                self.scenarios[-1].examples = Examples(name=parsed_line)
                prev_mode = EXAMPLES
            elif prev_mode == EXAMPLES:
                self.scenarios[-1].examples.add_example([parm for parm in split_line(parsed_line) if parm])

            prev_line = clean_line


def get_tags(line: str | None) -> set[str]:
    if not line or not line.strip().startswith("@"):
        return set()
    return {tag.lstrip("@") for tag in line.strip().split(" @") if len(tag) > 1}


def split_line(line: str) -> list[str]:
    return [cell.replace("\\|", "|").strip() for cell in re.compile(r"(?<!\\)\|").split(line)[1:-1]]


def parse_line(line: str) -> tuple[str, str]:
    for prefix, _ in STEP_PREFIXES:
        if line.startswith(prefix):
            return prefix.strip(), line[len(prefix):].strip()
    return "", line


def strip_comments(line: str) -> str:
    res = re.compile(r"(^|(?<=\s))#").search(line)
    if res:
        line = line[: res.start()]
    return line.strip()


def get_step_type(line: str) -> str | None:
    for prefix, _type in STEP_PREFIXES:
        if line.startswith(prefix):
            return _type
    return None
