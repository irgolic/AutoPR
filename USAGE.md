# USAGE.md
## 🚀 Getting Started with AutoPR

This guide will walk you through setting up and using AutoPR, the GitHub Action that automatically writes pull requests in response to issues.

### Prerequisites

Before getting started, ensure you have:

1. A GitHub repository for your project. You can use the [AutoPR-template](https://github.com/irgolic/AutoPR-template/) to create a new repository.
2. An OpenAI API key with access to ChatGPT.

### Setup

Follow these steps to set up AutoPR in your GitHub repository:

1. Create a new file in your repository named `.github/workflows/autopr.yml` and copy the contents from [the AutoPR-template workflow YAML file](https://github.com/irgolic/AutoPR-template/blob/main/.github/workflows/autopr.yml).
2. Configure the action as necessary (see [Customization](#customization) below).
3. In your GitHub repository settings, navigate to `Secrets and variables -> Actions` and add your OpenAI API key as `OPENAI_API_KEY`.
4. In your GitHub repository settings, go to `Actions -> General` and scroll down to `Workflow permissions`. Enable `Allow GitHub Actions to create and approve pull requests`.
5. Create a label in your repository that contains the string "AutoPR" (e.g., "Run AutoPR 🚀" or simply "AutoPR").

### Usage

To use AutoPR, follow these steps:

1. Create a new issue in your GitHub repository with a clear and concise description of the task or bug fix.
2. Add the AutoPR label to the issue. This will trigger the AutoPR workflow.
3. Once the action is triggered, it will create a new branch named autopr/issue-# and open a pull request to the base branch. **If the branch already exists, it will be overwritten.**
4. Review the generated pull request and make any necessary adjustments.
5. Merge the pull request into the base branch once you're satisfied with the changes.

### Customization

You can customize the behavior of AutoPR by modifying the `autopr.yml` file in your `.github/workflows` directory. 

#### Using a personal access token (PAT)

The default token (`{{ secrets.GITHUB_TOKEN }}`) does not have permissions to create/edit Github Action Workflow files (located in `.github/workflows`).
The only way to get around this is to create a personal access token (PAT), add it as a secret in your repository, and reference it as a token.

1. Create a [personal access token](https://github.com/settings/tokens?type=beta) with the `Contents`, `Issues`, `Pull requests`, `Workflows` scopes.
2. Add the token as a secret in your repository (for example, named `PAT`).
3. Set it in the `github_token` parameter, for example: 

```yaml
    - name: AutoPR
      uses: docker://ghcr.io/irgolic/autopr:latest
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      with:
        github_token: ${{ secrets.PAT }}`
```

#### Using a different model

For example, if you don't have access to `gpt-4`, you can set the parameters following the `with:` line at the end of the workflow file to:

```yaml
    - name: AutoPR
      uses: docker://ghcr.io/irgolic/autopr:latest
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        model: 'gpt-3.5-turbo'
        context_limit: 4096
```

Warning: AutoPR is currently not optimized for `gpt-3.5-turbo`.
See [#65](https://github.com/irgolic/AutoPR/issues/65) for more details.
In the mean time, if you have access to the `gpt-4` API, please use that instead.
Please note that ChatGPT Plus does not give you access to the `gpt-4` API; 
you need to sign up on [the GPT-4 API waitlist](https://openai.com/waitlist/gpt-4-api). 

#### All customization options

- `github_token`: The action's GitHub token (`{{ secrets.GITHUB_TOKEN }}`). Required.
- `base_branch`: The base branch for the pull request. Defaults to `main`.
- `model`: The name of the OpenAI chat model to use. Defaults to `gpt-4`.
- `context_limit`: The maximum size of the context window to use, varies depending on the model and preference. Defaults to `8192`.
- `min_tokens`: The minimum number of tokens to be made available for generation. Defaults to `1000`.
- `max_tokens`: The maximum number of tokens to generate. Defaults to `2000`.
- `num_reasks`: The number of times to re-ask the model in file exploration and commit generation. Defaults to `2`.
- `target_branch_name_template`: The template for the name of the target branch. Defaults to `autopr/{issue_number}`.
- `temperature`: The temperature for the model. Defaults to `0.9`.
- `rail_temperature`: The temperature for the guardrails calls. Defaults to `0.9`.
- `agent_id`: The ID of the agent to use. Defaults to `plan_and_code`.
- `agent_config`: The configuration for the agent. Empty by default.
- `overwrite_existing`: Whether to overwrite the branch being generated for the issue instead of always making a new pull request. Defaults to `false`.

Specify `agent_config` as a yaml string, e.g.:

```yaml
...
    - name: AutoPR
      uses: docker://ghcr.io/irgolic/autopr:latest
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        agent_config: |
          planning_actions: 
          - plan_pull_request
...
```

#### Agent Configuration Options

The `plan_and_code` agent has the following configuration options:

- `planning_actions`: The actions to run to plan the pull request. Defaults to `plan_pull_request` and `request_more_information`
- `codegen_actions`: The actions to run to generate the pull request. Defaults to `new_file` and `edit_file`.
- `max_codegen_iterations`: The maximum number of iterations to run the code generation actions for. Defaults to `5`.
