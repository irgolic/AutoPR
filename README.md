<div align="center">

# 🚀 AutoPR 🚀

[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.gg/ykk7Znt3K6)


<table align="center">
  <tr>
    <td>
      <video src="https://user-images.githubusercontent.com/24586651/235325137-b4283565-f759-48f8-9e8b-39df144e0eb7.mov">
    </td>
  </tr>
</table>


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
- [ ] Vector search through repository contents (https://github.com/irgolic/AutoPR/issues/55)
- [ ] Improving codegen performance (https://github.com/irgolic/AutoPR/issues/56)
- [ ] Iterate with PR comments and code review (https://github.com/irgolic/AutoPR/issues/31)
- [ ] ChatGPT plugin that writes an issue during the course of a conversation
- [ ] User-configurable tasks like "add tests", "add docs", "add type hints"
- [ ] User-configurable semantic CI checks like "if file x changes, ensure file y reflects the change"
- [ ] Autonomous PR reviewer who pushes to your branch

## 💎 Examples

Well-written issues often lead to better results.

- [Create a dice rolling bot](https://github.com/irgolic/AutoPR-template/pull/21)
- [Design a poll and survey bot](https://github.com/irgolic/AutoPR-template/pull/19)
- [Create a 'Tech Jargon Generator'](https://github.com/irgolic/AutoPR-template/pull/13)
- [Create a user-friendly weather app](https://github.com/irgolic/AutoPR-template/pull/15)
- [Write three programming interview challenges](https://github.com/irgolic/AutoPR-template/pull/11)
- [Replace `GPT2FastTokenizer` with `tiktoken`](https://github.com/irgolic/AutoPR/pull/44)


## 🤞 Limitations

This Github Action is **in development**, and in **alpha release**.

It still:

- [Incorrectly references](https://github.com/irgolic/AutoPR-template/pull/19/files#diff-830c8547feabc5e216043b6af2f7784ee819537d88219e607543a899db1853c0R17) code in other files
- Sometimes [duplicates lines](https://github.com/irgolic/AutoPR/pull/44/files#diff-8427d3dc331c8d06d0eca82385f08cb9878240db18a867f463ae90afab6ded43R135)
- Sometimes calls [functions that don't exist](https://github.com/irgolic/AutoPR-template/pull/9/files#diff-01de17011a56527deac53327fec7f83279509157a1e806a2cec5c2215a953e97R63)
- Only works on Github (see [#46](https://github.com/irgolic/AutoPR/issues/46))

## 🔨 Usage

Please see [USAGE.md](USAGE.md) for more information.

## 📝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information.
