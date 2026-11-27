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

from ..models.risk_rule_check_verdict import RiskRuleCheckVerdict
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskRuleCheck")


@_attrs_define
class RiskRuleCheck:
    """
    Attributes:
        rule (str):
        verdict (RiskRuleCheckVerdict):
        used (Union[None, str]):
        would_be (Union[None, str]):
        limit (Union[None, str]):
        reason (Union[None, str]): The refusal reason the pre-trade check would answer
        challenge_id (Union[None, UUID, Unset]): The challenge whose rule this row checks; absent or null on a policy's
            row
        input_ (Union[None, Unset, str]): On the row named inputs: the first input that is missing or too old, in the
            order of x-known-values. The list is not closed: a client must show a value it does not know as it is, and never
            fail on it. Absent or null on every other row
    """

    rule: str
    verdict: RiskRuleCheckVerdict
    used: Union[None, str]
    would_be: Union[None, str]
    limit: Union[None, str]
    reason: Union[None, str]
    challenge_id: Union[None, UUID, Unset] = UNSET
    input_: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rule = self.rule

        verdict = self.verdict.value

        used: Union[None, str]
        used = self.used

        would_be: Union[None, str]
        would_be = self.would_be

        limit: Union[None, str]
        limit = self.limit

        reason: Union[None, str]
        reason = self.reason

        challenge_id: Union[None, Unset, str]
        if isinstance(self.challenge_id, Unset):
            challenge_id = UNSET
        elif isinstance(self.challenge_id, UUID):
            challenge_id = str(self.challenge_id)
        else:
            challenge_id = self.challenge_id

        input_: Union[None, Unset, str]
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule": rule,
                "verdict": verdict,
                "used": used,
                "would_be": would_be,
                "limit": limit,
                "reason": reason,
            }
        )
        if challenge_id is not UNSET:
            field_dict["challenge_id"] = challenge_id
        if input_ is not UNSET:
            field_dict["input"] = input_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rule = d.pop("rule")

        verdict = RiskRuleCheckVerdict._read(d.pop("verdict"))

        def _parse_used(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        used = _parse_used(d.pop("used"))

        def _parse_would_be(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        would_be = _parse_would_be(d.pop("would_be"))

        def _parse_limit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit = _parse_limit(d.pop("limit"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_challenge_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                challenge_id_type_0 = UUID(data)

                return challenge_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        challenge_id = _parse_challenge_id(d.pop("challenge_id", UNSET))

        def _parse_input_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_ = _parse_input_(d.pop("input", UNSET))

        risk_rule_check = cls(
            rule=rule,
            verdict=verdict,
            used=used,
            would_be=would_be,
            limit=limit,
            reason=reason,
            challenge_id=challenge_id,
            input_=input_,
        )

        risk_rule_check.additional_properties = d
        return risk_rule_check

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
