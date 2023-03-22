# 🤖👨‍💻 Automatic Pull Request Github Action 


This Github Action automatically writes code in pull requests using GPT-4.
Built with [Guardrails](https://github.com/ShreyaR/guardrails).

## 💪 How does it work?

The action triggers when a new issue is created or edited by a repository collaborator.

1. We ask the model what files in the repo are relevant to the issue
2. We iteratively show it files, and ask it to write down notes about them
3. We ask it to write a pull request title, body, and outline a list of commits (also specifying relevant files)
4. For each commit, we ask it to generate a diff given the relevant files

## 📍 Roadmap

- [X] On new/edited issue, generate code, push a branch, and open a pull request
- [X] Generate multiple commits
- [ ] Update pull request on issue/pull request comment
- [ ] Update pull request based on code review comments
- [ ] Explore alternative code generation models

## 🔨 Usage

Warning: This Github Action is currently **in development**, and in **alpha release**.
If you're interested in using this action, please reach out on [Discord](https://discord.gg/vz7p9TfHsh).

To use the action:
- In `Settings -> Secrets and variables -> Actions`, enter your Open AI API key as `OPENAI_API_KEY`
- In `Settings -> Actions -> General`, scroll down to `Workflow permissions` and enable `Allow Github Actions to create and approve pull requests`
- Include the workflow file in your repository. [For example, you can use it in the same way as this repo](https://github.com/irgolic/autopr/blob/main/.github/workflows/create-pr-from-issue.yml).

Whenever a new issue is opened or edited, the action will push a branch named `autopr/issue-#` and open a pull request to the base branch.
Please note that if the branch already exists (on issue edit), it will be overwritten.
