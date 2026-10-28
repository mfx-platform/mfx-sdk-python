"""MFX client library — the only way a tenant talks to MFX.

Execution methods never raise across the boundary; read methods raise the typed hierarchy.

    import mfx

    async with mfx.MfxClient("https://api.mfxhub.com/v1", key_id, private_key) as client:
        terminal = await client.terminals.create(
            farm_id=farm, broker_id=broker, server_id=server, idempotency_key="my-key-1"
        )
        await client.terminals.submit_credentials(
            terminal.id,
            login=1234567,
            password=mfx.Secret(...),
            server="EquitiSecurities-Demo",
            idempotency_key="my-key-2",
        )
"""

from mfx.client import Budget, MfxClient
from mfx.errors import (
    AuthError,
    ConflictError,
    DependencyUnavailableError,
    EdgeError,
    ForbiddenError,
    InternalError,
    MaintenanceError,
    MfxApiError,
    MfxError,
    MfxTimeout,
    MfxTransportError,
    NotFoundError,
    PlacementError,
    RateLimitError,
    StateError,
    TenantDisabledError,
    TenantSuspendedError,
    UnsupportedBrokerError,
    UpstreamError,
    ValidationError,
)
from mfx.expert_advisors import EaRecord, EaTelemetry, EaTelemetryLost, telemetry_of
from mfx.live_account import AccountView, LiveAccount
from mfx.logging import MfxLogger, configure_logging, get_logger
from mfx.md import Book, SubscriptionDegraded, SubscriptionRecovered, book_of, subscription_event
from mfx.pages import Page
from mfx.results import CommandState, ExecutionResult, Reason, Tickets
from mfx.secrets import Secret
from mfx.signing import SigningKey
from mfx.streaming import (
    Channel,
    ChannelRefused,
    MfxStream,
    Resync,
    StreamMessage,
    StreamStats,
)
from mfx.sync import SyncMfxClient
from mfx.terminals import OFFLINE_IS_TEMPORARY, is_usable
from mfx.webhooks import WebhookSignatureError, verify

__all__ = [
    "OFFLINE_IS_TEMPORARY",
    "AuthError",
    "Budget",
    "AccountView",
    "Book",
    "Channel",
    "CommandState",
    "ConflictError",
    "DependencyUnavailableError",
    "EdgeError",
    "EaRecord",
    "EaTelemetry",
    "EaTelemetryLost",
    "ExecutionResult",
    "ForbiddenError",
    "InternalError",
    "MaintenanceError",
    "MfxApiError",
    "MfxClient",
    "MfxError",
    "MfxLogger",
    "MfxStream",
    "MfxTimeout",
    "MfxTransportError",
    "NotFoundError",
    "Page",
    "PlacementError",
    "RateLimitError",
    "Reason",
    "LiveAccount",
    "Resync",
    "Secret",
    "SigningKey",
    "StateError",
    "TenantDisabledError",
    "TenantSuspendedError",
    "ChannelRefused",
    "StreamMessage",
    "StreamStats",
    "SubscriptionDegraded",
    "SubscriptionRecovered",
    "SyncMfxClient",
    "Tickets",
    "UnsupportedBrokerError",
    "UpstreamError",
    "ValidationError",
    "WebhookSignatureError",
    "__version__",
    "configure_logging",
    "is_usable",
    "get_logger",
    "book_of",
    "subscription_event",
    "telemetry_of",
    "verify",
]

__version__ = "0.9.19"
