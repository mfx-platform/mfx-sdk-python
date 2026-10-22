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

from ..models.md_subscription_degraded_cause_type_1 import (
    MdSubscriptionDegradedCauseType1,
)
from ..models.md_subscription_degraded_cause_type_2_type_1 import (
    MdSubscriptionDegradedCauseType2Type1,
)
from ..models.md_subscription_degraded_cause_type_3_type_1 import (
    MdSubscriptionDegradedCauseType3Type1,
)
from ..models.md_subscription_degraded_reason_type_1 import (
    MdSubscriptionDegradedReasonType1,
)
from ..models.md_subscription_degraded_reason_type_2_type_1 import (
    MdSubscriptionDegradedReasonType2Type1,
)
from ..models.md_subscription_degraded_reason_type_3_type_1 import (
    MdSubscriptionDegradedReasonType3Type1,
)
from ..models.md_subscription_delivery import MdSubscriptionDelivery
from ..models.md_subscription_state import MdSubscriptionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref import Ref


T = TypeVar("T", bound="MdSubscription")


@_attrs_define
class MdSubscription:
    """
    Attributes:
        id (UUID):
        broker (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        server (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        symbol (str):
        timeframes (list[str]):
        delivery (MdSubscriptionDelivery):
        state (MdSubscriptionState): `pending` until the first tick. `degraded` when the symbol cannot tick or should be
            ticking and is not (`degraded_reason`); its stream stays granted
        created_at (datetime.datetime):
        degraded_reason (Union[MdSubscriptionDegradedReasonType1, MdSubscriptionDegradedReasonType2Type1,
            MdSubscriptionDegradedReasonType3Type1, None, Unset]): Why the subscription is `degraded`; null in every other
            state. `symbol_removed`: the broker no longer lists the symbol. `subscription_refused`: the broker refused it on
            every one of your ACTIVE terminals on the server that carries it. `terminal_disconnected`: you have no ACTIVE
            terminal on the server and no report of the symbol has arrived for the unknown window. `report_stale`: a
            terminal is ACTIVE and still none has arrived, for instance because none of them carries the symbol any more.
            `no_ticks_in_session`: the symbol's own hours say it is trading and it has not ticked for the silence window
            (measured at the newest report); it recovers on two reports in a row that each bring a new tick inside the
            window, or when its session closes. Nothing is degraded for silence outside the symbol's trading session.
        degraded_since (Union[None, Unset, datetime.datetime]): When it became degraded; null in every other state
        degraded_cause (Union[MdSubscriptionDegradedCauseType1, MdSubscriptionDegradedCauseType2Type1,
            MdSubscriptionDegradedCauseType3Type1, None, Unset]): Whose cause the degradation is; null in every other state.
            `broker`: the broker removed or refused the symbol, or, for `no_ticks_in_session`, no terminal on the server has
            ticked it inside the silence window either. `platform`: your terminals are lost or not reporting, or the symbol
            is ticking for other terminals on the server and not for this subscription. Judged again on every pass; a change
            sends no event.
        first_tick_at (Union[None, Unset, datetime.datetime]):
    """

    id: UUID
    broker: "Ref"
    server: "Ref"
    symbol: str
    timeframes: list[str]
    delivery: MdSubscriptionDelivery
    state: MdSubscriptionState
    created_at: datetime.datetime
    degraded_reason: Union[
        MdSubscriptionDegradedReasonType1,
        MdSubscriptionDegradedReasonType2Type1,
        MdSubscriptionDegradedReasonType3Type1,
        None,
        Unset,
    ] = UNSET
    degraded_since: Union[None, Unset, datetime.datetime] = UNSET
    degraded_cause: Union[
        MdSubscriptionDegradedCauseType1,
        MdSubscriptionDegradedCauseType2Type1,
        MdSubscriptionDegradedCauseType3Type1,
        None,
        Unset,
    ] = UNSET
    first_tick_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ref import Ref

        id = str(self.id)

        broker = self.broker.to_dict()

        server = self.server.to_dict()

        symbol = self.symbol

        timeframes = self.timeframes

        delivery = self.delivery.value

        state = self.state.value

        created_at = self.created_at.isoformat()

        degraded_reason: Union[None, Unset, str]
        if isinstance(self.degraded_reason, Unset):
            degraded_reason = UNSET
        elif isinstance(self.degraded_reason, MdSubscriptionDegradedReasonType1):
            degraded_reason = self.degraded_reason.value
        elif isinstance(self.degraded_reason, MdSubscriptionDegradedReasonType2Type1):
            degraded_reason = self.degraded_reason.value
        elif isinstance(self.degraded_reason, MdSubscriptionDegradedReasonType3Type1):
            degraded_reason = self.degraded_reason.value
        else:
            degraded_reason = self.degraded_reason

        degraded_since: Union[None, Unset, str]
        if isinstance(self.degraded_since, Unset):
            degraded_since = UNSET
        elif isinstance(self.degraded_since, datetime.datetime):
            degraded_since = self.degraded_since.isoformat()
        else:
            degraded_since = self.degraded_since

        degraded_cause: Union[None, Unset, str]
        if isinstance(self.degraded_cause, Unset):
            degraded_cause = UNSET
        elif isinstance(self.degraded_cause, MdSubscriptionDegradedCauseType1):
            degraded_cause = self.degraded_cause.value
        elif isinstance(self.degraded_cause, MdSubscriptionDegradedCauseType2Type1):
            degraded_cause = self.degraded_cause.value
        elif isinstance(self.degraded_cause, MdSubscriptionDegradedCauseType3Type1):
            degraded_cause = self.degraded_cause.value
        else:
            degraded_cause = self.degraded_cause

        first_tick_at: Union[None, Unset, str]
        if isinstance(self.first_tick_at, Unset):
            first_tick_at = UNSET
        elif isinstance(self.first_tick_at, datetime.datetime):
            first_tick_at = self.first_tick_at.isoformat()
        else:
            first_tick_at = self.first_tick_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "broker": broker,
                "server": server,
                "symbol": symbol,
                "timeframes": timeframes,
                "delivery": delivery,
                "state": state,
                "created_at": created_at,
            }
        )
        if degraded_reason is not UNSET:
            field_dict["degraded_reason"] = degraded_reason
        if degraded_since is not UNSET:
            field_dict["degraded_since"] = degraded_since
        if degraded_cause is not UNSET:
            field_dict["degraded_cause"] = degraded_cause
        if first_tick_at is not UNSET:
            field_dict["first_tick_at"] = first_tick_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ref import Ref

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        broker = Ref.from_dict(d.pop("broker"))

        server = Ref.from_dict(d.pop("server"))

        symbol = d.pop("symbol")

        timeframes = cast(list[str], d.pop("timeframes"))

        delivery = MdSubscriptionDelivery(d.pop("delivery"))

        state = MdSubscriptionState(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_degraded_reason(
            data: object,
        ) -> Union[
            MdSubscriptionDegradedReasonType1,
            MdSubscriptionDegradedReasonType2Type1,
            MdSubscriptionDegradedReasonType3Type1,
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_reason_type_1 = MdSubscriptionDegradedReasonType1(data)

                return degraded_reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_reason_type_2_type_1 = MdSubscriptionDegradedReasonType2Type1(data)

                return degraded_reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_reason_type_3_type_1 = MdSubscriptionDegradedReasonType3Type1(data)

                return degraded_reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    MdSubscriptionDegradedReasonType1,
                    MdSubscriptionDegradedReasonType2Type1,
                    MdSubscriptionDegradedReasonType3Type1,
                    None,
                    Unset,
                ],
                data,
            )

        degraded_reason = _parse_degraded_reason(d.pop("degraded_reason", UNSET))

        def _parse_degraded_since(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_since_type_0 = isoparse(data)

                return degraded_since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        degraded_since = _parse_degraded_since(d.pop("degraded_since", UNSET))

        def _parse_degraded_cause(
            data: object,
        ) -> Union[
            MdSubscriptionDegradedCauseType1,
            MdSubscriptionDegradedCauseType2Type1,
            MdSubscriptionDegradedCauseType3Type1,
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_cause_type_1 = MdSubscriptionDegradedCauseType1(data)

                return degraded_cause_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_cause_type_2_type_1 = MdSubscriptionDegradedCauseType2Type1(data)

                return degraded_cause_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                degraded_cause_type_3_type_1 = MdSubscriptionDegradedCauseType3Type1(data)

                return degraded_cause_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    MdSubscriptionDegradedCauseType1,
                    MdSubscriptionDegradedCauseType2Type1,
                    MdSubscriptionDegradedCauseType3Type1,
                    None,
                    Unset,
                ],
                data,
            )

        degraded_cause = _parse_degraded_cause(d.pop("degraded_cause", UNSET))

        def _parse_first_tick_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_tick_at_type_0 = isoparse(data)

                return first_tick_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        first_tick_at = _parse_first_tick_at(d.pop("first_tick_at", UNSET))

        md_subscription = cls(
            id=id,
            broker=broker,
            server=server,
            symbol=symbol,
            timeframes=timeframes,
            delivery=delivery,
            state=state,
            created_at=created_at,
            degraded_reason=degraded_reason,
            degraded_since=degraded_since,
            degraded_cause=degraded_cause,
            first_tick_at=first_tick_at,
        )

        md_subscription.additional_properties = d
        return md_subscription

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
