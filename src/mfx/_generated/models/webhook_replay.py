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
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookReplay")


@_attrs_define
class WebhookReplay:
    """Send again every event after `after` that the endpoint asks for, marked MFX-Delivery-Attempt: replay; or one dead
    letter by its id

        Attributes:
            after (Union[Unset, str]): A cursor of the tenant's stream. Refused 409 cursor_too_old, with details.oldest,
                when the stream no longer holds it
            failure_id (Union[Unset, UUID]):
    """

    after: Union[Unset, str] = UNSET
    failure_id: Union[Unset, UUID] = UNSET

    def to_dict(self) -> dict[str, Any]:
        after = self.after

        failure_id: Union[Unset, str] = UNSET
        if not isinstance(self.failure_id, Unset):
            failure_id = str(self.failure_id)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if after is not UNSET:
            field_dict["after"] = after
        if failure_id is not UNSET:
            field_dict["failure_id"] = failure_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        after = d.pop("after", UNSET)

        _failure_id = d.pop("failure_id", UNSET)
        failure_id: Union[Unset, UUID]
        if isinstance(_failure_id, Unset):
            failure_id = UNSET
        else:
            failure_id = UUID(_failure_id)

        webhook_replay = cls(
            after=after,
            failure_id=failure_id,
        )

        return webhook_replay
