# Changelog

Every release of `mfx-sdk`, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/). Until 1.0.0, a minor version may change the public
surface; each such change is listed under **Changed** with what to do.

## Unreleased

## 0.19.0

### Added

- The Service Agreement: `client.tenant.service_agreement()` (and `SyncMfxClient.tenant`) reads
  `GET /tenant/service-agreement`, any key, and answers the API's own `TenantServiceAgreement`:
  `due`, `held`, the plan in force, the `plan_change` awaiting acceptance (None when there is
  none), each document due and `accept_url`, where an owner or admin accepts.
  `SyncMfxClient.tenant` also has `contacts()`.
- `ServiceAgreementNotAccepted`, a `ConflictError`, for 409 `service_agreement_not_accepted`: a
  plan change awaits acceptance of the new plan's Service Agreement, or a version of the plan's
  agreement is past its grace period unaccepted, and an addition (a terminal, an expert advisor,
  an API key, higher limits) was refused. Its `plan_change` (a `PlanChange`: `id`, `from_`, `to`,
  `state`, `requested_at`, `until`, `requested_by_operator`), `documents` (each a `DocumentDue`:
  `document`, `number`, `plan`, `grace_ends_at`) and `accept_url` are read from `details`, None or
  empty where absent. Not retryable unchanged; nothing running is refused.
- `TermsNotAccepted`, a `ConflictError`, for 409 `terms_not_accepted`, which until now arrived as a
  plain `ConflictError`: a Terms of Service or MetaTrader 5 licence version is past its grace
  period unaccepted. Its `documents` are `DocumentDue` values, each with `grace_ends_at`, when
  that document's grace period ended.
- The first answer carrying `MFX-Service-Agreement: due` logs one WARNING on the `mfx` logger,
  `mfx.SERVICE_AGREEMENT_WARNING`, with the client's `key_id`; that client never logs it again.

- `client.risk.archive_challenge(challenge_id, *, idempotency_key)` archives a challenge
  (`POST /risk/challenges/{id}/archive`, `risk:write`). It is refused with `StateError`
  (`state_error`) while any account is in progress, and `details["accounts"]` names them.
  Archiving it again answers it unchanged. `RiskChallenge` gains `archived_at`, and the planner's
  check and preview rows (`RiskRuleCheck`) gain `challenge_id`.
- Billing: `client.billing` (and `SyncMfxClient.billing`) reads every `billing` route of the API
  (scope `billing:read`): `price_list()` (the public price list, which needs no key and is
  signed like every request), `summary()` (`GET /billing`: every profile with its standing),
  `profile(id)`, `forecast(profile_id, month=...)`, `prices()`, `invoice(id)`, and the invoices
  as `invoices_page(billing_profile_id=..., state=..., cursor=..., limit=...)` or `invoices(...)`,
  which follows the cursor. Each answers the API's own model; amounts stay exact decimal strings.
- `PaymentRequiredError`, the class for any 402, and beneath it `BillingPaymentRequiredError`
  for `billing_payment_required`: a payment is missing on the billing profile. Not retryable
  unchanged. Its `tenant_id`, `billing_profile_id`, `stage` (`reminder` or `suspended`), `cause`,
  `since`, `suspends_at`, `pay_by` (aware datetimes) and `action` (a `BillingAction`: `kind`,
  `portal_path`, `amount_usd` as a `Decimal`, `invoice_id`) are read from `details`, None where
  absent. An execution method refused for billing returns a refused `ExecutionResult` with the
  error's text in `detail`, as for every refusal, and never raises.
- `docs/sdkref.json`: this SDK's public surface in the shared reference format `mfx-sdkref/1`,
  which the docs site renders beside the other languages. Generated from the source by
  `tools/sdkref.py`: every class, method, signature with its defaults, docstring, field, enum
  value, alias and constant, with the API operation each method calls and the API error code
  each error is raised for. Parameter docs now live in the docstrings, under `Args:`.

### Fixed

- An answer carrying an enum word this SDK was not built with no longer fails the call with a
  `ValueError` from a generated module: the field reads as the enum's `UNKNOWN`, a
  pseudo-member whose `.value` is the word as sent, so `to_dict` writes it back unchanged and the
  rest of the page is read as before. A terminal in a state the SDK does not know reads, with
  `is_usable` false, where it used to raise `MfxApiError` `contract_breach`. A word you pass in a
  request is still refused before anything is sent. Suite 0.13.0.

- `place_order` (on `client.execution` and `client.trading_accounts`) now refuses a `comment`
  longer than 31 characters with `ValueError`, before anything is sent, as its docstring always
  said and the contract's `maxLength` asks: the terminal would cut it without saying so. Until now
  it was sent and the platform refused it. Counted in characters (code points), not bytes. The
  message is `comment is at most 31 characters; the terminal would cut a longer one (N given)`.
- `close_position` and `close_position_partial` (on `client.execution`, `client.trading_accounts`
  and their `SyncMfxClient` forms) take an optional `comment`, written on the closing deal
  (`Deal.comment`) so a caller can tell its own closes apart, as the contract's `PositionClose`
  and `PositionClosePartial` always allowed; the docstring that said the body had no such field
  was wrong. Without one the deal takes the position's own comment. Over 31 characters raises
  the same `ValueError` as `place_order`, before anything is sent.

## 0.18.0

### Added

- Copy Trading: `client.copy` covers every `/copy` route of the API (scopes `copy:read` and
  `copy:write`). Leaders: `create_leader`, `get_leader`, `leaders` / `all_leaders`,
  `update_leader`, `pause_leader`, `resume_leader`, `retire_leader(close_copied=..., reason=...)`,
  and an external leader's `send_open_signal` (exactly one of `volume` and `units`) and
  `send_close_signal`. Followers: `create_follower`, `preview_follower` (a read: no idempotency
  key), `get_follower`, `followers` / `all_followers`, `update_follower`, `pause_follower`,
  `resume_follower`, `resync_follower` and `unfollow(close_copied=...)`; their stop-outs:
  `stopouts` / `all_stopouts` and `reset_stopouts(reason=...)`. Groups: `create_group`,
  `get_group`, `groups` / `all_groups`, `update_group`, `add_group_followers`,
  `remove_group_followers`, `pause_group` and `resume_group`. The copy log: `log` / `all_log`,
  with its filters (each list sent comma-separated and checked here), its window and its order.
  Every write takes an `idempotency_key` and is never retried; nested settings are mappings in
  the API's own names, a `float` anywhere is a `TypeError` and a name the API does not have a
  `ValueError`, both before anything is sent. Every `all_*` method takes the page size, `limit`.
  An open signal's `sl` and `tp` may be below zero, as the API's decimals allow; `volume`, `units`
  and `gross_exposure_cap` may not. The log's `from_` and `to` are aware datetimes: a naive one is
  a `ValueError`.
- `options` (a follower's, a preview's and a group template's) takes `when_risk_unchecked`:
  `"refuse"` (the default) or `"copy"`, for a follower account protected by Risk Management whose
  copy host cannot yet check a copy against it. It comes from the API description, so a follower
  read back shows it in `options.when_risk_unchecked`.
- Requested closes and groups' bulk work: `close_group(group_id, reason=..., pause=...)` (`pause`
  has no default) closes the copied positions of every live member under one `batch_id`;
  `rollover_group(group_id, dry_run=..., fields=..., after=..., limit=...)` sets the group's
  template on its members, a dry run with no key and an applied one with its `idempotency_key`
  (checked before sending); `closes` / `all_closes` (by follower, leader, group, batch, state and
  window) and `get_close` follow each requested close of copied positions, an unfollow's or a
  retire's with `close_copied` among them.
- The tenant's reads: `signals` / `all_signals` (the leaders' signals with each one's outcomes, by
  leader, kind, action and window) and `tenant_stopouts` / `all_tenant_stopouts` (every stop-out
  of the followers, by state, follower, group and window).
- `followers` / `all_followers` take `sort` (`"newest"`, the default, or `"oldest"`) and
  `out_of_step`; `log` / `all_log` take `group_id`. A follower read carries `drift`, `limits_use`,
  `today`, `exposure` and its requested `close`; a group its `exposure` against its cap (USD, an
  equal share for each live member, with `leavers` and `unenforced`) and `out_of_step`; a log row
  the leader's `deal`, the follower's `symbol` and, for a Risk refusal, `risk`; the log's stats
  the p95s; a preview row both contract sizes and the follower's volume unit.
- `CopyPage`: a list page with its `stats` row, counted over everything the filters match.
- `REFUSAL_REASONS`: the closed list of reasons a copy did not fill.
- The `copy.*` events as typed values from `mfx.event_of`: `CopyCopied` (with its stage timings),
  `CopyRefused` (with `risk`, a `RiskRefusal`, when Risk Management refused the copy),
  `CopyStopoutEvent`, `CopyDrift`, `CopyStateChanged` and `CopyClosedEvent` (`copy.closed`: a
  requested close is final, with what it closed and what it did not), each naming the follower
  account and its venue.
- `SyncMfxClient.copy`: the same methods, blocking.
- `client.risk.archive_policy(policy_id, *, idempotency_key)` archives a policy
  (`POST /risk/policies/{id}/archive`, `risk:write`). It is refused with `StateError`
  (`state_error`) while any account holds the policy, and `details["accounts"]` names those
  accounts. Once archived, a policy can't be activated or versioned, and archiving it again answers
  it unchanged. `RiskPolicy` gains `archived_at`, null while the policy is active.
- `SyncMfxClient` has the account calls the async client has, for scripts with no event loop:
  `trading_account_funds`, `trading_account_positions`, `trading_account_pending_orders`,
  `trading_account_deals`, `trading_account_symbols`; the account's commands
  (`place_account_order`, `cancel_account_order`, `modify_account_order`,
  `modify_account_position`, `close_account_position`, `close_account_position_by`,
  `close_account_position_partial`, `set_account_trailing_stop`, `clear_account_trailing_stop`);
  `wait_for`; and the cTrader grant flow (`start_ctrader_grant`, `ctrader_grant`,
  `connect_ctrader_accounts`, `revoke_ctrader_grant`). Each is the blocking form of the method of
  the same name on `client.trading_accounts` or `client.execution`.

### Changed

- The conformance suite is pinned at 0.8.0: its Copy Trading cases run.
- `create_group` and `update_group` still take `placement_policy`, which the API now marks
  deprecated: it is stored and returned, and placement never reads it.
- Contract refresh: `spec/openapi.yaml` is the public API description with Copy Trading's final
  shape, and `mfx._generated` is regenerated from it.

## 0.17.0

### Removed

- `terminals.bulk_retire(...)`. MFX Hub does not serve a tenant's bulk retire and will not: the
  call always answered 404. The contract keeps `POST /terminals:retire` only as deprecated, because
  v1 changes are additive. To retire many terminals, call `terminals.retire(terminal_id, ...)` for
  each. `terminals.bulk_restart`, `get_bulk_action` and `cancel_bulk_action` are unchanged.

### Changed

- The vendored contract is refreshed. It adds the advisor parameter-definition routes
  (`/expert-advisors/{id}/parameter-definitions`), listed under REST only until the SDK wraps them.

## 0.16.0

### Added

- Risk Management: `client.risk` covers every `/v1/risk/*` route (scopes `risk:read`, `risk:write`,
  `risk:override`).
  - **Policies:** `create_policy`, `add_policy_version` (a relaxing version needs `risk:override`
    and a `reason`), `activate` (one outcome per account), `policy`, `policy_version`, `policies`
    (`sort="newest"` or `"oldest"`) and `policy_versions`.
  - **Accounts:** `accounts_page` (one page and its `stats`) and `accounts` (every page), filtered
    by several `coverage` and `restriction` values and sorted by a figure; `account`, `equity`,
    `close_scope(account_id, "mfx_positions" | "all_positions")` (what a close action would close
    now), `deactivate`, `clear` and `coverage`.
  - **The planner:** `preview` (size a trade from a risk budget) and `check` (an order already
    sized, as the pre-trade check would judge it).
  - **Exit plans:** `create_plan`, `plan` (with `r_now`), `plans_page` and `plans` (several
    accounts and states, `newest` or `oldest`), `amend_plan`, `pause_plan`, `resume_plan` and
    `end_plan`.
  - **Challenges:** `create_challenge`, `add_challenge_version`, `challenge`, `challenges`,
    `enrol`, `challenge_accounts_page` and `challenge_accounts` (several states and rules, sorted
    by a figure, with `stats`), and `challenge_account` (its periods and their statistics).
  - **Activity:** `activity_page` and `activity` (several kinds, accounts and outcomes;
    `unresolved_first`, `newest` or `oldest`).
- `RiskRefusedError` (a `ValidationError`, code `risk_refused`): a new entry that breaks a rule in
  force. Its `refusal` names the reason, the rule, the policy or the challenge with its version,
  and the figure used, the limit and what the entry would have made it, as text.
- `RiskOverrideRequiredError` (a `ForbiddenError`, code `risk_override_required`): a change that
  relaxes protection without `risk:override` and a reason.
- Typed events: `RiskRuleEvent` (`risk.rule_warning`, `risk.rule_breached`, `risk.rule_cleared`),
  `RiskCoverageChanged`, `RiskProgrammeResult` and `RiskPeriodClosed`, from `event_of`.

## 0.15.0

### Added

- Market data by a cTrader account: `client.md.subscribe_account(account_id, symbol, idempotency_key=...)`
  streams one symbol's spots on `md:{account_id}:{symbol}` (scope `md:write`; `pending` until the
  first spot), `account_subscriptions(account_id, cursor=..., limit=...)` and
  `all_account_subscriptions(account_id)` list them (`md:read`), and
  `account_candles(account_id, symbol, timeframe, from_=..., to=..., limit=...)` reads Spotware's
  bars through the account, at most 1,000 a call. An account's subscription is stopped with the
  existing `unsubscribe`. An MT5 account is a `StateError` with `details["reason"] ==
  "not_on_this_venue"`; use `subscribe` and `candles` for it.

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
