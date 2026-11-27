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

from mfx._version import __version__
from mfx.client import SERVICE_AGREEMENT_WARNING, Budget, CallTiming, MfxClient
from mfx.copy_trading import REFUSAL_REASONS, CopyPage
from mfx.errors import (
    AuthError,
    BillingAction,
    BillingPaymentRequiredError,
    ConflictError,
    DependencyUnavailableError,
    DocumentDue,
    EdgeError,
    ForbiddenError,
    InternalError,
    MaintenanceError,
    MfxApiError,
    MfxError,
    MfxTimeout,
    MfxTransportError,
    NotFoundError,
    PaymentRequiredError,
    PlacementError,
    PlanChange,
    RateLimitError,
    RiskOverrideRequiredError,
    RiskRefusal,
    RiskRefusedError,
    ServiceAgreementNotAccepted,
    StateError,
    TenantDisabledError,
    TenantSuspendedError,
    TermsNotAccepted,
    UnsupportedBrokerError,
    UpstreamError,
    ValidationError,
)
from mfx.events import (
    CandleClosed,
    CopyClosedEvent,
    CopyCopied,
    CopyDrift,
    CopyRefused,
    CopyStateChanged,
    CopyStopoutEvent,
    OrderClosed,
    OrderModified,
    OrderPlaced,
    PositionClosed,
    PositionModified,
    PositionOpened,
    RiskCoverageChanged,
    RiskPeriodClosed,
    RiskProgrammeResult,
    RiskRuleEvent,
    TerminalStateChanged,
    event_of,
)
from mfx.expert_advisors import EaRecord, EaTelemetry, EaTelemetryLost, telemetry_of
from mfx.live_account import AccountView, LiveAccount
from mfx.logging import MfxLogger, configure_logging, get_logger
from mfx.md import Book, SubscriptionDegraded, SubscriptionRecovered, book_of, subscription_event
from mfx.pages import Page
from mfx.results import CommandState, ExecutionResult, Reason, Tickets, VenueDeal
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
    "event_of",
    "TerminalStateChanged",
    "PositionOpened",
    "PositionModified",
    "PositionClosed",
    "OrderPlaced",
    "OrderModified",
    "OrderClosed",
    "CandleClosed",
    "CopyClosedEvent",
    "CopyCopied",
    "CopyDrift",
    "CopyPage",
    "CopyRefused",
    "CopyStateChanged",
    "CopyStopoutEvent",
    "REFUSAL_REASONS",
    "OFFLINE_IS_TEMPORARY",
    "SERVICE_AGREEMENT_WARNING",
    "AuthError",
    "BillingAction",
    "BillingPaymentRequiredError",
    "Budget",
    "CallTiming",
    "AccountView",
    "Book",
    "Channel",
    "CommandState",
    "ConflictError",
    "DependencyUnavailableError",
    "DocumentDue",
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
    "PaymentRequiredError",
    "PlacementError",
    "PlanChange",
    "RateLimitError",
    "Reason",
    "RiskCoverageChanged",
    "RiskOverrideRequiredError",
    "RiskPeriodClosed",
    "RiskProgrammeResult",
    "RiskRefusal",
    "RiskRefusedError",
    "RiskRuleEvent",
    "LiveAccount",
    "Resync",
    "Secret",
    "ServiceAgreementNotAccepted",
    "SigningKey",
    "StateError",
    "TenantDisabledError",
    "TenantSuspendedError",
    "TermsNotAccepted",
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
    "VenueDeal",
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
