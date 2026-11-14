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

from ..models.risk_close_scope_scope import RiskCloseScopeScope
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_close_scope_positions_item import RiskCloseScopePositionsItem


T = TypeVar("T", bound="RiskCloseScope")


@_attrs_define
class RiskCloseScope:
    """The positions close_positions would close now on the account under one scope, from its last read. Nothing is sent

    Attributes:
        account_id (UUID):
        scope (RiskCloseScopeScope):
        read_at (Union[None, datetime.datetime]): The account read the positions come from; null when there is none
        count (int):
        positions (list['RiskCloseScopePositionsItem']):
    """

    account_id: UUID
    scope: RiskCloseScopeScope
    read_at: Union[None, datetime.datetime]
    count: int
    positions: list["RiskCloseScopePositionsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_close_scope_positions_item import RiskCloseScopePositionsItem

        account_id = str(self.account_id)

        scope = self.scope.value

        read_at: Union[None, str]
        if isinstance(self.read_at, datetime.datetime):
            read_at = self.read_at.isoformat()
        else:
            read_at = self.read_at

        count = self.count

        positions = []
        for positions_item_data in self.positions:
            positions_item = positions_item_data.to_dict()
            positions.append(positions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_id": account_id,
                "scope": scope,
                "read_at": read_at,
                "count": count,
                "positions": positions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_close_scope_positions_item import RiskCloseScopePositionsItem

        d = dict(src_dict)
        account_id = UUID(d.pop("account_id"))

        scope = RiskCloseScopeScope(d.pop("scope"))

        def _parse_read_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                read_at_type_0 = isoparse(data)

                return read_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        read_at = _parse_read_at(d.pop("read_at"))

        count = d.pop("count")

        positions = []
        _positions = d.pop("positions")
        for positions_item_data in _positions:
            positions_item = RiskCloseScopePositionsItem.from_dict(positions_item_data)

            positions.append(positions_item)

        risk_close_scope = cls(
            account_id=account_id,
            scope=scope,
            read_at=read_at,
            count=count,
            positions=positions,
        )

        risk_close_scope.additional_properties = d
        return risk_close_scope

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
