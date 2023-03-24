# 🤖👨‍💻 AutoPR Github Action 

<div align="center">

[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.gg/ykk7Znt3K6)

AutoPR automatically writes pull requests in response to issues using GPT-4.  
To get started, see [AutoPR-template](https://github.com/irgolic/AutoPR-template).  
Built with [Guardrails](https://github.com/ShreyaR/guardrails).    

</div>

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
- [ ] Running tests and taking corrective action

## 🔨 Usage

Warning: This Github Action is currently **in development**, and in **alpha release**.
If you're interested in using this action, please reach out on [Discord](https://discord.gg/ykk7Znt3K6).

See [AutoPR-template](https://github.com/irgolic/AutoPR-template) for a guide and example of how to use this action.
