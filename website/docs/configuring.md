---
sidebar_position: 3
---

# ✂️ Configuring

## 📁 The `.autopr` Folder

When you initialize AutoPR for your repository, create a folder named `.autopr`.
Think of this directory as AutoPR's command center, where it looks for instructions on what to do.  
Inside this folder, there are a few important files and folders:

- `.autopr/triggers.yaml`: Tells AutoPR when to act.
- `.autopr/workflows.yaml`: Optionally defines custom workflows for AutoPR to execute.
- `.autopr/cache`: Where AutoPR stores its cache files.
  At the moment, action `prompt` (for executing LLM prompts) implements caching in the background.

## 🏁 Setting Triggers in `.autopr/triggers.yaml`

Triggers serve as conditions or events that, when met, initiate specific actions,
such as pushing to a branch, or labeling a pull request.

See [the triggers reference](../reference/triggers) for a full list of triggers and their descriptions.

## 🛠️ Writing Workflows in `.autopr/workflows.yaml`

There are a few predefined workflows that you can use out of the box.  
See [the workflow catalogue](../workflow-catalogue) for a full list of workflows and their descriptions.

AutoPR is designed to be highly flexible and customizable, so you can write your own workflows to automate your repository.  
See the [tutorial on how to write your own workflows](./tutorials/writing-a-workflow) for more information.

## 🚀 Ready, Set, Go!

And that's it! With your triggers set and workflows defined, AutoPR is ready to work its magic on your repository. 
Remember, you can always come back and tweak these configurations as your needs evolve. AutoPR is designed to be flexible and grow with you. 🌟

If you have any questions, or you need assistance with writing custom trigger files or workflows, feel free to reach out to us on [Discord](https://discord.com/invite/ykk7Znt3K6) or [post an issue on Github](https://github.com/irgolic/AutoPR/issues).