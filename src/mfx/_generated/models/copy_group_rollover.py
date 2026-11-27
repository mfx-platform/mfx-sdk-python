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

from ..models.copy_group_rollover_fields_item import CopyGroupRolloverFieldsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyGroupRollover")


@_attrs_define
class CopyGroupRollover:
    """
    Attributes:
        dry_run (bool): true answers what would change and changes nothing
        fields (Union[Unset, list[CopyGroupRolloverFieldsItem]]): The template fields to set; by default every field the
            template sets
        after (Union[None, UUID, Unset]): The page after this member id: the previous answer's next_after
        limit (Union[Unset, int]):  Default: 500.
    """

    dry_run: bool
    fields: Union[Unset, list[CopyGroupRolloverFieldsItem]] = UNSET
    after: Union[None, UUID, Unset] = UNSET
    limit: Union[Unset, int] = 500

    def to_dict(self) -> dict[str, Any]:
        dry_run = self.dry_run

        fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.value
                fields.append(fields_item)

        after: Union[None, Unset, str]
        if isinstance(self.after, Unset):
            after = UNSET
        elif isinstance(self.after, UUID):
            after = str(self.after)
        else:
            after = self.after

        limit = self.limit

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dry_run": dry_run,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields
        if after is not UNSET:
            field_dict["after"] = after
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dry_run = d.pop("dry_run")

        fields = []
        _fields = d.pop("fields", UNSET)
        for fields_item_data in _fields or []:
            fields_item = CopyGroupRolloverFieldsItem._read(fields_item_data)

            fields.append(fields_item)

        def _parse_after(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                after_type_0 = UUID(data)

                return after_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        after = _parse_after(d.pop("after", UNSET))

        limit = d.pop("limit", UNSET)

        copy_group_rollover = cls(
            dry_run=dry_run,
            fields=fields,
            after=after,
            limit=limit,
        )

        return copy_group_rollover
