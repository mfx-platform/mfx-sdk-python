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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_stops_account_closed_by_magic_item import (
        RiskStopsAccountClosedByMagicItem,
    )


T = TypeVar("T", bound="RiskStopsAccount")


@_attrs_define
class RiskStopsAccount:
    """
    Attributes:
        account_id (UUID):
        refused (int): Entries a rule in force refused
        closed (int): Positions a rule's or a challenge's close_positions action closed, in whole or in part
        closed_by_magic (list['RiskStopsAccountClosedByMagicItem']): closed per magic number, magic number order; 0 is a
            position no expert advisor opened
        closed_unattributed (int): Closes listed before magic numbers were recorded; closed is closed_by_magic's sum
            plus this
    """

    account_id: UUID
    refused: int
    closed: int
    closed_by_magic: list["RiskStopsAccountClosedByMagicItem"]
    closed_unattributed: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_stops_account_closed_by_magic_item import (
            RiskStopsAccountClosedByMagicItem,
        )

        account_id = str(self.account_id)

        refused = self.refused

        closed = self.closed

        closed_by_magic = []
        for closed_by_magic_item_data in self.closed_by_magic:
            closed_by_magic_item = closed_by_magic_item_data.to_dict()
            closed_by_magic.append(closed_by_magic_item)

        closed_unattributed = self.closed_unattributed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "refused": refused,
                "closed": closed,
                "closed_by_magic": closed_by_magic,
                "closed_unattributed": closed_unattributed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_stops_account_closed_by_magic_item import (
            RiskStopsAccountClosedByMagicItem,
        )

        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        refused = d.pop("refused")

        closed = d.pop("closed")

        closed_by_magic = []
        _closed_by_magic = d.pop("closed_by_magic")
        for closed_by_magic_item_data in _closed_by_magic:
            closed_by_magic_item = RiskStopsAccountClosedByMagicItem.from_dict(
                closed_by_magic_item_data
            )

            closed_by_magic.append(closed_by_magic_item)

        closed_unattributed = d.pop("closed_unattributed")

        risk_stops_account = cls(
            account_id=account_id,
            refused=refused,
            closed=closed,
            closed_by_magic=closed_by_magic,
            closed_unattributed=closed_unattributed,
        )

        risk_stops_account.additional_properties = d
        return risk_stops_account

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
