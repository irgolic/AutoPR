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
    - name: Install jq
      run: sudo apt-get install jq
    - name: Check if issue is created by collaborator
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        is_collaborator=$(curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
          "https://api.github.com/repos/${{ github.repository }}/collaborators/${{ github.event.issue.user.login }}" | jq -r '.message')

        if [ "$is_collaborator" == "Not Found" ]; then
          echo "Issue not created by a collaborator. Skipping action."
          exit 78
        fi
    - name: Checkout
      uses: actions/checkout@v2
      with:
        ref: main
        fetch-depth: 1
    - name: AutoPR
      uses: ./
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        openai_api_key: ${{ secrets.OPENAI_API_KEY }}
        issue_number: ${{ github.event.issue.number }}
        issue_title: ${{ github.event.issue.title }}
        issue_body: ${{ github.event.issue.body }}
        base_branch: main

```

Whenever a new issue is opened or edited, the action will push a branch named `autopr/issue-#` and open a pull request to the base branch.
Please note that if the branch already exists (on issue edit), it will be overwritten.
