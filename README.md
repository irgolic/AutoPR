<div align="center">

<a href="https://autopr.com">
<img alt="AutoPR logo" width=150 src="https://github.com/user-attachments/assets/4c1dc5b3-7e82-489e-905e-6ad79005adcb" />
</a>

<h1>🌳 AutoPR 🌳</h1>
  
<table align="center">
  <tr >
    <td width=400 >
      <video src="https://user-images.githubusercontent.com/24586651/235325137-b4283565-f759-48f8-9e8b-39df144e0eb7.mov">
    </td>
  </tr>
</table>

AutoPR autonomously wrote pull requests in response to issues.  
Built with [Guardrails](https://github.com/guardrails-ai/guardrails).

</div>

## What is this?

A vision of user experience I had in March of 2023, back when OpenAI had just launched its first "ChatGPT API".

As far as I am aware, AutoPR was the first bot to autonomously generate pull requests in response to issues.
Like most demos back in the day, it worked about 20% of the time.

What inspired the initial weekend coding sprint was [Guardrails](https://github.com/guardrails-ai/guardrails), 
who were prompting LLMs to generate structured data with JSON Schemas, and reasking it when it did not adhere.
This was a time before grammar-powered structured data generation.

Enjoy this brief glimpse into the past. 🜂

## 💪 How did it work?

Triggered by adding a label containing `AutoPR` to an issue, AutoPR would:

1. Plan a fix
2. Write the code
3. Push a branch
4. Open a pull request

## 💎 Examples

Well-written issues often lead to better results.

- [Create a dice rolling bot](https://github.com/irgolic/AutoPR-template/pull/21)
- [Create a 'Tech Jargon Generator'](https://github.com/irgolic/AutoPR-template/pull/13)
- [Create a user-friendly weather app](https://github.com/irgolic/AutoPR-template/pull/15)
- [Write three programming interview challenges](https://github.com/irgolic/AutoPR-template/pull/11)
- [Replace `GPT2FastTokenizer` with `tiktoken`](https://github.com/irgolic/AutoPR/pull/44)


## 🤞 Limitations

This GitHub Action was **in development**, and in **alpha release**.

It still:

- [Incorrectly referenced](https://github.com/irgolic/AutoPR-template/pull/19/files#diff-830c8547feabc5e216043b6af2f7784ee819537d88219e607543a899db1853c0R17) code in other files
- [Duplicated lines](https://github.com/irgolic/AutoPR/pull/44/files#diff-8427d3dc331c8d06d0eca82385f08cb9878240db18a867f463ae90afab6ded43R135)
- Called [functions that don't exist](https://github.com/irgolic/AutoPR-template/pull/9/files#diff-01de17011a56527deac53327fec7f83279509157a1e806a2cec5c2215a953e97R63)
- Only worked on GitHub (see [#46](https://github.com/irgolic/AutoPR/issues/46))

## 🔨 Usage

Please see [USAGE.md](USAGE.md) for more information.

## 📝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information.
