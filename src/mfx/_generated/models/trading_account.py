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

from ..models.trading_account_environment_type_1 import TradingAccountEnvironmentType1
from ..models.trading_account_environment_type_2_type_1 import (
    TradingAccountEnvironmentType2Type1,
)
from ..models.trading_account_environment_type_3_type_1 import (
    TradingAccountEnvironmentType3Type1,
)
from ..models.trading_account_state import TradingAccountState
from ..models.trading_account_venue import TradingAccountVenue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trading_account_broker import TradingAccountBroker
    from ..models.trading_account_runners_item import TradingAccountRunnersItem


T = TypeVar("T", bound="TradingAccount")


@_attrs_define
class TradingAccount:
    """One trading account at one venue. Its state is its runner's, in words that hold on every venue. An MT5 account's id
    is the id of the terminal you created for it; with HA, both terminals run the one account and `runners` names them.

        Attributes:
            id (UUID):
            venue (TradingAccountVenue): The trading technology. cTrader accounts appear from the cTrader release
            environment (Union[None, TradingAccountEnvironmentType1, TradingAccountEnvironmentType2Type1,
                TradingAccountEnvironmentType3Type1]): live or demo. MT5: from the account's own type once the terminal has
                logged in (contest is demo); null until then
            label (Union[None, str]): Your own name for the account; null when none is set
            state (TradingAccountState): PENDING: being placed. CONNECTING: logging in. CONNECTED: logged in, nothing
                failing. DEGRADED: logged in with a condition failing, or its runner cannot run it for now (it comes back by
                itself). PAUSED: drained by you, or stopped while your account is suspended. REAUTH_NEEDED: the broker refused
                the login as an invalid account; submit the credential again. RETIRED, FAILED: as the terminal's. For MT5 it is
                the writing terminal's state (`GET /terminals/{id}` has the detail)
            broker (TradingAccountBroker):
            login_masked (Union[None, str]): e.g. ****3456; null until a credential is submitted
            runners (list['TradingAccountRunnersItem']): MT5: the terminals that run the account, yours to read at
                /terminals/{id}; empty for a venue MFX runs without a terminal of yours
            created_at (datetime.datetime):
    """

    id: UUID
    venue: TradingAccountVenue
    environment: Union[
        None,
        TradingAccountEnvironmentType1,
        TradingAccountEnvironmentType2Type1,
        TradingAccountEnvironmentType3Type1,
    ]
    label: Union[None, str]
    state: TradingAccountState
    broker: "TradingAccountBroker"
    login_masked: Union[None, str]
    runners: list["TradingAccountRunnersItem"]
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.trading_account_broker import TradingAccountBroker
        from ..models.trading_account_runners_item import TradingAccountRunnersItem

        id = str(self.id)

        venue = self.venue.value

        environment: Union[None, str]
        if isinstance(self.environment, TradingAccountEnvironmentType1):
            environment = self.environment.value
        elif isinstance(self.environment, TradingAccountEnvironmentType2Type1):
            environment = self.environment.value
        elif isinstance(self.environment, TradingAccountEnvironmentType3Type1):
            environment = self.environment.value
        else:
            environment = self.environment

        label: Union[None, str]
        label = self.label

        state = self.state.value

        broker = self.broker.to_dict()

        login_masked: Union[None, str]
        login_masked = self.login_masked

        runners = []
        for runners_item_data in self.runners:
            runners_item = runners_item_data.to_dict()
            runners.append(runners_item)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "venue": venue,
                "environment": environment,
                "label": label,
                "state": state,
                "broker": broker,
                "login_masked": login_masked,
                "runners": runners,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trading_account_broker import TradingAccountBroker
        from ..models.trading_account_runners_item import TradingAccountRunnersItem

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        venue = TradingAccountVenue(d.pop("venue"))

        def _parse_environment(
            data: object,
        ) -> Union[
            None,
            TradingAccountEnvironmentType1,
            TradingAccountEnvironmentType2Type1,
            TradingAccountEnvironmentType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_type_1 = TradingAccountEnvironmentType1(data)

                return environment_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_type_2_type_1 = TradingAccountEnvironmentType2Type1(data)

                return environment_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_type_3_type_1 = TradingAccountEnvironmentType3Type1(data)

                return environment_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TradingAccountEnvironmentType1,
                    TradingAccountEnvironmentType2Type1,
                    TradingAccountEnvironmentType3Type1,
                ],
                data,
            )

        environment = _parse_environment(d.pop("environment"))

        def _parse_label(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        label = _parse_label(d.pop("label"))

        state = TradingAccountState(d.pop("state"))

        broker = TradingAccountBroker.from_dict(d.pop("broker"))

        def _parse_login_masked(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        login_masked = _parse_login_masked(d.pop("login_masked"))

        runners = []
        _runners = d.pop("runners")
        for runners_item_data in _runners:
            runners_item = TradingAccountRunnersItem.from_dict(runners_item_data)

            runners.append(runners_item)

        created_at = isoparse(d.pop("created_at"))

        trading_account = cls(
            id=id,
            venue=venue,
            environment=environment,
            label=label,
            state=state,
            broker=broker,
            login_masked=login_masked,
            runners=runners,
            created_at=created_at,
        )

        trading_account.additional_properties = d
        return trading_account

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
