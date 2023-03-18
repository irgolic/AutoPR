# 🚀 Automatic Pull Request Github Action 🤖

The following input variables are documented in the `action.yml` file:

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
      - edited

jobs:
  autopr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Automatic Pull Request
        uses: ./
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          issue_number: ${{ github.event.issue.number }}
          issue_title: ${{ github.event.issue.title }}
          issue_body: ${{ github.event.issue.body }}
```

## Environment Variables

- `GITHUB_TOKEN` - The GitHub token to use for the action. This is automatically provided by GitHub, you do not need to create your own token.
