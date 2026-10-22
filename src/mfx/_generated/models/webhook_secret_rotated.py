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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookSecretRotated")


@_attrs_define
class WebhookSecretRotated:
    """The new secret, shown once. The previous one signs beside it until `previous_secret_until`, a day

    Attributes:
        secret (str):
        previous_secret_until (datetime.datetime):
    """

    secret: str
    previous_secret_until: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        secret = self.secret

        previous_secret_until = self.previous_secret_until.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secret": secret,
                "previous_secret_until": previous_secret_until,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        secret = d.pop("secret")

        previous_secret_until = isoparse(d.pop("previous_secret_until"))

        webhook_secret_rotated = cls(
            secret=secret,
            previous_secret_until=previous_secret_until,
        )

        webhook_secret_rotated.additional_properties = d
        return webhook_secret_rotated

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
