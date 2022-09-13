from __future__ import annotations

import argparse
from typing import Sequence


def get_branch_name():
    # $(git rev-parse --abbrev-ref HEAD)
    ...


def extract_ticket_from_branch_name():
    # regex: '([A-Z]+-[0-9])'
    ...


def get_commit_msg():
    ...


def check_commit_msg_for_ticket():
    ...


def prepend_jira_ticket_to_commit_msg():
    ...


# todo: ignore merge requests

# get the branch name
# extract a jira ticket from the branch name
# if there is a jira ticket name then...
# get the commit message
# check if commit message already has the jira ticket in it's name
# prepend the jira ticket to the commit message if it's missing

# todo: on error exit 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

    args = parser.parse_args(argv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
