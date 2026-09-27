# Research instructions

Read the [fixed question](campaigns/unspecified-interval-partition/question.md), [prior state](campaigns/unspecified-interval-partition/state.md) and [preparation notes](campaigns/unspecified-interval-partition/work/preparation.md). The fixed [test corpus](campaigns/unspecified-interval-partition/work/cases.json) and [verifier](campaigns/unspecified-interval-partition/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/unspecified-interval-partition/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
