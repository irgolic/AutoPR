---
sidebar_position: 1
---

# 🐙 GitHub

This guide will walk you through setting up and using AutoPR as a GitHub Action.

### Prerequisites

You need your own OpenAI API key.

### Setup

Follow these steps to set up AutoPR in your GitHub repository:

1. Create a new file in your repository named `.github/workflows/autopr.yaml` and copy the contents from [the GitHub workflow template](https://github.com/irgolic/AutoPR-template/blob/main/.github/workflows/autopr.yaml).
2. Create a new folder in your repository named `.autopr/triggers.yaml` and copy the contents from [the triggers template](https://github.com/irgolic/AutoPR-template/blob/main/.autopr/triggers.yaml).
3. In your GitHub repository settings, navigate to `Secrets and variables -> Actions` and add your OpenAI API key as `OPENAI_API_KEY`.
4. In your GitHub repository settings, go to `Actions -> General` and scroll down to `Workflow permissions`. Enable `Allow GitHub Actions to create and approve pull requests`.

That's it! Check out the [Customization guide](./customization) to see how to customize AutoPR for your repository.