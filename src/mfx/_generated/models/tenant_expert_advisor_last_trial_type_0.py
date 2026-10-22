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

from ..models.tenant_expert_advisor_last_trial_type_0_ended_reason_type_1 import (
    TenantExpertAdvisorLastTrialType0EndedReasonType1,
)
from ..models.tenant_expert_advisor_last_trial_type_0_ended_reason_type_2_type_1 import (
    TenantExpertAdvisorLastTrialType0EndedReasonType2Type1,
)
from ..models.tenant_expert_advisor_last_trial_type_0_ended_reason_type_3_type_1 import (
    TenantExpertAdvisorLastTrialType0EndedReasonType3Type1,
)
from ..models.tenant_expert_advisor_last_trial_type_0_state import (
    TenantExpertAdvisorLastTrialType0State,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_trial import EaTrial


T = TypeVar("T", bound="TenantExpertAdvisorLastTrialType0")


@_attrs_define
class TenantExpertAdvisorLastTrialType0:
    """
    Attributes:
        terminal_id (UUID):
        state (TenantExpertAdvisorLastTrialType0State): Where that attachment stands now; detached once it has left the
            terminal
        symbol (str):
        timeframe (str): e.g. M1
        ended_at (Union[None, datetime.datetime]): When the attachment left the terminal; null while it is on it
        ended_reason (Union[None, TenantExpertAdvisorLastTrialType0EndedReasonType1,
            TenantExpertAdvisorLastTrialType0EndedReasonType2Type1,
            TenantExpertAdvisorLastTrialType0EndedReasonType3Type1]): Why the platform took it off the terminal; null while
            it is on it, and for your own detach
        trial (EaTrial): A trial with trading off on one terminal
    """

    terminal_id: UUID
    state: TenantExpertAdvisorLastTrialType0State
    symbol: str
    timeframe: str
    ended_at: Union[None, datetime.datetime]
    ended_reason: Union[
        None,
        TenantExpertAdvisorLastTrialType0EndedReasonType1,
        TenantExpertAdvisorLastTrialType0EndedReasonType2Type1,
        TenantExpertAdvisorLastTrialType0EndedReasonType3Type1,
    ]
    trial: "EaTrial"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_trial import EaTrial

        terminal_id = str(self.terminal_id)

        state = self.state.value

        symbol = self.symbol

        timeframe = self.timeframe

        ended_at: Union[None, str]
        if isinstance(self.ended_at, datetime.datetime):
            ended_at = self.ended_at.isoformat()
        else:
            ended_at = self.ended_at

        ended_reason: Union[None, str]
        if isinstance(self.ended_reason, TenantExpertAdvisorLastTrialType0EndedReasonType1):
            ended_reason = self.ended_reason.value
        elif isinstance(self.ended_reason, TenantExpertAdvisorLastTrialType0EndedReasonType2Type1):
            ended_reason = self.ended_reason.value
        elif isinstance(self.ended_reason, TenantExpertAdvisorLastTrialType0EndedReasonType3Type1):
            ended_reason = self.ended_reason.value
        else:
            ended_reason = self.ended_reason

        trial = self.trial.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "state": state,
                "symbol": symbol,
                "timeframe": timeframe,
                "ended_at": ended_at,
                "ended_reason": ended_reason,
                "trial": trial,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_trial import EaTrial

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        state = TenantExpertAdvisorLastTrialType0State(d.pop("state"))

        symbol = d.pop("symbol")

        timeframe = d.pop("timeframe")

        def _parse_ended_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_at_type_0 = isoparse(data)

                return ended_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        ended_at = _parse_ended_at(d.pop("ended_at"))

        def _parse_ended_reason(
            data: object,
        ) -> Union[
            None,
            TenantExpertAdvisorLastTrialType0EndedReasonType1,
            TenantExpertAdvisorLastTrialType0EndedReasonType2Type1,
            TenantExpertAdvisorLastTrialType0EndedReasonType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_reason_type_1 = TenantExpertAdvisorLastTrialType0EndedReasonType1(data)

                return ended_reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_reason_type_2_type_1 = TenantExpertAdvisorLastTrialType0EndedReasonType2Type1(
                    data
                )

                return ended_reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_reason_type_3_type_1 = TenantExpertAdvisorLastTrialType0EndedReasonType3Type1(
                    data
                )

                return ended_reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TenantExpertAdvisorLastTrialType0EndedReasonType1,
                    TenantExpertAdvisorLastTrialType0EndedReasonType2Type1,
                    TenantExpertAdvisorLastTrialType0EndedReasonType3Type1,
                ],
                data,
            )

        ended_reason = _parse_ended_reason(d.pop("ended_reason"))

        trial = EaTrial.from_dict(d.pop("trial"))

        tenant_expert_advisor_last_trial_type_0 = cls(
            terminal_id=terminal_id,
            state=state,
            symbol=symbol,
            timeframe=timeframe,
            ended_at=ended_at,
            ended_reason=ended_reason,
            trial=trial,
        )

        tenant_expert_advisor_last_trial_type_0.additional_properties = d
        return tenant_expert_advisor_last_trial_type_0

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
