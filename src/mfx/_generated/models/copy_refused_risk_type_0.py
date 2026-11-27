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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyRefusedRiskType0")


@_attrs_define
class CopyRefusedRiskType0:
    """Risk Management's detail of a risk_rule refusal, in the 422 risk_refused shape (reason, rule, policy_id, version,
    used, limit, would_be, and challenge_id, challenge_version when a challenge's rule refused): figures as decimal
    strings in the follower account's currency (in US dollars when reason is copy_exposure_cap, limit being the
    follower's share of its group's cap), every field null where the host gave none. A host that predates the detail
    sends its reason alone, kept with every other field null. Null on every other row

        Attributes:
            reason (str): Risk Management's reason, for example risk_daily_loss or risk_inputs_stale; copy_exposure_cap
                (rule gross_exposure_cap, no policy) when the copy would take the follower past its share of its group's gross
                exposure cap
            rule (Union[None, str]):
            policy_id (Union[None, UUID]):
            version (Union[None, int]): The policy's version
            used (Union[None, str]):
            limit (Union[None, str]):
            would_be (Union[None, str]):
            challenge_id (Union[None, UUID, Unset]):
            challenge_version (Union[None, Unset, int]):
    """

    reason: str
    rule: Union[None, str]
    policy_id: Union[None, UUID]
    version: Union[None, int]
    used: Union[None, str]
    limit: Union[None, str]
    would_be: Union[None, str]
    challenge_id: Union[None, UUID, Unset] = UNSET
    challenge_version: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        rule: Union[None, str]
        rule = self.rule

        policy_id: Union[None, str]
        if isinstance(self.policy_id, UUID):
            policy_id = str(self.policy_id)
        else:
            policy_id = self.policy_id

        version: Union[None, int]
        version = self.version

        used: Union[None, str]
        used = self.used

        limit: Union[None, str]
        limit = self.limit

        would_be: Union[None, str]
        would_be = self.would_be

        challenge_id: Union[None, Unset, str]
        if isinstance(self.challenge_id, Unset):
            challenge_id = UNSET
        elif isinstance(self.challenge_id, UUID):
            challenge_id = str(self.challenge_id)
        else:
            challenge_id = self.challenge_id

        challenge_version: Union[None, Unset, int]
        if isinstance(self.challenge_version, Unset):
            challenge_version = UNSET
        else:
            challenge_version = self.challenge_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
                "rule": rule,
                "policy_id": policy_id,
                "version": version,
                "used": used,
                "limit": limit,
                "would_be": would_be,
            }
        )
        if challenge_id is not UNSET:
            field_dict["challenge_id"] = challenge_id
        if challenge_version is not UNSET:
            field_dict["challenge_version"] = challenge_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        def _parse_rule(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rule = _parse_rule(d.pop("rule"))

        def _parse_policy_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_id_type_0 = UUID(data)

                return policy_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        policy_id = _parse_policy_id(d.pop("policy_id"))

        def _parse_version(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        version = _parse_version(d.pop("version"))

        def _parse_used(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        used = _parse_used(d.pop("used"))

        def _parse_limit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit = _parse_limit(d.pop("limit"))

        def _parse_would_be(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        would_be = _parse_would_be(d.pop("would_be"))

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

        def _parse_challenge_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        challenge_version = _parse_challenge_version(d.pop("challenge_version", UNSET))

        copy_refused_risk_type_0 = cls(
            reason=reason,
            rule=rule,
            policy_id=policy_id,
            version=version,
            used=used,
            limit=limit,
            would_be=would_be,
            challenge_id=challenge_id,
            challenge_version=challenge_version,
        )

        copy_refused_risk_type_0.additional_properties = d
        return copy_refused_risk_type_0

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
