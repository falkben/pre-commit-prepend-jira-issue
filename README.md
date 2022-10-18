# pre-commit prepend jira issue

A [pre-commit](https://pre-commit.com/) hook to prepend a Jira issue to a commit message, extracted from the current branch name.

With this hook installed, when you commit, if a Jira issue is found in your branch name, and a Jira issue is not already included in your commit message, the Jira issue from the branch name will be prepended to your commit message.

## Install

1. Install [`pre-commit`](https://pre-commit.com/) if it's not already installed

    Globally with [`pipx`](https://github.com/pypa/pipx):

    ```command
    pipx install pre-commit
    ```

    Or any of the ways mentioned in the pre-commit [installation docs](https://pre-commit.com/#installation).

2. Add this hook to your `.pre-commit-config.yaml` file (create in root directory if it doesn't exist already).

    ```yaml
    repos:
    - repo: https://github.com/falkben/pre-commit-prepend-jira-issue
        rev: v0.0.1
        hooks:
        - id: prepend-jira-issue
          stages: [commit-msg]
    ```

3. Install this hook

    ```command
    pre-commit install --hook-type commit-msg
    ```

4. Commit the `.pre-commit-config.yaml` to your repo.

## License

[MIT](LICENSE)

## Inspiration

1. <https://github.com/radix-ai/auto-smart-commit>
2. <https://agussarwono.com/article/add-ticket-to-your-commit/>
3. <https://github.com/erskaggs/jira-pre-commit>

## Developer Notes

### Install for local dev

Create virtual environment then install:

```bash
pip install -r dev-requirements.txt
pip install -e ".[dev]"
```

## Create dev dependency lock file

```bash
pip-compile --extra dev -o dev-requirements.txt pyproject.toml
```
