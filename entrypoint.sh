#!/bin/sh
poetry install
poetry run python -m pr_drafter.gh_actions_entrypoint