from pathlib import Path

import pytest

import prepend_jira_issue

LONG_COMMIT_MSG = """\
spanning many lines

a very long commit message

i am a haiku
"""
SHORT_COMMIT_MSG = "a short commit msg"
COMMENTED_COMMIT_MSG = """\
This is the commit message

Not the stuff below
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch ABC-111
# Untracked files:
#	a-file.txt
#
"""


@pytest.fixture
def create_commit_msg_file(tmp_path: Path):
    """Fixture factory for creating a commit message file

    Defaults to creating a file containing short commit message but can pass in a custom
    commit message

    Ex:

    ```python
    def test_get_commit_msg_long(create_commit_msg_file):
        long_commit_msg_file = create_commit_msg_file(LONG_COMMIT_MSG)
    ```
    """

    def _commit_msg_file(
        commit_msg: str = SHORT_COMMIT_MSG,
    ):

        f = tmp_path / "commit_msg"
        f.write_text(commit_msg)
        return str(f)

    yield _commit_msg_file


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


def test_get_commit_msg_long(create_commit_msg_file):
    long_commit_msg_file = create_commit_msg_file(LONG_COMMIT_MSG)

    msg = prepend_jira_issue.get_commit_msg(long_commit_msg_file)
    assert msg == LONG_COMMIT_MSG


def test_get_commit_msg_short(create_commit_msg_file):
    short_commit_msg_file = create_commit_msg_file(SHORT_COMMIT_MSG)

    msg = prepend_jira_issue.get_commit_msg(short_commit_msg_file)
    assert msg == SHORT_COMMIT_MSG


def test_get_commit_msg_commented(create_commit_msg_file):
    commented_commit_msg_file = create_commit_msg_file(COMMENTED_COMMIT_MSG)

    expected_msg = """\
This is the commit message

Not the stuff below
"""

    msg = prepend_jira_issue.get_commit_msg(commented_commit_msg_file)
    assert msg == expected_msg


def test_prepend_jira_issue_short_msg():
    issue = "some_issue"
    new_msg = prepend_jira_issue.prepend_jira_issue(SHORT_COMMIT_MSG, issue)

    assert new_msg == f"some_issue: {SHORT_COMMIT_MSG}"


def test_prepend_jira_issue_long_msg():
    issue = "some_issue"
    new_msg = prepend_jira_issue.prepend_jira_issue(LONG_COMMIT_MSG, issue)

    assert new_msg == f"some_issue: {LONG_COMMIT_MSG}"
