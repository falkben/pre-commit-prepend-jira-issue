# pre-commit prepend jira issue

A [pre-commit](https://pre-commit.com/) hook to prepend a Jira issue to a commit message, extracted from the current branch name.

## Usage

1. Install [`pre-commit`](https://pre-commit.com/) if it's not already installed

    Globally with [`pipx`](https://github.com/pypa/pipx):

    ```command
    pipx install pre-commit
    ```

    Or one of the ways mentioned in the pre-commit [installation docs](https://pre-commit.com/#installation).

2. Add this hook to your `.pre-commit-config.yaml` file.

    ```yaml
    repos:
    - repo: https://github.com/falkben/pre-commit-prepend-jira-issue
        rev: v0.0.1
        hooks:
        - id: prepend-jira-issue
            stages: [commit-msg]
    ```

3. Install the hook

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

todo
