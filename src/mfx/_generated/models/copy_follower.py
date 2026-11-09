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

from ..models.copy_follower_state import CopyFollowerState
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_bounds import CopyBounds
    from ..models.copy_follower_symbol_map import CopyFollowerSymbolMap
    from ..models.copy_options import CopyOptions
    from ..models.copy_risk_limits import CopyRiskLimits
    from ..models.copy_scaling import CopyScaling
    from ..models.copy_stopout import CopyStopout


T = TypeVar("T", bound="CopyFollower")


@_attrs_define
class CopyFollower:
    """
    Attributes:
        id (UUID):
        account_id (UUID):
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        leader_id (UUID):
        scaling (CopyScaling): The mode and the figure it needs: multiplier for balance_ratio, equity_ratio and
            fixed_multiplier (1 when absent for the ratios); volume for fixed_volume; risk_pct for fixed_risk. A missing
            figure the mode needs is 422 `validation_error`.
        bounds (CopyBounds): The follower's own limits on one copy, in its venue's unit; the broker's apply as well, and
            the tighter wins
        symbol_map (CopyFollowerSymbolMap):
        options (CopyOptions):
        risk_limits (CopyRiskLimits): The follower's copy limits, as a percentage of `basis`, in the follower account's
            currency. Reaching one stops the follower out; with close_on_stopout its copied volume of this leader is closed,
            never the account's own positions.
        close_on_stopout (bool):
        group_id (Union[None, UUID]):
        mandate_version (int): The mandate's version; every change is a new one
        state (CopyFollowerState): copying: receives the leader's deals. paused: by you, its entries are not copied,
            closes of what it copied still are. stopped_out: a copy limit was reached; it copies nothing new until the
            period ends or the stop-out is reset. unfollowed: final.
        stopouts (list['CopyStopout']): Its active stop-outs; empty when none
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: UUID
    account_id: UUID
    venue: Venue
    leader_id: UUID
    scaling: "CopyScaling"
    bounds: "CopyBounds"
    symbol_map: "CopyFollowerSymbolMap"
    options: "CopyOptions"
    risk_limits: "CopyRiskLimits"
    close_on_stopout: bool
    group_id: Union[None, UUID]
    mandate_version: int
    state: CopyFollowerState
    stopouts: list["CopyStopout"]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_follower_symbol_map import CopyFollowerSymbolMap
        from ..models.copy_options import CopyOptions
        from ..models.copy_risk_limits import CopyRiskLimits
        from ..models.copy_scaling import CopyScaling
        from ..models.copy_stopout import CopyStopout

        id = str(self.id)

        account_id = str(self.account_id)

        venue = self.venue.value

        leader_id = str(self.leader_id)

        scaling = self.scaling.to_dict()

        bounds = self.bounds.to_dict()

        symbol_map = self.symbol_map.to_dict()

        options = self.options.to_dict()

        risk_limits = self.risk_limits.to_dict()

        close_on_stopout = self.close_on_stopout

        group_id: Union[None, str]
        if isinstance(self.group_id, UUID):
            group_id = str(self.group_id)
        else:
            group_id = self.group_id

        mandate_version = self.mandate_version

        state = self.state.value

        stopouts = []
        for stopouts_item_data in self.stopouts:
            stopouts_item = stopouts_item_data.to_dict()
            stopouts.append(stopouts_item)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "account_id": account_id,
                "venue": venue,
                "leader_id": leader_id,
                "scaling": scaling,
                "bounds": bounds,
                "symbol_map": symbol_map,
                "options": options,
                "risk_limits": risk_limits,
                "close_on_stopout": close_on_stopout,
                "group_id": group_id,
                "mandate_version": mandate_version,
                "state": state,
                "stopouts": stopouts,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_follower_symbol_map import CopyFollowerSymbolMap
        from ..models.copy_options import CopyOptions
        from ..models.copy_risk_limits import CopyRiskLimits
        from ..models.copy_scaling import CopyScaling
        from ..models.copy_stopout import CopyStopout

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        leader_id = UUID(d.pop("leader_id"))

        scaling = CopyScaling.from_dict(d.pop("scaling"))

        bounds = CopyBounds.from_dict(d.pop("bounds"))

        symbol_map = CopyFollowerSymbolMap.from_dict(d.pop("symbol_map"))

        options = CopyOptions.from_dict(d.pop("options"))

        risk_limits = CopyRiskLimits.from_dict(d.pop("risk_limits"))

        close_on_stopout = d.pop("close_on_stopout")

        def _parse_group_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                group_id_type_0 = UUID(data)

                return group_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        group_id = _parse_group_id(d.pop("group_id"))

        mandate_version = d.pop("mandate_version")

        state = CopyFollowerState(d.pop("state"))

        stopouts = []
        _stopouts = d.pop("stopouts")
        for stopouts_item_data in _stopouts:
            stopouts_item = CopyStopout.from_dict(stopouts_item_data)

            stopouts.append(stopouts_item)

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        copy_follower = cls(
            id=id,
            account_id=account_id,
            venue=venue,
            leader_id=leader_id,
            scaling=scaling,
            bounds=bounds,
            symbol_map=symbol_map,
            options=options,
            risk_limits=risk_limits,
            close_on_stopout=close_on_stopout,
            group_id=group_id,
            mandate_version=mandate_version,
            state=state,
            stopouts=stopouts,
            created_at=created_at,
            updated_at=updated_at,
        )

        copy_follower.additional_properties = d
        return copy_follower

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
