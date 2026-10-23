# Changelog

Every release of `mfx-sdk`, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). Until 1.0.0, a minor version may change the public
surface; each such change is listed under **Changed** with what to do.

## Unreleased

## 0.9.18

### Fixed

- An order whose connection dropped after it was sent came back `retryable`, which invited sending
  it again under a new key while the first may already be a position. It now reads `UNKNOWN` and is
  not retryable; sending it again under the **same** key is safe. Only an order whose connection
  never opened is retryable.

### Added

- The SDK runs the shared MFX Hub SDK test suite (`tests/conformance`), the same cases every MFX Hub
  SDK must pass: signing, every error code, decimals, idempotency, paging and execution.

## 0.9.17

### Changed

- Dependencies: anyio 4.15.1, websockets 17.3, cryptography 50.0.2; for development, mypy 2.4.0
  and ruff 0.17.
- The repository runs the OpenSSF Scorecard weekly and publishes its results.

## 0.9.16

### Changed

- The README's first program finds your farm, broker and server from their names, places the
  smallest order the symbol allows, closes it and retires the terminal; it is the same code as the
  knowledge base's `first_order.py`. The README links every reference page.
- Reference text: every field of `ExecutionResult`, what `reason` is on a success (none: read
  `state`), where `catalog.quote` reads from and what its `state` means, and how to read a `Page`.

## 0.9.15

The first public release.

### Added

- `MfxClient`, async, and `SyncMfxClient` for scripts, signing every request with your API key's
  Ed25519 private key, which never leaves your process.
- Terminals: create on a farm, submit broker credentials, follow the state until usable, drain,
  resume and retire, with optional redundancy (active-passive or active-active).
- Execution: market, limit, stop and stop-limit orders; cancel and modify a pending order; modify,
  close, partially close and close-by a position; trailing stops; and `wait_for` a command's
  outcome. Every outcome is an `ExecutionResult` with a granular reason, the broker's own comment,
  and the broker and platform latencies. Execution never raises.
- Catalogue and accounts: brokers, servers, symbols with the broker's own facts, quotes with their
  age, the account, positions, pending orders, deals by window and spreads.
- Market data: candles and tick history by request, and subscriptions that report when they stop
  and start delivering.
- The stream: prices, candles, order books, account state, results and events over one
  WebSocket, with resumable sequence numbers, automatic reconnection, and a live account view that
  merges marks into the snapshot it holds.
- Expert advisors: upload, wait for the verdict, attach, follow the operation and read telemetry.
- Webhooks: register, pause, rotate, test, read failures, replay, and `verify()` a delivery's
  signature.
- Typed errors for every error code the API names, with `retry_after_s` on a rate limit and the
  window's end on maintenance; an unknown code still arrives as a typed error.
- `Secret` and `SigningKey`, which render as `***` in every repr, log line and traceback, and
  cannot be pickled.
- Structured logging on the standard library, with secrets redacted.
