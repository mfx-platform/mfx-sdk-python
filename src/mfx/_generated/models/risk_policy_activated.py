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

from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskPolicyActivated")


@_attrs_define
class RiskPolicyActivated:
    """`data` of `risk.policy_activated`: an account's policy version changed, or it was ended

    Attributes:
        schema_version (str):
        terminal_id (UUID):
        policy_id (Union[None, UUID]):
        version (Union[None, int]):
        previous_version (Union[None, int]):
        relaxes (bool):
        at (datetime.datetime):
    """

    schema_version: str
    terminal_id: UUID
    policy_id: Union[None, UUID]
    version: Union[None, int]
    previous_version: Union[None, int]
    relaxes: bool
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        policy_id: Union[None, str]
        if isinstance(self.policy_id, UUID):
            policy_id = str(self.policy_id)
        else:
            policy_id = self.policy_id

        version: Union[None, int]
        version = self.version

        previous_version: Union[None, int]
        previous_version = self.previous_version

        relaxes = self.relaxes

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "policy_id": policy_id,
                "version": version,
                "previous_version": previous_version,
                "relaxes": relaxes,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

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

        def _parse_previous_version(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        previous_version = _parse_previous_version(d.pop("previous_version"))

        relaxes = d.pop("relaxes")

        at = isoparse(d.pop("at"))

        risk_policy_activated = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            policy_id=policy_id,
            version=version,
            previous_version=previous_version,
            relaxes=relaxes,
            at=at,
        )

        risk_policy_activated.additional_properties = d
        return risk_policy_activated

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
