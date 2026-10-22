# Changelog

Every release of `mfx-sdk`, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). Until 1.0.0, a minor version may change the public
surface; each such change is listed under **Changed** with what to do.

## Unreleased

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
