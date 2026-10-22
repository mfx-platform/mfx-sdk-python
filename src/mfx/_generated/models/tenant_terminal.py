import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tenant_terminal_offline_reason_type_1 import (
    TenantTerminalOfflineReasonType1,
)
from ..models.tenant_terminal_offline_reason_type_2_type_1 import (
    TenantTerminalOfflineReasonType2Type1,
)
from ..models.tenant_terminal_offline_reason_type_3_type_1 import (
    TenantTerminalOfflineReasonType3Type1,
)
from ..models.tenant_terminal_redundancy import TenantTerminalRedundancy
from ..models.tenant_terminal_refresh_ms import TenantTerminalRefreshMs
from ..models.tenant_terminal_replica_role_type_1 import TenantTerminalReplicaRoleType1
from ..models.tenant_terminal_replica_role_type_2_type_1 import (
    TenantTerminalReplicaRoleType2Type1,
)
from ..models.tenant_terminal_replica_role_type_3_type_1 import (
    TenantTerminalReplicaRoleType3Type1,
)
from ..models.tenant_terminal_state import TenantTerminalState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref import Ref
    from ..models.tenant_terminal_conditions import TenantTerminalConditions
    from ..models.tenant_terminal_labels import TenantTerminalLabels


T = TypeVar("T", bound="TenantTerminal")


@_attrs_define
class TenantTerminal:
    """
    Attributes:
        id (UUID):
        farm (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        broker (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        server (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        streaming (bool):
        execution (bool):
        state (TenantTerminalState): As `Terminal.state`. OFFLINE: its cell cannot run it (`offline_reason` says why);
            it comes back by itself, or is moved after 15 minutes. DRAINED: you drained it; stopped and not billed, keeping
            its id, account and settings until you resume or retire it. PARKED: your account is suspended and its grace
            period ended; the terminal is stopped and keeps its settings, its place and its login. It returns to LOGGING_IN
            by itself when your account is reinstated, or goes to DRAINING when it is retired.
        instruments (list[str]):
        created_at (datetime.datetime):
        same_login_terminals (Union[None, Unset, int]): How many of YOUR live terminals use this terminal's broker
            login, this one included. They share the account at the broker: each sees the same balance, positions and
            history. Another tenant's use of the same login is never counted or shown here. Null until the terminal has a
            credential.
        login_masked (Union[None, Unset, str]): e.g. ****3456; null until a credential is submitted
        offline_reason (Union[None, TenantTerminalOfflineReasonType1, TenantTerminalOfflineReasonType2Type1,
            TenantTerminalOfflineReasonType3Type1, Unset]): Why an OFFLINE terminal is offline; null in every other state
        state_since (Union[None, Unset, datetime.datetime]): When it entered this state (its creation when it has not
            moved)
        state_expected_s (Union[None, Unset, int]): How long this state usually takes; null for a settled state
        conditions (Union[Unset, TenantTerminalConditions]): ProcessRunning, BrokerConnected, TicksFresh, TradeAllowed,
            CredentialLeased — each {status, reason, since, attributed_to}; absent means not yet observed
        depth_instruments (Union[Unset, list[str]]): The symbols whose market depth this terminal reads; empty when
            none. Set with PUT /terminals/{id}/instruments
        labels (Union[Unset, TenantTerminalLabels]):
        redundancy (Union[Unset, TenantTerminalRedundancy]):
        replica_role (Union[None, TenantTerminalReplicaRoleType1, TenantTerminalReplicaRoleType2Type1,
            TenantTerminalReplicaRoleType3Type1, Unset]):
        terminal_build (Union[None, Unset, int]):
        last_tick_at (Union[None, Unset, datetime.datetime]):
        refresh_ms (Union[Unset, TenantTerminalRefreshMs]): The refresh rate this terminal runs at
    """

    id: UUID
    farm: "Ref"
    broker: "Ref"
    server: "Ref"
    streaming: bool
    execution: bool
    state: TenantTerminalState
    instruments: list[str]
    created_at: datetime.datetime
    same_login_terminals: Union[None, Unset, int] = UNSET
    login_masked: Union[None, Unset, str] = UNSET
    offline_reason: Union[
        None,
        TenantTerminalOfflineReasonType1,
        TenantTerminalOfflineReasonType2Type1,
        TenantTerminalOfflineReasonType3Type1,
        Unset,
    ] = UNSET
    state_since: Union[None, Unset, datetime.datetime] = UNSET
    state_expected_s: Union[None, Unset, int] = UNSET
    conditions: Union[Unset, "TenantTerminalConditions"] = UNSET
    depth_instruments: Union[Unset, list[str]] = UNSET
    labels: Union[Unset, "TenantTerminalLabels"] = UNSET
    redundancy: Union[Unset, TenantTerminalRedundancy] = UNSET
    replica_role: Union[
        None,
        TenantTerminalReplicaRoleType1,
        TenantTerminalReplicaRoleType2Type1,
        TenantTerminalReplicaRoleType3Type1,
        Unset,
    ] = UNSET
    terminal_build: Union[None, Unset, int] = UNSET
    last_tick_at: Union[None, Unset, datetime.datetime] = UNSET
    refresh_ms: Union[Unset, TenantTerminalRefreshMs] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ref import Ref
        from ..models.tenant_terminal_conditions import TenantTerminalConditions
        from ..models.tenant_terminal_labels import TenantTerminalLabels

        id = str(self.id)

        farm = self.farm.to_dict()

        broker = self.broker.to_dict()

        server = self.server.to_dict()

        streaming = self.streaming

        execution = self.execution

        state = self.state.value

        instruments = self.instruments

        created_at = self.created_at.isoformat()

        same_login_terminals: Union[None, Unset, int]
        if isinstance(self.same_login_terminals, Unset):
            same_login_terminals = UNSET
        else:
            same_login_terminals = self.same_login_terminals

        login_masked: Union[None, Unset, str]
        if isinstance(self.login_masked, Unset):
            login_masked = UNSET
        else:
            login_masked = self.login_masked

        offline_reason: Union[None, Unset, str]
        if isinstance(self.offline_reason, Unset):
            offline_reason = UNSET
        elif isinstance(self.offline_reason, TenantTerminalOfflineReasonType1):
            offline_reason = self.offline_reason.value
        elif isinstance(self.offline_reason, TenantTerminalOfflineReasonType2Type1):
            offline_reason = self.offline_reason.value
        elif isinstance(self.offline_reason, TenantTerminalOfflineReasonType3Type1):
            offline_reason = self.offline_reason.value
        else:
            offline_reason = self.offline_reason

        state_since: Union[None, Unset, str]
        if isinstance(self.state_since, Unset):
            state_since = UNSET
        elif isinstance(self.state_since, datetime.datetime):
            state_since = self.state_since.isoformat()
        else:
            state_since = self.state_since

        state_expected_s: Union[None, Unset, int]
        if isinstance(self.state_expected_s, Unset):
            state_expected_s = UNSET
        else:
            state_expected_s = self.state_expected_s

        conditions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = self.conditions.to_dict()

        depth_instruments: Union[Unset, list[str]] = UNSET
        if not isinstance(self.depth_instruments, Unset):
            depth_instruments = self.depth_instruments

        labels: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        redundancy: Union[Unset, str] = UNSET
        if not isinstance(self.redundancy, Unset):
            redundancy = self.redundancy.value

        replica_role: Union[None, Unset, str]
        if isinstance(self.replica_role, Unset):
            replica_role = UNSET
        elif isinstance(self.replica_role, TenantTerminalReplicaRoleType1):
            replica_role = self.replica_role.value
        elif isinstance(self.replica_role, TenantTerminalReplicaRoleType2Type1):
            replica_role = self.replica_role.value
        elif isinstance(self.replica_role, TenantTerminalReplicaRoleType3Type1):
            replica_role = self.replica_role.value
        else:
            replica_role = self.replica_role

        terminal_build: Union[None, Unset, int]
        if isinstance(self.terminal_build, Unset):
            terminal_build = UNSET
        else:
            terminal_build = self.terminal_build

        last_tick_at: Union[None, Unset, str]
        if isinstance(self.last_tick_at, Unset):
            last_tick_at = UNSET
        elif isinstance(self.last_tick_at, datetime.datetime):
            last_tick_at = self.last_tick_at.isoformat()
        else:
            last_tick_at = self.last_tick_at

        refresh_ms: Union[Unset, int] = UNSET
        if not isinstance(self.refresh_ms, Unset):
            refresh_ms = self.refresh_ms.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "farm": farm,
                "broker": broker,
                "server": server,
                "streaming": streaming,
                "execution": execution,
                "state": state,
                "instruments": instruments,
                "created_at": created_at,
            }
        )
        if same_login_terminals is not UNSET:
            field_dict["same_login_terminals"] = same_login_terminals
        if login_masked is not UNSET:
            field_dict["login_masked"] = login_masked
        if offline_reason is not UNSET:
            field_dict["offline_reason"] = offline_reason
        if state_since is not UNSET:
            field_dict["state_since"] = state_since
        if state_expected_s is not UNSET:
            field_dict["state_expected_s"] = state_expected_s
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if depth_instruments is not UNSET:
            field_dict["depth_instruments"] = depth_instruments
        if labels is not UNSET:
            field_dict["labels"] = labels
        if redundancy is not UNSET:
            field_dict["redundancy"] = redundancy
        if replica_role is not UNSET:
            field_dict["replica_role"] = replica_role
        if terminal_build is not UNSET:
            field_dict["terminal_build"] = terminal_build
        if last_tick_at is not UNSET:
            field_dict["last_tick_at"] = last_tick_at
        if refresh_ms is not UNSET:
            field_dict["refresh_ms"] = refresh_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ref import Ref
        from ..models.tenant_terminal_conditions import TenantTerminalConditions
        from ..models.tenant_terminal_labels import TenantTerminalLabels

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        farm = Ref.from_dict(d.pop("farm"))

        broker = Ref.from_dict(d.pop("broker"))

        server = Ref.from_dict(d.pop("server"))

        streaming = d.pop("streaming")

        execution = d.pop("execution")

        state = TenantTerminalState(d.pop("state"))

        instruments = cast(list[str], d.pop("instruments"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_same_login_terminals(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        same_login_terminals = _parse_same_login_terminals(d.pop("same_login_terminals", UNSET))

        def _parse_login_masked(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        login_masked = _parse_login_masked(d.pop("login_masked", UNSET))

        def _parse_offline_reason(
            data: object,
        ) -> Union[
            None,
            TenantTerminalOfflineReasonType1,
            TenantTerminalOfflineReasonType2Type1,
            TenantTerminalOfflineReasonType3Type1,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offline_reason_type_1 = TenantTerminalOfflineReasonType1(data)

                return offline_reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offline_reason_type_2_type_1 = TenantTerminalOfflineReasonType2Type1(data)

                return offline_reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offline_reason_type_3_type_1 = TenantTerminalOfflineReasonType3Type1(data)

                return offline_reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TenantTerminalOfflineReasonType1,
                    TenantTerminalOfflineReasonType2Type1,
                    TenantTerminalOfflineReasonType3Type1,
                    Unset,
                ],
                data,
            )

        offline_reason = _parse_offline_reason(d.pop("offline_reason", UNSET))

        def _parse_state_since(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_since_type_0 = isoparse(data)

                return state_since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        state_since = _parse_state_since(d.pop("state_since", UNSET))

        def _parse_state_expected_s(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        state_expected_s = _parse_state_expected_s(d.pop("state_expected_s", UNSET))

        _conditions = d.pop("conditions", UNSET)
        conditions: Union[Unset, TenantTerminalConditions]
        if isinstance(_conditions, Unset):
            conditions = UNSET
        else:
            conditions = TenantTerminalConditions.from_dict(_conditions)

        depth_instruments = cast(list[str], d.pop("depth_instruments", UNSET))

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, TenantTerminalLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = TenantTerminalLabels.from_dict(_labels)

        _redundancy = d.pop("redundancy", UNSET)
        redundancy: Union[Unset, TenantTerminalRedundancy]
        if isinstance(_redundancy, Unset):
            redundancy = UNSET
        else:
            redundancy = TenantTerminalRedundancy(_redundancy)

        def _parse_replica_role(
            data: object,
        ) -> Union[
            None,
            TenantTerminalReplicaRoleType1,
            TenantTerminalReplicaRoleType2Type1,
            TenantTerminalReplicaRoleType3Type1,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                replica_role_type_1 = TenantTerminalReplicaRoleType1(data)

                return replica_role_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                replica_role_type_2_type_1 = TenantTerminalReplicaRoleType2Type1(data)

                return replica_role_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                replica_role_type_3_type_1 = TenantTerminalReplicaRoleType3Type1(data)

                return replica_role_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TenantTerminalReplicaRoleType1,
                    TenantTerminalReplicaRoleType2Type1,
                    TenantTerminalReplicaRoleType3Type1,
                    Unset,
                ],
                data,
            )

        replica_role = _parse_replica_role(d.pop("replica_role", UNSET))

        def _parse_terminal_build(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        terminal_build = _parse_terminal_build(d.pop("terminal_build", UNSET))

        def _parse_last_tick_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_tick_at_type_0 = isoparse(data)

                return last_tick_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_tick_at = _parse_last_tick_at(d.pop("last_tick_at", UNSET))

        _refresh_ms = d.pop("refresh_ms", UNSET)
        refresh_ms: Union[Unset, TenantTerminalRefreshMs]
        if isinstance(_refresh_ms, Unset):
            refresh_ms = UNSET
        else:
            refresh_ms = TenantTerminalRefreshMs(_refresh_ms)

        tenant_terminal = cls(
            id=id,
            farm=farm,
            broker=broker,
            server=server,
            streaming=streaming,
            execution=execution,
            state=state,
            instruments=instruments,
            created_at=created_at,
            same_login_terminals=same_login_terminals,
            login_masked=login_masked,
            offline_reason=offline_reason,
            state_since=state_since,
            state_expected_s=state_expected_s,
            conditions=conditions,
            depth_instruments=depth_instruments,
            labels=labels,
            redundancy=redundancy,
            replica_role=replica_role,
            terminal_build=terminal_build,
            last_tick_at=last_tick_at,
            refresh_ms=refresh_ms,
        )

        tenant_terminal.additional_properties = d
        return tenant_terminal

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
