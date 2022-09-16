from setuptools import setup

setup(
    name="prepend_jira_issue",
    version="0.0.1",
    py_modules=["prepend_jira_issue"],
    entry_points={
        "console_scripts": [
            "prepend_jira_issue = prepend_jira_issue:main",
        ],
    },
)
