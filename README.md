# 🚀 Automatic Pull Request Github Action 🤖

This Github Action automatically writes code in pull requests using GPT-4.

## Roadmap

Features:
- [X] On new issue, generate code, push a branch, and open a pull request
- [ ] Generate multiple commits
- [ ] Update pull request on new issue/pull request comment
- [ ] Update pull request based on code review comments
- [ ] Update pull request based on code review comments

## Usage

**This Github Action is currently in development.**

The following input variables are used by the action:

- `github_token`: The GitHub token to use for the action. This is automatically provided by GitHub, you do not need to create your own token.
- `openai_api_key`: The OpenAI API key to use for generating the pull request.
- `issue_number`: The issue number associated with the pull request.
- `issue_title`: The title of the issue.
- `issue_body`: The body of the issue.
- `base_branch`: The base branch for the pull request. The default value is 'main'.

To include this Github action in your own repository, you can use the following example in your workflow file:

```yaml
on:
  issues:
    types:
      - opened

jobs:
  autopr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Automatic Pull Request
        uses: irgolic/autopr@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          issue_number: ${{ github.event.issue.number }}
          issue_title: ${{ github.event.issue.title }}
          issue_body: ${{ github.event.issue.body }}
```

Whenever a new issue is opened, the action will push a branch named `autopr/issue-#` and open a pull request to the base branch.