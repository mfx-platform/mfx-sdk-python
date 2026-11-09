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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_group_template import CopyGroupTemplate


T = TypeVar("T", bound="CopyGroupUpdate")


@_attrs_define
class CopyGroupUpdate:
    """
    Attributes:
        name (Union[Unset, str]):
        template (Union[Unset, CopyGroupTemplate]): What a follower created into the group starts from, for every field
            it leaves out
        gross_exposure_cap (Union[None, Unset, str]):
        placement_policy (Union[None, Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    template: Union[Unset, "CopyGroupTemplate"] = UNSET
    gross_exposure_cap: Union[None, Unset, str] = UNSET
    placement_policy: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_template import CopyGroupTemplate

        name = self.name

        template: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.template, Unset):
            template = self.template.to_dict()

        gross_exposure_cap: Union[None, Unset, str]
        if isinstance(self.gross_exposure_cap, Unset):
            gross_exposure_cap = UNSET
        else:
            gross_exposure_cap = self.gross_exposure_cap

        placement_policy: Union[None, Unset, str]
        if isinstance(self.placement_policy, Unset):
            placement_policy = UNSET
        else:
            placement_policy = self.placement_policy

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if template is not UNSET:
            field_dict["template"] = template
        if gross_exposure_cap is not UNSET:
            field_dict["gross_exposure_cap"] = gross_exposure_cap
        if placement_policy is not UNSET:
            field_dict["placement_policy"] = placement_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_template import CopyGroupTemplate

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _template = d.pop("template", UNSET)
        template: Union[Unset, CopyGroupTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = CopyGroupTemplate.from_dict(_template)

        def _parse_gross_exposure_cap(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gross_exposure_cap = _parse_gross_exposure_cap(d.pop("gross_exposure_cap", UNSET))

        def _parse_placement_policy(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        placement_policy = _parse_placement_policy(d.pop("placement_policy", UNSET))

        copy_group_update = cls(
            name=name,
            template=template,
            gross_exposure_cap=gross_exposure_cap,
            placement_policy=placement_policy,
        )

        return copy_group_update
