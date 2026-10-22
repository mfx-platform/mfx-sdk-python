# MFX Hub Python SDK

The typed Python client for the [MFX Hub](https://mfxhub.com) API: hosted trading terminals for your
own broker accounts, with market data, execution, account state and a live event stream behind one
signed REST and WebSocket API.

```bash
pip install mfx-sdk
```

Python 3.12 or later. Async first, with a thin synchronous client for scripts.

## Your first quote and your first order

You need an API key (its id, and the private key shown once when it was issued), your broker's
name, your server's name exactly as your trading platform's login window shows it, and your
login. The program below finds the ids for those names, asks for a terminal, reads a quote,
buys the smallest volume the symbol allows, closes the position and retires the terminal. Use a
**demo** account: the order is real on whatever account you log in to.

```python
import asyncio
import getpass
import os
import uuid

import mfx

API = "https://api.dev.mfxhub.com/v1"           # https://api.mfxhub.com/v1 for production
SYMBOL = "EURUSD"                               # the broker's own symbol name


async def main() -> None:
    run = uuid.uuid4().hex[:8]  # every write takes an idempotency key; one set per run
    key = mfx.SigningKey(os.environ["MFX_PRIVATE_KEY"])
    async with mfx.MfxClient(API, os.environ["MFX_KEY_ID"], key) as client:
        # 1. The ids for the names you know: a farm your plan allows that executes orders,
        #    your broker, and your server.
        farm = [f async for f in client.farms.list() if "order_execution" in map(str, f.usages)][0]
        broker = [b async for b in client.catalog.all_brokers()
                  if os.environ["MFX_BROKER"].lower() in (b.code.lower(), b.display_name.lower())][0]
        server = [s for s in await client.catalog.servers(broker.id)
                  if s.server_name == os.environ["MFX_SERVER"]][0]

        # 2. A terminal for your account, logged in with your password, typed at a prompt.
        terminal = await client.terminals.create(
            farm_id=farm.id, broker_id=broker.id, server_id=server.id, execution=True,
            instruments=[SYMBOL], idempotency_key=f"terminal-{run}",
        )
        await client.terminals.submit_credentials(
            terminal.id, login=int(os.environ["MFX_LOGIN"]), server=server.server_name,
            password=mfx.Secret(getpass.getpass("Broker password: ")),
            idempotency_key=f"credential-{run}",
        )
        while not mfx.is_usable(terminal := await client.terminals.get(terminal.id)):
            await asyncio.sleep(5)

        # 3. A quote, always with its age.
        quote = await client.catalog.quote(broker.id, SYMBOL, server_id=server.id)
        print(quote.bid, quote.ask, quote.age_s)

        # 4. An order, the smallest volume allowed. Execution never raises: every outcome is a
        #    result, and wait_for returns it once it is final.
        spec = await client.catalog.symbol(broker.id, SYMBOL, server_id=server.id)
        placed = await client.execution.place_order(
            terminal.id, symbol=SYMBOL, side="buy", volume=str(spec.volume_min),
            idempotency_key=f"buy-{run}",
        )
        done = await client.execution.wait_for(placed.command_id)
        print(done.state, done.exec_price, done.comment_raw)

        # 5. Close the position it opened, and retire the terminal.
        closed = await client.execution.close_position(
            terminal.id, done.tickets.position, idempotency_key=f"close-{run}"
        )
        print((await client.execution.wait_for(closed.command_id)).state)
        await client.terminals.retire(terminal.id, idempotency_key=f"retire-{run}")


asyncio.run(main())
```

Run it with `MFX_KEY_ID`, `MFX_PRIVATE_KEY`, `MFX_BROKER` (for example `Pepperstone`),
`MFX_SERVER` (for example `Pepperstone-Demo`) and `MFX_LOGIN` set. The same program, with every
outcome checked, is [`samples/first_order.py`](https://github.com/mfx-platform/mfx-kb/blob/main/samples/first_order.py)
in the knowledge base, whose [guide](https://github.com/mfx-platform/mfx-kb/blob/main/guides/your-first-order.md)
explains each step.

## Reference

The [documentation](https://docs.mfxhub.com) has guides and the full reference, generated from this
package:
[client and signing](https://docs.mfxhub.com/sdk-client) ·
[terminals](https://docs.mfxhub.com/sdk-terminals) ·
[execution](https://docs.mfxhub.com/sdk-execution) ·
[accounts and catalogue](https://docs.mfxhub.com/sdk-accounts) ·
[market data](https://docs.mfxhub.com/sdk-market-data) ·
[stream and live account](https://docs.mfxhub.com/sdk-stream) ·
[errors](https://docs.mfxhub.com/sdk-errors).

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
