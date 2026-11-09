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

from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_preview_inputs import CopyPreviewInputs
    from ..models.copy_preview_refusal_type_0 import CopyPreviewRefusalType0
    from ..models.copy_preview_rows_item import CopyPreviewRowsItem


T = TypeVar("T", bound="CopyPreview")


@_attrs_define
class CopyPreview:
    """
    Attributes:
        account_id (UUID):
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        leader_id (UUID):
        refusal (Union['CopyPreviewRefusalType0', None]): Why the follow itself would be refused, as creating it would
            answer; null when it would be accepted
        inputs (CopyPreviewInputs): The figures the rows were worked from
        rows (list['CopyPreviewRowsItem']):
    """

    account_id: UUID
    venue: Venue
    leader_id: UUID
    refusal: Union["CopyPreviewRefusalType0", None]
    inputs: "CopyPreviewInputs"
    rows: list["CopyPreviewRowsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_preview_inputs import CopyPreviewInputs
        from ..models.copy_preview_refusal_type_0 import CopyPreviewRefusalType0
        from ..models.copy_preview_rows_item import CopyPreviewRowsItem

        account_id = str(self.account_id)

        venue = self.venue.value

        leader_id = str(self.leader_id)

        refusal: Union[None, dict[str, Any]]
        if isinstance(self.refusal, CopyPreviewRefusalType0):
            refusal = self.refusal.to_dict()
        else:
            refusal = self.refusal

        inputs = self.inputs.to_dict()

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "venue": venue,
                "leader_id": leader_id,
                "refusal": refusal,
                "inputs": inputs,
                "rows": rows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_preview_inputs import CopyPreviewInputs
        from ..models.copy_preview_refusal_type_0 import CopyPreviewRefusalType0
        from ..models.copy_preview_rows_item import CopyPreviewRowsItem

        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        leader_id = UUID(d.pop("leader_id"))

        def _parse_refusal(data: object) -> Union["CopyPreviewRefusalType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                refusal_type_0 = CopyPreviewRefusalType0.from_dict(data)

                return refusal_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyPreviewRefusalType0", None], data)

        refusal = _parse_refusal(d.pop("refusal"))

        inputs = CopyPreviewInputs.from_dict(d.pop("inputs"))

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = CopyPreviewRowsItem.from_dict(rows_item_data)

            rows.append(rows_item)

        copy_preview = cls(
            account_id=account_id,
            venue=venue,
            leader_id=leader_id,
            refusal=refusal,
            inputs=inputs,
            rows=rows,
        )

        copy_preview.additional_properties = d
        return copy_preview

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
