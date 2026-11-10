# Changelog

Every release of `mfx-sdk`, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). Until 1.0.0, a minor version may change the public
surface; each such change is listed under **Changed** with what to do.

## 0.14.0

### Added

- Trade a trading account on any venue: `client.trading_accounts.place_order`, `cancel_order`,
  `modify_order`, `modify_position`, `close_position`, `close_position_by`,
  `close_position_partial`, `set_trailing_stop` and `clear_trailing_stop` take the account's id
  and send to `/v1/accounts/{id}/...` (scope `exec:write`). Same bodies and rules as
  `client.execution`: a required `idempotency_key`, a result returned and never raised, nothing
  retried. Read the outcome with `client.execution.wait_for`.
- Read a trading account on any venue: `funds`, `positions`, `pending_orders`,
  `deals(from_=..., to=..., position=...)` and `symbols` (scope `acct:read`). `symbols` gives a
  cTrader account's volume rules in lots and its leverage.
- Connect cTrader accounts: `start_ctrader_grant(environment=..., scope=..., return_url=...)`
  answers the consent link to send the trader to; `ctrader_grant(id)` lists the accounts they
  shared; `connect_ctrader_accounts(id, [...])` makes the chosen ones trading accounts of yours;
  `revoke_ctrader_grant(id)` moves them to `REAUTH_NEEDED`.
- `ExecutionResult` reads what a venue adds: `venue`, `venue_code` (the venue's own refusal code
  beside `reason`), `deals` (each `VenueDeal` with `volume_units` and `price`), `volume_units`,
  `close_by_emulated` and `protection_not_set`.
- `Reason.VENUE_UNAVAILABLE` (retryable) and `Reason.NOT_ON_THIS_VENUE`.

## 0.13.0

### Added

- `QUEUED`, a terminal state and an operation state: placed and waiting its turn to start,
  because a cell starts terminals a few at a time. `terminal.queue` says its place, its
  `expected_start_at` and why it waits (`cell_busy`, `cell_settling`, `broker_cap` and so on).
  `TerminalStateName` takes it, so `terminals.list(state="QUEUED")` narrows to it.
- `terminals.wait_until_active(id, timeout_s=900)`: reads the terminal until it is no longer on
  its way to ACTIVE (REQUESTED, QUEUED, PROVISIONING, LOGGING_IN), and returns the last read. A
  QUEUED terminal is read again at its expected start, between 2 s and a minute away; anything
  else after 2 s, doubling to 15 s.
- `terminals.bulk_restart(...)` and `terminals.bulk_retire(...)` (`POST /v1/terminals:restart`,
  `POST /v1/terminals:retire`): many terminals at once, chosen by `farm_id`, `broker_id` or
  `terminal_ids` (at most 1000). Each is judged by the rules of a single restart or retire; a
  refused one is listed in `refused` with its rule's code and the rest are taken. The reason, the
  filter and the id count are checked at the call. `terminals.get_bulk_action(id)` and
  `terminals.cancel_bulk_action(id, idempotency_key=...)` read and cancel one.
- `client.trading_accounts`: the trading accounts over every venue (`GET /v1/accounts`,
  `GET /v1/accounts/{id}`, scope `acct:read`). `page()` and `list()` narrow by `venue`,
  `environment` and `state` on the platform, each checked at the call; `get(id)` takes the
  account's id or one of its terminals' ids. An MT5 account's id is its terminal's id. The sync
  client has `get_trading_account` and `trading_accounts`. `client.accounts` is unchanged: it is
  still the balance, positions and deals of a terminal's account.
- The copy-trading operations (`/v1/copy/...`) are in the contract and listed in the README's
  REST-only table; the SDK has no methods for them yet.

### Changed

- `terminals.restart(...)` sends `queue=True` unless told otherwise, as the contract now defaults
  it. A valid restart refused only because the platform is busy is answered 202 with the operation
  `QUEUED`, and it starts on its own. To keep the old answer, a 409 or 429 with `Retry-After`,
  pass `queue=False`.

## 0.12.1

### Fixed

- `stream.aclose()` ends the stream for good. A read waiting for a message (`async for`, or
  `anext`) ends with nothing, and a reconnect under way is given up. Before, closing while a read
  waited made the stream reconnect and keep delivering, so a script that closed its stream did not
  end.

### Changed

- The SDK passes the shared SDK test suite 0.4.0, which adds four stream cases.

## 0.12.0

### Added

- `mfx.event_of(message)` reads a stream message as a typed event, or None for any other type:
  `OrderPlaced`, `OrderModified` and `OrderClosed` (with `reason` and, on a fill,
  `position_ticket`), `PositionOpened` (with `order_ticket`), `PositionModified`,
  `PositionClosed`, `TerminalStateChanged` and, from a `candles:` channel, `CandleClosed`. Ids are
  UUIDs, tickets integers, prices, volumes and money Decimals, times aware UTC datetimes. The
  platform's own words (side, order type, reasons, states, timeframe) stay text, so a word added
  later still reads.

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
