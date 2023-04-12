<div align="center">

# 🚀 AutoPR 🚀

[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.gg/ykk7Znt3K6)

AutoPR autonomously writes pull requests in response to issues with ChatGPT.  
Built with [Guardrails](https://github.com/ShreyaR/guardrails) and [Langchain](https://github.com/hwchase17/langchain).    

</div>

## 💪 How does it work?

Triggered by adding a label containing `AutoPR` to an issue, AutoPR will:

1. Plan a fix
2. Write the code
3. Push a branch
4. Open a pull request

## 📍 Roadmap

- [X] Automatically write pull requests based on labeled issues
- [X] Autonomously generate code through iterative and adaptive planning
- [ ] Vector search through repository contents
- [ ] Implement advanced codegen techniques like [Reflexion](https://arxiv.org/abs/2303.11366) and [RepoCoder](https://arxiv.org/abs/2303.12570)
- [ ] Respond to PR comments
- [ ] Fix specific code hunks by highlighted line range in code review
- [ ] ChatGPT plugin that writes an issue during the course of a conversation
- [ ] User-configurable tasks like "add tests", "add docs", "add type hints"
- [ ] User-configurable semantic CI checks like "if file x changes, ensure file y reflects the change"
- [ ] Autonomous PR reviewer who pushes to your branch

## 💎 Examples

Well-written issue often lead to better results.

It can write code that fixes a bug in an existing repository.

- Example 1: Replace `GPT2FastTokenizer` with `tiktoken`
  - [Issue](https://github.com/irgolic/AutoPR/issues/43)
  - [Pull request](https://github.com/irgolic/AutoPR/pull/44)

Or it can write code from scratch in an empty repository.

- Example 2: Write three programming interview challenges
  - [Issue](https://github.com/irgolic/AutoPR-template/issues/10)
  - [Pull request](https://github.com/irgolic/AutoPR-template/pull/11)


## 🤞 Limitations

This Github Action is **in development**, and in **alpha release**.

It still:

- Sometimes [duplicates lines](https://github.com/irgolic/AutoPR/pull/44/files#diff-8427d3dc331c8d06d0eca82385f08cb9878240db18a867f463ae90afab6ded43R135)
- Sometimes calls [functions that don't exist](https://github.com/irgolic/AutoPR-template/pull/9/files#diff-01de17011a56527deac53327fec7f83279509157a1e806a2cec5c2215a953e97R63)
- Only works on Github (see [#46](https://github.com/irgolic/AutoPR/issues/46))

## 🔨 Usage

Please see [USAGE.md](USAGE.md) for more information.

## 📝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information.
