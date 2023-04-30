# USAGE.md
## 🚀 Getting Started with AutoPR

This guide will walk you through setting up and using AutoPR, the GitHub Action that automatically writes pull requests in response to issues.

### Prerequisites

Before getting started, ensure you have:

1. A GitHub repository for your project. Alternatively, you can use the [AutoPR-template](https://github.com/irgolic/AutoPR-template/) to create a new repository.
2. An OpenAI API key with access to ChatGPT.

### Setup

Follow these steps to set up AutoPR in your GitHub repository:

1. Create a new file in your repository named `.github/workflows/autopr.yml` and add the contents from [the AutoPR-template workflow YAML file](https://github.com/irgolic/AutoPR-template/blob/main/.github/workflows/autopr.yml).
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

For example, if you don't have access to `gpt-4`, you can set the parameters following the `with:` line in the workflow file to:

```yaml
  - model: gpt-3.5-turbo
  - context_limit: 4096
```

Warning: AutoPR is currently not optimized for `gpt-3.5-turbo`.
See [#65](https://github.com/irgolic/AutoPR/issues/65) for more details.
In the mean time, if you have access to the `gpt-4` API, please use that instead.

#### Inputs

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
- `pull_request_agent_id`: The ID of the planner to use. Defaults to `rail-v1`.
- `codegen_agent_id`: The ID of the code generator to use. Defaults to `rail-v1`.
- `brain_agent_id`: The ID of the brain to use. Defaults to `simple-v1`.
- `pull_request_agent_config`: The configuration for the planner. Empty by default.
- `codegen_agent_config`: The configuration for the code generator. Empty by default.
- `brain_agent_config`: The configuration for the coordinating agent. Empty by default.

#### Agent Configuration Options

Initial Prototype Pull Request Agent and Codegen Agent (`rail-v1`)

- `file_context_token_limit`: The maximum number of tokens in the file context. Defaults to `5000`.
- `file_chunk_size`: How many tokens fit in a file chunk. Defaults to `500`.

Autonomous Codegen Agent (`auto-v1`)

- `context_size`: How many lines around the selected code hunk to include. Defaults to `3`.
- `iterations_per_commit`: The maximum number of thinking steps per commit. Defaults to `5`.
