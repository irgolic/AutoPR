# Automatic Pull Request Github Action 🎉🚀

## Input Variables

The input variables for this Github Action are documented in `action.yml`. They include:

- `github_token`
- `openai_api_key`
- `issue_number`
- `issue_title`
- `issue_body`
- `base_branch`

## Guardrails Library

This Github Action utilizes the guardrails library, which can be found in `generation_service.py` and `validators.py`. The library helps in generating and validating pull requests based on the input variables and the codebase.

## Including the Github Action in Your Repository

To include the Automatic Pull Request Github Action in your own repository, add its configuration to your `.github/workflows` directory. Follow the documentation in `action.yml` for further guidance.
- `GITHUB_TOKEN` - The GitHub token to use for the action. This is automatically provided by GitHub, you do not need to create your own token.
