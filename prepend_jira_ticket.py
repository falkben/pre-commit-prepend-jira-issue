from __future__ import annotations

import argparse
import re
import subprocess
from typing import Sequence


def run_command(command: str) -> str:
    try:
        stdout: str = subprocess.check_output(command.split()).decode("utf-8").strip()
    except Exception:
        stdout = ""
    return stdout


def get_branch_name() -> str:
    # git rev-parse --abbrev-ref HEAD
    #   returns HEAD if in detatched state
    # git symbolic-ref --short HEAD
    #   returns fatal: ref HEAD is not a symbolic ref if in detatched state
    return run_command("git symbolic-ref --short HEAD")


def extract_jira_issue(message: str) -> str | None:
    project_key, issue_number = r"[A-Z]{2,}", r"[0-9]+"
    match = re.search(f"{project_key}-{issue_number}", message)
    if match:
        # todo: what if there's more than one?
        return match.group(0)
    return None


def get_commit_msg(commit_msg_filepath: str) -> str:
    with open(commit_msg_filepath) as f:
        msg = f.read()
    return msg


def write_commit_msg(commit_msg_filepath: str, commit_msg: str):
    with open(commit_msg_filepath, "w") as f:
        f.write(commit_msg)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath", type=str)

    args = parser.parse_args(argv)

    # todo: ignore merge requests

    git_branch_name = get_branch_name()
    branch_jira_issue = extract_jira_issue(git_branch_name)

    # if no jira issue in branch name, exit
    if branch_jira_issue is None:
        return 0

    commit_msg = get_commit_msg(args.commit_msg_filepath)

    # check if commit message already has the jira ticket in it's name
    commit_msg_jira_issue = extract_jira_issue(commit_msg)
    # if jira issue already in commit message, nothing to do
    if commit_msg_jira_issue and branch_jira_issue == commit_msg_jira_issue:
        return 0

    # prepend the jira ticket to the commit message if it's missing
    new_commit_msg = f"{branch_jira_issue}: {commit_msg}"
    write_commit_msg(args.commit_msg_filepath, new_commit_msg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
