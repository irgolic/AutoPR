# 🚀 Automatic Pull Request Github Action 🤖

This Github Action automatically writes code in pull requests using GPT-4.
Built with [Guardrails](https://github.com/ShreyaR/guardrails).

## Roadmap

- [X] On new issue, generate code, push a branch, and open a pull request
- [ ] Generate multiple commits
- [ ] Update pull request on new issue/pull request comment
- [ ] Update pull request based on code review comments
- [ ] Alternative code generation models

## Usage

Warning: This Github Action is currently **in development**, and in **alpha release**.
If you're interested in using this action, please reach out on [Discord](https://discord.gg/vz7p9TfHsh).

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
    types: [opened, edited]

permissions:
  contents: write
  issues: read
  pull-requests: write

jobs:
  autopr:
    runs-on: ubuntu-latest
    steps:
    - name: Check if issue is created by owner
      run: |
        if [ "${{ github.event.issue.user.login }}" != "${{ github.repository_owner }}" ]; then
            echo "Issue not created by the owner. Skipping action.";
            exit 78;
          fi
    - name: Checkout
      uses: actions/checkout@v2
      with:
        ref: main
        fetch-depth: 1
    - name: AutoPR
      uses: ./
      with:
        github_token: ${{ secrets.GH_TOKEN }}
        openai_api_key: ${{ secrets.OPENAI_API_KEY }}
        issue_number: ${{ github.event.issue.number }}
        issue_title: ${{ github.event.issue.title }}
        issue_body: ${{ github.event.issue.body }}
        base_branch: main
```

Whenever a new issue is opened or edited, the action will push a branch named `autopr/issue-#` and open a pull request to the base branch.
Please note that if the branch already exists (on issue edit), it will be overwritten.
