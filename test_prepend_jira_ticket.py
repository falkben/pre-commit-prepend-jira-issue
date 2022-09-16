import pytest

import prepend_jira_issue


@pytest.mark.parametrize(
    ("content", "expected"),
    (
        ("ABC-1111", "ABC-1111"),
        ("A-1111", None),
        ("ABC-1", "ABC-1"),
        ("abc 1111", None),
        ("two little bears, sitting in chairs", None),
        ("and a bowl of much 123-ABC", None),
        ("and a little old lady CDE-123", "CDE-123"),
        ("CDE-123: and a little old lady ", "CDE-123"),
        ("ZYX-123-321-ABC", "ZYX-123"),
        ("ZYX-123-ABC-321", "ZYX-123"),
        ("ZYX-ABC-321-123", "ABC-321"),
    ),
)
def test_extract_jira_issue(content, expected):
    output = prepend_jira_issue.extract_jira_issue(content)
    assert output == expected
