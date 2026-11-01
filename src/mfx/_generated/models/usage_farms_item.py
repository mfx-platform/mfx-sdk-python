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
    from ..models.ref import Ref


T = TypeVar("T", bound="UsageFarmsItem")


@_attrs_define
class UsageFarmsItem:
    """
    Attributes:
        farm (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        cap (Union[None, int]): Terminals one cell of the farm holds, not the farm's total: a farm adds cells by itself
            as it fills, so it has no total of its own. Null where no cap is set
        used (int): Terminals on the whole farm now, not counting retired ones. It may be more than `cap` once the farm
            has more than one cell
    """

    farm: "Ref"
    cap: Union[None, int]
    used: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ref import Ref

        farm = self.farm.to_dict()

        cap: Union[None, int]
        cap = self.cap

        used = self.used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "farm": farm,
                "cap": cap,
                "used": used,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ref import Ref

        d = dict(src_dict)
        farm = Ref.from_dict(d.pop("farm"))

        def _parse_cap(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        cap = _parse_cap(d.pop("cap"))

        used = d.pop("used")

        usage_farms_item = cls(
            farm=farm,
            cap=cap,
            used=used,
        )

        usage_farms_item.additional_properties = d
        return usage_farms_item

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
