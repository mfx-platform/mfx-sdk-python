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

from ..models.copy_limit_kind import CopyLimitKind
from ..models.copy_stopout_state import CopyStopoutState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_stopout_closed_item import CopyStopoutClosedItem
    from ..models.copy_stopout_reset_type_0 import CopyStopoutResetType0


T = TypeVar("T", bound="CopyStopout")


@_attrs_define
class CopyStopout:
    """
    Attributes:
        id (UUID):
        follower_id (UUID):
        limit (CopyLimitKind):
        used (str): A decimal as a string, never a JSON number
        period_start (datetime.datetime):
        period_end (Union[None, datetime.datetime]): Null for a lifetime limit
        closed (list['CopyStopoutClosedItem']): The copied volume it closed, when close_on_stopout was set
        state (CopyStopoutState): active: in force. reset: ended early by a person, with a reason. expired: its period
            ended
        reset (Union['CopyStopoutResetType0', None]): Who reset it, when and why; null unless reset
        created_at (datetime.datetime):
    """

    id: UUID
    follower_id: UUID
    limit: CopyLimitKind
    used: str
    period_start: datetime.datetime
    period_end: Union[None, datetime.datetime]
    closed: list["CopyStopoutClosedItem"]
    state: CopyStopoutState
    reset: Union["CopyStopoutResetType0", None]
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_stopout_closed_item import CopyStopoutClosedItem
        from ..models.copy_stopout_reset_type_0 import CopyStopoutResetType0

        id = str(self.id)

        follower_id = str(self.follower_id)

        limit = self.limit.value

        used = self.used

        period_start = self.period_start.isoformat()

        period_end: Union[None, str]
        if isinstance(self.period_end, datetime.datetime):
            period_end = self.period_end.isoformat()
        else:
            period_end = self.period_end

        closed = []
        for closed_item_data in self.closed:
            closed_item = closed_item_data.to_dict()
            closed.append(closed_item)

        state = self.state.value

        reset: Union[None, dict[str, Any]]
        if isinstance(self.reset, CopyStopoutResetType0):
            reset = self.reset.to_dict()
        else:
            reset = self.reset

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "follower_id": follower_id,
                "limit": limit,
                "used": used,
                "period_start": period_start,
                "period_end": period_end,
                "closed": closed,
                "state": state,
                "reset": reset,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_stopout_closed_item import CopyStopoutClosedItem
        from ..models.copy_stopout_reset_type_0 import CopyStopoutResetType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        follower_id = UUID(d.pop("follower_id"))

        limit = CopyLimitKind(d.pop("limit"))

        used = d.pop("used")

        period_start = isoparse(d.pop("period_start"))

        def _parse_period_end(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                period_end_type_0 = isoparse(data)

                return period_end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        period_end = _parse_period_end(d.pop("period_end"))

        closed = []
        _closed = d.pop("closed")
        for closed_item_data in _closed:
            closed_item = CopyStopoutClosedItem.from_dict(closed_item_data)

            closed.append(closed_item)

        state = CopyStopoutState(d.pop("state"))

        def _parse_reset(data: object) -> Union["CopyStopoutResetType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reset_type_0 = CopyStopoutResetType0.from_dict(data)

                return reset_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyStopoutResetType0", None], data)

        reset = _parse_reset(d.pop("reset"))

        created_at = isoparse(d.pop("created_at"))

        copy_stopout = cls(
            id=id,
            follower_id=follower_id,
            limit=limit,
            used=used,
            period_start=period_start,
            period_end=period_end,
            closed=closed,
            state=state,
            reset=reset,
            created_at=created_at,
        )

        copy_stopout.additional_properties = d
        return copy_stopout

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
