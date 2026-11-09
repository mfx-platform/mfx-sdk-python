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

from ..models.copy_group_state import CopyGroupState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_group_template import CopyGroupTemplate


T = TypeVar("T", bound="CopyGroup")


@_attrs_define
class CopyGroup:
    """
    Attributes:
        id (UUID):
        name (str):
        template (CopyGroupTemplate): What a follower created into the group starts from, for every field it leaves out
        gross_exposure_cap (Union[None, str]):
        placement_policy (Union[None, str]):
        state (CopyGroupState):
        followers_live (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: UUID
    name: str
    template: "CopyGroupTemplate"
    gross_exposure_cap: Union[None, str]
    placement_policy: Union[None, str]
    state: CopyGroupState
    followers_live: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_template import CopyGroupTemplate

        id = str(self.id)

        name = self.name

        template = self.template.to_dict()

        gross_exposure_cap: Union[None, str]
        gross_exposure_cap = self.gross_exposure_cap

        placement_policy: Union[None, str]
        placement_policy = self.placement_policy

        state = self.state.value

        followers_live = self.followers_live

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "template": template,
                "gross_exposure_cap": gross_exposure_cap,
                "placement_policy": placement_policy,
                "state": state,
                "followers_live": followers_live,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_template import CopyGroupTemplate

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        template = CopyGroupTemplate.from_dict(d.pop("template"))

        def _parse_gross_exposure_cap(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        gross_exposure_cap = _parse_gross_exposure_cap(d.pop("gross_exposure_cap"))

        def _parse_placement_policy(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        placement_policy = _parse_placement_policy(d.pop("placement_policy"))

        state = CopyGroupState(d.pop("state"))

        followers_live = d.pop("followers_live")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        copy_group = cls(
            id=id,
            name=name,
            template=template,
            gross_exposure_cap=gross_exposure_cap,
            placement_policy=placement_policy,
            state=state,
            followers_live=followers_live,
            created_at=created_at,
            updated_at=updated_at,
        )

        copy_group.additional_properties = d
        return copy_group

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
