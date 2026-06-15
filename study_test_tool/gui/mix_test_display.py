"""Shared display helpers for mixed-test UI."""

from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from models.test import Test

UNGROUPED_LABEL = "Ungrouped"


@dataclass(frozen=True)
class MixTestDisplay:
    """Display metadata for a mixed test."""

    title: str
    subtitle: str


def _plural(count: int, singular: str, plural: Optional[str] = None) -> str:
    """Return a count with a singular/plural noun."""
    noun = singular if count == 1 else plural or f"{singular}s"
    return f"{count} {noun}"


def build_mix_test_display(
    selected_tests: List[Test],
    all_tests_with_counts: List[Tuple[Test, int]],
    question_count: int,
) -> MixTestDisplay:
    """Build concise title/subtitle text for a mixed test."""
    selected_by_group: Dict[str, List[Test]] = OrderedDict()
    available_by_group: Dict[str, int] = {}

    for test, _ in all_tests_with_counts:
        group = test.group_name.strip() if test.group_name else UNGROUPED_LABEL
        available_by_group[group] = available_by_group.get(group, 0) + 1

    for test in selected_tests:
        group = test.group_name.strip() if test.group_name else UNGROUPED_LABEL
        selected_by_group.setdefault(group, []).append(test)

    group_names = list(selected_by_group.keys())
    named_groups = sorted(group for group in group_names if group != UNGROUPED_LABEL)
    has_ungrouped = UNGROUPED_LABEL in selected_by_group
    bucket_count = len(named_groups) + (1 if has_ungrouped else 0)
    selected_test_count = len(selected_tests)

    if bucket_count == 1 and named_groups:
        title = f"{named_groups[0]} Mixed Test"
    elif bucket_count == 2 and len(named_groups) == 2 and not has_ungrouped:
        title = f"{named_groups[0]} + {named_groups[1]} Mixed Test"
    elif bucket_count <= 2 and len(named_groups) == 1:
        title = f"{named_groups[0]} Mixed Test"
    elif bucket_count >= 3:
        title = "Mixed Review"
    else:
        title = "Mixed Test"

    if bucket_count == 1 and named_groups:
        group = named_groups[0]
        selected_in_group = len(selected_by_group[group])
        available_in_group = available_by_group.get(group, selected_in_group)
        if selected_in_group < available_in_group:
            scope = f"{selected_in_group} of {available_in_group} tests in {group}"
        else:
            scope = f"{_plural(selected_in_group, 'test')} in {group}"
        subtitle = f"{_plural(question_count, 'question')} from {scope}"
    elif bucket_count <= 1:
        subtitle = (
            f"{_plural(question_count, 'question')} from "
            f"{_plural(selected_test_count, 'test')}"
        )
    else:
        subtitle = (
            f"{_plural(question_count, 'question')} from "
            f"{_plural(bucket_count, 'group')} and "
            f"{_plural(selected_test_count, 'test')}"
        )

    return MixTestDisplay(title=title, subtitle=subtitle)


def group_tests_by_name(
    tests_with_counts: List[Tuple[Test, int]],
) -> List[Tuple[str, List[Tuple[Test, int]]]]:
    """Organize tests by group name with ungrouped tests last."""
    groups: "OrderedDict[str, List[Tuple[Test, int]]]" = OrderedDict()
    ungrouped: List[Tuple[Test, int]] = []

    for test, count in tests_with_counts:
        if test.group_name:
            groups.setdefault(test.group_name, []).append((test, count))
        else:
            ungrouped.append((test, count))

    result: List[Tuple[str, List[Tuple[Test, int]]]] = [
        (name, groups[name]) for name in sorted(groups.keys())
    ]
    if ungrouped:
        result.append((UNGROUPED_LABEL, ungrouped))
    return result
