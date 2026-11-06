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

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskChallengeAccountResultType0")


@_attrs_define
class RiskChallengeAccountResultType0:
    """
    Attributes:
        rule (Union[None, str]): The rule that failed it; null on a pass
        at (datetime.datetime):
    """

    rule: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rule: Union[None, str]
        rule = self.rule

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule": rule,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_rule(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rule = _parse_rule(d.pop("rule"))

        at = isoparse(d.pop("at"))

        risk_challenge_account_result_type_0 = cls(
            rule=rule,
            at=at,
        )

        risk_challenge_account_result_type_0.additional_properties = d
        return risk_challenge_account_result_type_0

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
