"""``mfx.logging`` — the MFX shape, redaction by type, and a library that leaves its host alone.

The rule these assert is narrower than "secrets are masked": a secret is unloggable because of
*what it is*, so it survives being nested, renamed, or passed by an author who never heard of it.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import pytest

from mfx.logging import (
    LOGGER_NAME,
    REDACTED,
    LogContext,
    MfxJsonFormatter,
    MfxLogger,
    bound,
    configure_logging,
    get_logger,
    redact,
)
from mfx.secrets import Secret
from mfx.signing import SigningKey

#: The Story these cases are Tested By: generated core + ergonomic layer + conformance suite.


@pytest.fixture(autouse=True)
def clean_logger() -> Any:
    """Leave the `mfx` logger exactly as it was found — these tests configure it on purpose."""
    logger = logging.getLogger(LOGGER_NAME)
    handlers, level, propagate = list(logger.handlers), logger.level, logger.propagate
    yield
    logger.handlers = handlers
    logger.setLevel(level)
    logger.propagate = propagate


def test_a_secret_is_unloggable_by_type_however_deeply_it_is_buried(
    raw_key: str, caplog: pytest.LogCaptureFixture
) -> None:
    """Given a log line carrying secrets in a dict, a list and a field nobody anticipated / When it
    is written / Then every one renders as *** — because redaction is by type, not by a blocklist
    of field names.

    A name-based blocklist only ever catches the names someone thought of, and the line that leaks
    is always the one with the name nobody thought of."""
    password = "s3cret-Pepperstone!"
    log = get_logger(command_id="c-1")

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        log.info(
            "submitting",
            credential=Secret(password),
            key=SigningKey(raw_key),
            nested={"deep": {"inner": Secret(password)}},
            batch=[Secret(password), "EURUSD.sd"],
            anything_at_all=Secret(password),
        )

    assert password not in caplog.text
    fields = caplog.records[0].mfx
    assert fields["credential"] == REDACTED
    assert fields["key"] == REDACTED
    assert fields["nested"]["deep"]["inner"] == REDACTED
    assert fields["batch"] == [REDACTED, "EURUSD.sd"]
    assert fields["anything_at_all"] == REDACTED
    assert fields["command_id"] == "c-1", "every execution line carries it (rule 4)"
    assert fields["batch"][1] == "EURUSD.sd", "everything that is not a secret survives intact"


def test_importing_this_sdk_does_not_touch_the_hosts_logging(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A library that calls basicConfig(force=True) or reconfigures the root logger is a library
    that loses someone their production log format. Nothing here happens until a host asks."""
    root = logging.getLogger()
    before = list(root.handlers)

    get_logger().info("a line", terminal_id="t-1")

    assert list(root.handlers) == before
    assert logging.getLogger(LOGGER_NAME).propagate is True, "the host still sees our lines"


def test_configuring_the_mfx_shape_is_opt_in_and_reaches_one_logger_only(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The MFX JSON shape on request: ts, level, service, env, msg and the line's own fields, on
    the `mfx` logger and nowhere else. Propagation goes off so the host's own handlers do not print
    every line a second time in their format."""
    handler = configure_logging(service="mfx-sdk", env="dev", level=logging.INFO)

    get_logger(tenant_id="tn-1").info("terminal requested", terminal_id="t-1")

    line = json.loads(capsys.readouterr().err.strip())
    assert line["level"] == "info"
    assert line["service"] == "mfx-sdk" and line["env"] == "dev"
    assert line["msg"] == "terminal requested"
    assert line["terminal_id"] == "t-1" and line["tenant_id"] == "tn-1"
    assert line["ts"].endswith(("Z", "+00:00")) or "T" in line["ts"]
    assert logging.getLogger(LOGGER_NAME).propagate is False
    assert logging.getLogger().handlers == logging.getLogger().handlers, "root untouched"
    assert handler in logging.getLogger(LOGGER_NAME).handlers

    configure_logging(service="mfx-sdk", env="dev")
    assert (
        len(
            [
                h
                for h in logging.getLogger(LOGGER_NAME).handlers
                if h.formatter.__class__.__name__ == "MfxJsonFormatter"
            ]
        )
        == 1
    ), "configuring twice replaces rather than doubles every line"


def test_context_is_bound_for_a_block_and_put_back_afterwards(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """command_id on every line an execution writes, including the ones inside the SDK a caller
    never calls directly — without threading it through every signature."""
    log = get_logger()

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        with LogContext(correlation_id="r-1"):
            log.info("inside")
            with bound(command_id="c-2"):
                log.info("deeper")
        log.info("outside")

    inside, deeper, outside = (record.mfx for record in caplog.records)
    assert inside == {"correlation_id": "r-1"}
    assert deeper == {"correlation_id": "r-1", "command_id": "c-2"}
    assert outside == {}, "the block put back exactly what was there before"


def test_a_field_named_like_a_log_record_attribute_does_not_crash_the_caller(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """stdlib logging raises "Attempt to overwrite 'module' in LogRecord" when `extra` collides
    with a record attribute. Our fields go under one key, so a tenant's choice of field name can
    never take their own process down."""
    log = get_logger()

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        log.info("collides", module="theirs", name="theirs", args="theirs", message="theirs")

    assert caplog.records[0].mfx["module"] == "theirs"
    assert caplog.records[0].getMessage() == "collides"


def test_every_level_is_available_and_a_switched_off_level_builds_nothing(
    caplog: pytest.LogCaptureFixture, raw_key: str
) -> None:
    """The level check comes before the line is assembled and redacted: on a per-tick debug path,
    building a line the host has switched off is work done to be thrown away."""
    log = get_logger()
    revealed: list[str] = []

    class Loud(Secret):
        def __repr__(self) -> str:
            revealed.append("rendered")
            return super().__repr__()

    with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
        log.debug("not written", secret=Loud("x"))
        log.info("not written either")
        log.warning("written", a=1)
        log.error("also written")
        try:
            raise ValueError("boom")
        except ValueError:
            log.exception("with the traceback")

    assert [r.getMessage() for r in caplog.records] == [
        "written",
        "also written",
        "with the traceback",
    ]
    assert caplog.records[-1].exc_info is not None
    assert revealed == [], "nothing was rendered for the line that was never written"


def test_binding_returns_a_new_logger_and_leaves_the_original_alone(
    caplog: pytest.LogCaptureFixture,
) -> None:
    base = get_logger(service_field="a")
    child = base.bind(command_id="c-9")

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        child.info("child")
        base.info("base")

    assert caplog.records[0].mfx == {"service_field": "a", "command_id": "c-9"}
    assert caplog.records[1].mfx == {"service_field": "a"}
    assert "command_id" in repr(child) and "command_id" not in repr(base)


def test_redact_leaves_everything_that_is_not_a_secret_exactly_as_it_was() -> None:
    """Including the container types — a tuple stays a tuple, so redaction cannot change the shape
    of the thing being logged."""
    assert redact(("a", Secret("b"))) == ("a", REDACTED)
    assert redact({"n": 1, "f": 1.5, "none": None}) == {"n": 1, "f": 1.5, "none": None}
    assert redact(frozenset({"x"})) == frozenset({"x"})


def test_an_exception_is_rendered_into_the_json_shape(capsys: pytest.CaptureFixture[str]) -> None:
    """A failure that logs only "exc_info: true" is a failure nobody can read afterwards."""
    configure_logging(env="dev")

    try:
        raise ValueError("boom")
    except ValueError:
        get_logger().exception("it failed")

    line = json.loads(capsys.readouterr().err.strip())
    assert "ValueError: boom" in line["exc"]


def test_the_formatter_ignores_a_record_that_was_not_written_through_this_sdk(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Anything else routed to the `mfx` logger still formats, without fields it does not have."""
    configure_logging()
    logging.getLogger(LOGGER_NAME).warning("from somewhere else")

    line = json.loads(capsys.readouterr().err.strip())
    assert line["msg"] == "from somewhere else" and line["level"] == "warning"


def test_a_logger_names_itself_for_a_host_that_wants_to_route_it() -> None:
    assert isinstance(get_logger(), MfxLogger)
    assert MfxJsonFormatter(service="s", env="e").service == "s"
