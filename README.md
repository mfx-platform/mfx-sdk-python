# MFX Hub Python SDK

The typed Python client for the [MFX Hub](https://mfxhub.com) API: hosted trading terminals for your
own broker accounts, with market data, execution, account state and a live event stream behind one
signed REST and WebSocket API.

```bash
pip install mfx-sdk
```

Python 3.12 or later. Async first, with a thin synchronous client for scripts.

## Your first quote and your first order

You need an API key (its id and the private key shown once when it is issued), the id of a farm
your plan allows (`client.farms.list()` shows them and what each offers), and a broker account on
a server MFX Hub supports. The [documentation](https://docs.mfxhub.com) walks through each step,
and the [SDK reference](https://docs.mfxhub.com/sdk) lists every method.

```python
import os
import anyio
import mfx

API = "https://api.mfxhub.com/v1"          # https://api.dev.mfxhub.com/v1 for development


async def main() -> None:
    async with mfx.MfxClient(API, os.environ["MFX_KEY_ID"], os.environ["MFX_PRIVATE_KEY"]) as client:
        # 1. A terminal for your broker account, on a farm your plan allows, asking only for what
        #    that farm offers.
        farm = await client.farms.get(os.environ["MFX_FARM_ID"])
        offers = {str(usage) for usage in farm.usages}
        terminal = await client.terminals.create(
            farm_id=farm.id,
            broker_id=os.environ["MFX_BROKER_ID"],
            server_id=os.environ["MFX_SERVER_ID"],
            streaming="quote_streaming" in offers,
            execution="order_execution" in offers,
            instruments=["EURUSD"],                # the broker's own symbol names
            idempotency_key="my-first-terminal",
        )
        await client.terminals.submit_credentials(
            terminal.id,
            login=int(os.environ["BROKER_LOGIN"]),
            password=mfx.Secret(os.environ["BROKER_PASSWORD"]),
            server=os.environ["BROKER_SERVER"],
            idempotency_key="my-first-credential",
        )
        while not mfx.is_usable(terminal := await client.terminals.get(terminal.id)):
            await anyio.sleep(5)

        # 2. A quote, always with its age.
        quote = await client.catalog.quote(os.environ["MFX_BROKER_ID"], "EURUSD")
        print(quote.bid, quote.ask, quote.age_s)

        # 3. An order. Execution never raises: every outcome is a result.
        placed = await client.execution.place_order(
            terminal.id, symbol="EURUSD", side="buy", volume="0.01",
            idempotency_key="my-first-order",
        )
        done = await client.execution.wait_for(placed.command_id)
        print(done.state, done.reason, done.exec_price)


anyio.run(main)
```

## What to know

- **Every write takes an `idempotency_key`, and none defaults it.** Retrying with the same key
  returns the original answer; a fresh key asks for a second terminal or a second order.
- **Execution methods never raise.** A transport fault, a timeout, a rate limit and a broker
  rejection all come back as an `ExecutionResult` with a granular `reason`, the broker's own
  `comment_raw`, and `retryable`. A result in state `UNKNOWN` may already be a position: never
  re-send it under a new key; the platform reconciles it.
- **Prices, volumes and money are decimal strings**, in both directions. Pass `Decimal` or `str`;
  a `float` is refused, because `0.07 * 3` is `0.21000000000000002`.
- **Reads raise typed errors**, mapped from the API's `error.code`: `NotFoundError`,
  `RateLimitError` with `retry_after_s`, `UpstreamError` (with `DependencyUnavailableError` and
  `EdgeError` beneath it), `MaintenanceError` with the window's `ends_at`, and the rest.
- **Credentials cannot be logged by accident.** `SigningKey` and `Secret` render as `***` in every
  repr, f-string, log line and traceback, and cannot be pickled.
- **Lists follow the cursor.** There are no totals and no page numbers; `list()` methods iterate
  every page, `page()` methods return one.
- **The stream** (`client.stream()`) carries market data, candles, order book, account state, results
  and events, with resumable sequence numbers on the channels that need them.

## REST only

Every tenant operation in the API has a typed method here except these, which you call over HTTPS
with the same request signing (`mfx.signing`). A test keeps this table equal to the API, so it
cannot drift.

<!-- rest-only:start -->
| Operation | Route |
|---|---|
| `cancelTerminalOperation` | `DELETE /terminals/{id}/operations/{operation_id}` |
| `createRedisPushConnector` | `POST /connectors/redis-push` |
| `updateTerminal` | `PATCH /terminals/{id}` |
<!-- rest-only:end -->

`openStream` is the WebSocket, opened with `client.stream()`.

## How this package is built

`src/mfx/_generated` is generated from the published MFX Hub API description in `spec/openapi.yaml`
and is never edited by hand; CI regenerates it and fails on any difference. The hand-written modules
around it (`mfx.terminals`, `mfx.execution`, `mfx.streaming` and the rest) are what you import.

```bash
uv sync
uv run pytest
uv run python tools/generate.py      # after the API description changes
```

## Support and security

- Documentation: [docs.mfxhub.com](https://docs.mfxhub.com).
- Questions and bugs: open an issue, or write to support@mfxhub.com.
- Contributing: see [CONTRIBUTING.md](CONTRIBUTING.md); every release is in [CHANGELOG.md](CHANGELOG.md).
- Security reports: see [SECURITY.md](SECURITY.md). Please do not open a public issue for one.

## Licence and trademarks

Licensed under the [Apache License 2.0](LICENSE).

MFX Hub is an independent service and is not affiliated with, endorsed by or sponsored by
MetaQuotes Ltd. MetaTrader is a trademark of MetaQuotes Ltd., used here only to say which trading
platform MFX Hub's terminals are compatible with.
