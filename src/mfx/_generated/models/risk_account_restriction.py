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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.risk_account_restriction_state import RiskAccountRestrictionState
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskAccountRestriction")


@_attrs_define
class RiskAccountRestriction:
    """
    Attributes:
        state (RiskAccountRestrictionState):
        rule (Union[None, str]):
        since (Union[None, datetime.datetime]):
    """

    state: RiskAccountRestrictionState
    rule: Union[None, str]
    since: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        rule: Union[None, str]
        rule = self.rule

        since: Union[None, str]
        if isinstance(self.since, datetime.datetime):
            since = self.since.isoformat()
        else:
            since = self.since

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "rule": rule,
                "since": since,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = RiskAccountRestrictionState(d.pop("state"))

        def _parse_rule(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rule = _parse_rule(d.pop("rule"))

        def _parse_since(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                since_type_0 = isoparse(data)

                return since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        since = _parse_since(d.pop("since"))

        risk_account_restriction = cls(
            state=state,
            rule=rule,
            since=since,
        )

        risk_account_restriction.additional_properties = d
        return risk_account_restriction

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
