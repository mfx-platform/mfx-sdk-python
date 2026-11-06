from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_challenge_rules import RiskChallengeRules


T = TypeVar("T", bound="RiskChallengeCreate")


@_attrs_define
class RiskChallengeCreate:
    """
    Attributes:
        name (str):
        rules (RiskChallengeRules):
    """

    name: str
    rules: "RiskChallengeRules"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_challenge_rules import RiskChallengeRules

        name = self.name

        rules = self.rules.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "rules": rules,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_challenge_rules import RiskChallengeRules

        d = dict(src_dict)
        name = d.pop("name")

        rules = RiskChallengeRules.from_dict(d.pop("rules"))

        risk_challenge_create = cls(
            name=name,
            rules=rules,
        )

        risk_challenge_create.additional_properties = d
        return risk_challenge_create

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
