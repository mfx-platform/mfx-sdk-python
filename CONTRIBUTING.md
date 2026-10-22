# Contributing to the MFX Hub Python SDK

Thank you for helping. Bug reports, fixes, documentation and tests are all welcome.

## Before you start

- **A security problem?** Do not open an issue. Follow [SECURITY.md](SECURITY.md).
- **A question about your account, a terminal or the API itself?** Write to support@mfxhub.com.
  The documentation is at [docs.mfxhub.com](https://docs.mfxhub.com).
- **A bug in the SDK?** Open an issue with the SDK version (`python -c "import mfx; print(mfx.__version__)"`),
  your Python version, what you did, what you expected and what happened. Leave out API keys,
  broker logins and passwords, and anything else that identifies an account.
- **A larger change?** Open an issue first, so we can agree on the shape before you write it.

## Setting up

You need [uv](https://docs.astral.sh/uv/) and Python 3.12 or later.

```bash
uv sync
uv run pytest                    # the whole suite, with 100% line coverage required
uv run ruff format --check .     # formatting
uv run ruff check .              # lint, including a docstring on every public name
uv run mypy src                  # strict typing
```

The suite needs no network and no MFX Hub account: every call is answered by a recorded or
scripted response.

## What a change needs

- **Tests first.** A fix comes with the test that failed before it. Coverage stays at 100%.
- **Types.** `mypy --strict` passes; public names are fully annotated.
- **Docstrings.** Every public module, class, function and method says what it is for. Comments
  explain *why*, not *what*.
- **The SDK's rules hold.** Every write takes an `idempotency_key` and none invents one; execution
  methods return a result and never raise; prices, volumes and money are `Decimal` or `str`, never
  `float`; credentials never reach a log, a repr or a traceback.
- **No hand edits in `src/mfx/_generated`.** It is generated from `spec/openapi.yaml` by
  `uv run python tools/generate.py`, and CI regenerates it and fails on any difference. A change
  to the API description comes from MFX Hub, not from a pull request here.
- **A line in [CHANGELOG.md](CHANGELOG.md)** under *Unreleased*, written for someone upgrading.

## Signing off your commits

Every commit must carry a Developer Certificate of Origin sign-off: a statement that you wrote the
change, or otherwise have the right to submit it under this project's licence. The full text is at
[developercertificate.org](https://developercertificate.org). Add it with `-s`:

```bash
git commit -s -m "fix: a stream reconnect keeps its subscriptions"
```

which appends `Signed-off-by: Your Name <you@example.com>`, using the name and email in your git
configuration. A pull request with an unsigned commit cannot be merged; `git commit --amend -s`
or `git rebase --signoff` fixes it.

## How a pull request lands

The SDK is developed in a private repository alongside the platform it calls, and each release is
published here as a single commit. So a pull request here is not merged directly. Instead:

1. We review it here, in public, as usual.
2. Once it is approved, we apply it to the next release, keeping you as the commit's author and
   your sign-off.
3. When that release is published, we close the pull request with a link to it, and the
   changelog credits you.

The release that carries your change is usually the next one. If we cannot take a change, we say
why in the pull request.

## Licence

By contributing, you agree that your contribution is licensed under the
[Apache License 2.0](LICENSE), the same as the rest of the project.

## Code of conduct

Everyone taking part is expected to follow the [code of conduct](CODE_OF_CONDUCT.md).
