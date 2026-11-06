# Changelog

Every release of `mfx-sdk`, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). Until 1.0.0, a minor version may change the public
surface; each such change is listed under **Changed** with what to do.

## Unreleased

## 0.11.1

### Added

- Every request the SDK sends, and the stream's upgrade, carries
  `User-Agent: mfx-sdk-python/<version>`, built from the package's own version. It replaced the
  HTTP library's default name, so MFX Hub can tell which SDK and which version made each call.

## 0.11.0

### Added

- `client.terminals.journal(terminal_id, lines=...)` reads a terminal's MetaTrader journal, newest
  line first. While the terminal runs it is read from its cell now (`from_` is `live`); once it has
  stopped, failed or been retired you get the last lines its cell kept for 24 hours
  (`last_words`), and `stopped` says why. `lines` is 1 to 200 and is checked before the request.
  The blocking form is `SyncMfxClient.terminal_journal`.
- `client.terminals.page()` and `list()` take `label` (a mapping; a terminal is listed only when it
  carries every pair) and `state`. Both narrow the list on the platform before
  the page is cut. `SyncMfxClient.terminals()` takes them too.
- `client.catalog.catalogues(broker_id)` lists one row per server and account type you hold a
  symbol catalogue for, each with a `catalogue_hash` that changes only when a symbol is added,
  removed, comes back or changes its specification, description or identity: compare it to read the
  list again only when it moved. The blocking form is `SyncMfxClient.catalogues`.
- A symbol now carries the broker's `path`, `isin`, `exchange`, `category`, `currency_base`, `basis`
  and `calc_mode`, each `None` when the broker leaves it empty. A symbol page has `source`:
  `live` while a terminal of yours runs there, `last_known` when none does and the rows are the
  last reported. `Page.source` carries it for `client.catalog.symbols()`.
- A terminal has `server_kind` (`demo` or `live`, known before any login), and each of its
  conditions has `broker_words` (the broker's own words when it refused the login) and
  `refusal_kind` (`invalid_account` or `other`). `terminal.condition_changed` carries both.
- `maintenance.window_changed` is a new event on `events` and a new webhook type.
  `mfx.maintenance.window_event(message)` reads it as a typed value, and `WINDOW_CHANGED` names it.
- `symbol.spec_changed` has four more `change` values: `added`, `came_back`, `description` and
  `identity`.
- The API description is re-vendored.

### Changed

- `state` on `client.terminals.page()` and `list()` (and `SyncMfxClient.terminals()`) and on
  `client.maintenance.page()` and `list()` takes one state or a sequence of states, sent as one
  comma-separated value; each is checked before the request.
- A `LOGGING_IN` terminal can now be retired. Whether that is answered `202` (draining) or
  `409 state_error` depends on the platform version, and the SDK treats both as the platform's
  answer.

## 0.10.0

### Changed

- `client.usage.get()` answers the platform's new usage shape. Each limit now says its figure,
  where it comes from (`plan`, `tenant_override` or `key_override`), whether it is applied yet
  (`enforced`) and how much of it is used. `key` is the calling key's view, `tenant` the ceiling
  for all your keys, with `plan`, `farms`, `per_login`, `lifecycle` and `webhooks` beside them.
  `items`, `limits`, `budget_remaining` and `budget_source` are gone from it: read the remaining
  budget from `client.budget`, which every answer still carries. **What to do:** read
  `usage.key.commands_per_s.limit` where you read `usage.limits.commands_per_s`.

### Added

- The API description is re-vendored. New in it, and reachable today as plain HTTPS (listed in
  the README): `setTerminalHa` (`POST /terminals/{id}/ha`), and `getExpertAdvisorParameters` and
  `putExpertAdvisorParameters` (`/terminals/{id}/expert-advisor/parameters`).
- New fields carried by the generated models: a terminal's `ha`, a command's `resolve_by`, a
  candle list's `source`, `complete_from` and `complete_to`, and an opened position's
  `order_ticket`; and the events `command.resolved`, `command.unknown`, `md.candle.closed`,
  `order.placed`, `order.modified`, `order.closed` and `terminal.ha_switched`.

## 0.9.20

### Added

- Every HTTP call the client makes can be timed. Pass `on_call` to `MfxClient` and it is told each
  call as it ends, as a `CallTiming`: what was asked, the HTTP status (`None` when no answer came)
  and how long it took in milliseconds. A read retried after a 429 is two calls.
- `MFX_CALL_LOG`: when set to a file path, the client appends one JSON line per call to it,
  `{"status": 200, "ms": 12.5}`, and nothing else. The platform's checks use it to show how long
  a knowledge base sample's calls took.
- A listener that raises, or a log file that cannot be written, never fails the call.

## 0.9.19

### Fixed

- An order sent again with the same idempotency key, after the first had already finished, came
  back with `ok` false and no price, tickets or broker comment, because the platform answers a
  repeat with the command's state only. A filled order read as not filled. The SDK now reads the
  command once and returns the original result in full, marked `duplicate`. This applies to every
  execution write. A repeat still in flight is returned as it is, with no extra read; follow it
  with `wait_for`.
- If that read fails, the call still returns what the platform said (the state, `ok` true for a
  success, `duplicate`) with the price and tickets empty, and `detail` names the `get_command`
  call that reads the rest. It never raises.

### Changed

- The SDK passes the shared SDK test suite 0.3.0, all 74 cases.

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
