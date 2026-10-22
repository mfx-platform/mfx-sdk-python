"""``MfxLogger`` — structured lines a tenant can read, with redaction by type.

The MFX log *shape* is copied here — ``ts``, ``level``, ``service``, ``env``, ``correlation_id``,
``tenant_id``, ``command_id``, ``msg``, plus whatever the line carries. The MFX logging *library*
is not, and neither is its configuration step, for one reason:

**A library does not configure its host's logging.** ``logging.basicConfig(force=True)`` and
``structlog.configure()`` are process-wide; a tenant importing this SDK would find their own
handlers replaced and their own format rewritten by a dependency. So everything here writes to a
plain stdlib logger named ``mfx``, which the host already knows how to level, filter and route. A
tenant who *wants* the MFX JSON shape opts in with :func:`configure_logging`, and a tenant who
wants their own gets it by doing nothing.

Redaction is by **type**, not by field name (guardrail #1). A :class:`~mfx.secrets.Secret` or a
:class:`~mfx.signing.SigningKey` renders as ``***`` because of what it is, not because whoever
wrote the line remembered to mask it — including nested inside a dict, a list or a tuple. A field
name blocklist only ever catches the names someone thought of.

``command_id`` rides every execution line, so an order can be followed from the SDK call to the
platform's own logs without joining on a timestamp.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator, Mapping, MutableMapping
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Final, Self

from mfx.secrets import Secret
from mfx.signing import SigningKey

__all__ = ["REDACTED", "LogContext", "MfxLogger", "configure_logging", "get_logger", "redact"]

REDACTED: Final = "***"

#: The one logger a host configures to see everything this SDK says.
LOGGER_NAME: Final = "mfx"

#: Bound per task rather than threaded through signatures, so a correlation id set once appears on
#: every line beneath it — including inside a retry the caller never sees. The default is read-only:
#: a plain {} shared by every context is one `.update()` away from being global state.
_EMPTY: Final[Mapping[str, Any]] = MappingProxyType({})
_CONTEXT: ContextVar[Mapping[str, Any]] = ContextVar("mfx_log_context", default=_EMPTY)


def redact(value: Any) -> Any:  # noqa: ANN401 - it takes whatever a log line carries
    """``value`` with every secret in it replaced, however deeply it is nested."""
    if isinstance(value, Secret | SigningKey):
        return REDACTED
    if isinstance(value, Mapping):
        return {key: redact(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set | frozenset):
        return type(value)(redact(item) for item in value)
    return value


class MfxLogger:
    """A bound logger. Fields bound here appear on every line it writes.

    Thin on purpose: it holds context and redacts, and leaves levels, handlers and destinations to
    the host's own ``logging`` configuration.
    """

    __slots__ = ("_bound", "_logger")

    def __init__(self, name: str = LOGGER_NAME, **bound: Any) -> None:
        self._logger = logging.getLogger(name)
        self._bound = bound

    def bind(self, **values: Any) -> Self:
        """A new logger carrying these fields as well. The original is unchanged."""
        return type(self)(self._logger.name, **{**self._bound, **values})

    def debug(self, msg: str, **fields: Any) -> None:
        """Write a DEBUG record carrying ``fields``; secrets among them are redacted."""
        self._write(logging.DEBUG, msg, fields)

    def info(self, msg: str, **fields: Any) -> None:
        """Write an INFO record carrying ``fields``; secrets among them are redacted."""
        self._write(logging.INFO, msg, fields)

    def warning(self, msg: str, **fields: Any) -> None:
        """Write a WARNING record carrying ``fields``; secrets among them are redacted."""
        self._write(logging.WARNING, msg, fields)

    def error(self, msg: str, **fields: Any) -> None:
        """Write an ERROR record carrying ``fields``; secrets among them are redacted."""
        self._write(logging.ERROR, msg, fields)

    def exception(self, msg: str, **fields: Any) -> None:
        """An error with the active exception attached. The traceback is redacted the same way:
        a Secret inside an exception message renders as ``***`` by its own repr."""
        self._write(logging.ERROR, msg, fields, exc_info=True)

    def _write(
        self, level: int, msg: str, fields: Mapping[str, Any], *, exc_info: bool = False
    ) -> None:
        # Checked before anything is built: assembling and redacting a DEBUG line the host has
        # switched off is work done to be thrown away, on a path that runs per tick.
        if not self._logger.isEnabledFor(level):
            return
        # Everything goes under one key rather than being flattened onto the record. `extra` is
        # merged into the LogRecord's own attributes, so a caller logging a field called `module`,
        # `name` or `args` would make stdlib logging raise "Attempt to overwrite ... in LogRecord"
        # — a crash caused by a tenant's choice of field name. `record.mfx` is where a custom
        # formatter reads them.
        self._logger.log(
            level,
            msg,
            extra={"mfx": redact({**_CONTEXT.get(), **self._bound, **fields})},
            exc_info=exc_info,
        )

    def __repr__(self) -> str:
        return f"MfxLogger({self._logger.name!r}, {sorted(self._bound)})"


def get_logger(name: str = LOGGER_NAME, **bound: Any) -> MfxLogger:
    """The SDK's logger, optionally with fields bound to it."""
    return MfxLogger(name, **bound)


class LogContext:
    """Bind fields for a block, then put back exactly what was there before.

    Used per command so ``command_id`` appears on every line an execution writes — including the
    ones inside the SDK the caller never calls directly — without threading it through signatures.
    """

    __slots__ = ("_token", "_values")

    def __init__(self, **values: Any) -> None:
        self._values = values
        self._token: Any = None

    def __enter__(self) -> Self:
        self._token = _CONTEXT.set({**_CONTEXT.get(), **self._values})
        return self

    def __exit__(self, *_exc: object) -> None:
        _CONTEXT.reset(self._token)


@contextmanager
def bound(**values: Any) -> Iterator[None]:
    """:class:`LogContext` as a one-liner."""
    with LogContext(**values):
        yield


class MfxJsonFormatter(logging.Formatter):
    """The MFX log shape: ts, level, service, env, msg, and the line's own fields.

    Only ever installed by :func:`configure_logging`, which a tenant calls or does not.
    """

    def __init__(self, *, service: str = "mfx-sdk", env: str = "unknown") -> None:
        super().__init__()
        self.service = service
        self.env = env

    def format(self, record: logging.LogRecord) -> str:
        event: MutableMapping[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname.lower(),
            "service": self.service,
            "env": self.env,
            "msg": record.getMessage(),
        }
        fields = getattr(record, "mfx", None)
        if isinstance(fields, Mapping):
            event.update(fields)
        if record.exc_info:
            event["exc"] = self.formatException(record.exc_info)
        return json.dumps(event, default=str, separators=(",", ":"))


def configure_logging(
    *, service: str = "mfx-sdk", env: str = "unknown", level: int | str = logging.INFO
) -> logging.Handler:
    """Opt in to the MFX JSON shape on the ``mfx`` logger, and nothing else.

    Deliberately narrow: it touches one logger, adds one handler, and turns propagation off so the
    host's root handlers do not print every line a second time in their own format. It never calls
    ``basicConfig`` and never touches the root logger, because a library that reconfigures its
    host's logging is a library that loses someone their production log format.

    Returns the handler, so a caller can remove it again.
    """
    logger = logging.getLogger(LOGGER_NAME)
    for existing in [h for h in logger.handlers if isinstance(h.formatter, MfxJsonFormatter)]:
        logger.removeHandler(existing)
    handler = logging.StreamHandler()
    handler.setFormatter(MfxJsonFormatter(service=service, env=env))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return handler
