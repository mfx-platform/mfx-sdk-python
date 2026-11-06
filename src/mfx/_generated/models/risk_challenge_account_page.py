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
    from ..models.risk_challenge_account import RiskChallengeAccount


T = TypeVar("T", bound="RiskChallengeAccountPage")


@_attrs_define
class RiskChallengeAccountPage:
    """
    Attributes:
        items (list['RiskChallengeAccount']):
        next_cursor (Union[None, str]):
        returned (Union[Unset, int]):
    """

    items: list["RiskChallengeAccount"]
    next_cursor: Union[None, str]
    returned: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_challenge_account import RiskChallengeAccount

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_cursor: Union[None, str]
        next_cursor = self.next_cursor

        returned = self.returned

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "next_cursor": next_cursor,
            }
        )
        if returned is not UNSET:
            field_dict["returned"] = returned

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_challenge_account import RiskChallengeAccount

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RiskChallengeAccount.from_dict(items_item_data)

            items.append(items_item)

        def _parse_next_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        returned = d.pop("returned", UNSET)

        risk_challenge_account_page = cls(
            items=items,
            next_cursor=next_cursor,
            returned=returned,
        )

        risk_challenge_account_page.additional_properties = d
        return risk_challenge_account_page

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
