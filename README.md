# 🤖👨‍💻 AutoPR Github Action 🚀

<div align="center">

[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.gg/ykk7Znt3K6)

AutoPR automatically writes pull requests in response to issues using ChatGPT.  
To get started, see [AutoPR-template](https://github.com/irgolic/AutoPR-template).  
Built with [Guardrails](https://github.com/ShreyaR/guardrails).    

</div>

## 💪 How does it work?

The action triggers when a collaborator adds an "AutoPR" label to an issue.

1. We ask the model what files in the repo are relevant to the issue
2. We iteratively show it files, and ask it to write down notes about them
3. We ask it to write a pull request title, body, and outline a list of commits (also specifying relevant files)
4. For each commit, we ask it to generate a diff given the relevant files

## 📍 Roadmap

- [X] On new/edited issue, generate code, push a branch, and open a pull request
- [X] Generate multiple commits
- [X] Regenerate triggered from issue comment
- [ ] Update from pull request comment
- [ ] Update from code review comments
- [ ] Explore alternative code generation models
- [ ] Running CI and taking corrective action on failure

## 🔨 Usage

Warning: This Github Action is currently **in development**, and in **alpha release**.
If you're interested in using this action, please reach out on [Discord](https://discord.gg/ykk7Znt3K6).

See [AutoPR-template](https://github.com/irgolic/AutoPR-template) for a guide and example of how to use this action.

## 📝 Contributing

Got an idea on how to improve AutoPR? 
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information.
