from __future__ import annotations

import argparse
import re
import subprocess
from typing import Sequence


def run_command(command: str) -> str:
    """Run a command and return its output

    If the command fails, return an empty string"""

    try:
        stdout: str = subprocess.check_output(command.split()).decode("utf-8").strip()
    except Exception:
        stdout = ""
    return stdout


def get_branch_name() -> str:
    # git rev-parse --abbrev-ref HEAD
    #   returns HEAD if in detached state
    # git symbolic-ref --short HEAD
    #   returns fatal: ref HEAD is not a symbolic ref if in detached state
    return run_command("git symbolic-ref --short HEAD")


def extract_jira_issue(content: str) -> str | None:
    project_key, issue_number = r"[A-Z]{2,}", r"[0-9]+"
    match = re.search(f"{project_key}-{issue_number}", content)
    if match:
        return match.group(0)
    return None


def get_commit_msg(commit_msg_filepath: str) -> str:
    """Get the commit message

    Ignore comment lines as those aren't included in the commit message
    """

    # todo: instead of removing comment lines from the commit message, we should instead
    # skip them in our regex search
    with open(commit_msg_filepath) as f:
        msg = ""
        for line in f:
            if not line.startswith("#"):
                msg += line
    return msg


def prepend_jira_issue(msg: str, issue: str) -> str:
    return f"{issue}: {msg}"


def write_commit_msg(commit_msg_filepath: str, commit_msg: str) -> None:
    with open(commit_msg_filepath, "w") as f:
        f.write(commit_msg)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath", type=str)

    args = parser.parse_args(argv)

    git_branch_name = get_branch_name()
    branch_jira_issue = extract_jira_issue(git_branch_name)

    # if no jira issue in branch name, exit
    if branch_jira_issue is None:
        return 0

    commit_msg = get_commit_msg(args.commit_msg_filepath)

    # ignore merge requests
    if re.match("^Merge commit '", commit_msg):
        return 0

    # check if commit message already has a jira issue in it's name
    commit_msg_jira_issue = extract_jira_issue(commit_msg)
    # if jira issue already in commit message, skip
    if commit_msg_jira_issue:
        return 0

    new_commit_msg = prepend_jira_issue(commit_msg, branch_jira_issue)

    write_commit_msg(args.commit_msg_filepath, new_commit_msg)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
