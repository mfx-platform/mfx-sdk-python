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
from ..models.copy_follower_venue_state import CopyFollowerVenueState
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_bounds import CopyBounds
    from ..models.copy_close_summary import CopyCloseSummary
    from ..models.copy_follower_drift import CopyFollowerDrift
    from ..models.copy_follower_exposure import CopyFollowerExposure
    from ..models.copy_follower_symbol_map import CopyFollowerSymbolMap
    from ..models.copy_follower_today import CopyFollowerToday
    from ..models.copy_limits_use import CopyLimitsUse
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
        close (Union['CopyCloseSummary', None, Unset]): The newest requested close of this follower's copied positions,
            in brief; null when none was asked. GET /copy/closes/{id} has it whole
        exposure (Union['CopyFollowerExposure', None, Unset]): Its copied gross exposure and its share of its group's
            cap, in US dollars
        drift (Union['CopyFollowerDrift', None, Unset]): The newest drift a resync measured: the copied volume missing
            from the account, as a percentage of what the ledger expected, 0.00 when nothing was. A resync that could not
            read the account leaves the last. Null when never measured
        limits_use (Union['CopyLimitsUse', None, Unset]): Each copy limit's use as its copy host last reported it, in
            the account's currency. Null when the host has not reported it in the last 180 seconds, never zeros
        today (Union['CopyFollowerToday', None, Unset]): Its copies of the current UTC day; null where it was not read
        venue_state (Union[Unset, CopyFollowerVenueState]): Whether MFX Hub has braked this follower's account venue, as
            Copy Trading applies it. SUSPENDED: its mandate copies closes and stop changes only, whatever its own
            close_only, and a requested close still closes. DISABLED: nothing is copied and nothing is closed by the copy; a
            pending close waits, its give-up clock stopped, until the venue is enabled, and a follow, an update, a resume or
            a stop-out reset is refused 403 venue_suspended. An account whose venue row is retired or deleted reads
            DISABLED. Enabled again, its own settings are copied again
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
    close: Union["CopyCloseSummary", None, Unset] = UNSET
    exposure: Union["CopyFollowerExposure", None, Unset] = UNSET
    drift: Union["CopyFollowerDrift", None, Unset] = UNSET
    limits_use: Union["CopyLimitsUse", None, Unset] = UNSET
    today: Union["CopyFollowerToday", None, Unset] = UNSET
    venue_state: Union[Unset, CopyFollowerVenueState] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_close_summary import CopyCloseSummary
        from ..models.copy_follower_drift import CopyFollowerDrift
        from ..models.copy_follower_exposure import CopyFollowerExposure
        from ..models.copy_follower_symbol_map import CopyFollowerSymbolMap
        from ..models.copy_follower_today import CopyFollowerToday
        from ..models.copy_limits_use import CopyLimitsUse
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

        close: Union[None, Unset, dict[str, Any]]
        if isinstance(self.close, Unset):
            close = UNSET
        elif isinstance(self.close, CopyCloseSummary):
            close = self.close.to_dict()
        else:
            close = self.close

        exposure: Union[None, Unset, dict[str, Any]]
        if isinstance(self.exposure, Unset):
            exposure = UNSET
        elif isinstance(self.exposure, CopyFollowerExposure):
            exposure = self.exposure.to_dict()
        else:
            exposure = self.exposure

        drift: Union[None, Unset, dict[str, Any]]
        if isinstance(self.drift, Unset):
            drift = UNSET
        elif isinstance(self.drift, CopyFollowerDrift):
            drift = self.drift.to_dict()
        else:
            drift = self.drift

        limits_use: Union[None, Unset, dict[str, Any]]
        if isinstance(self.limits_use, Unset):
            limits_use = UNSET
        elif isinstance(self.limits_use, CopyLimitsUse):
            limits_use = self.limits_use.to_dict()
        else:
            limits_use = self.limits_use

        today: Union[None, Unset, dict[str, Any]]
        if isinstance(self.today, Unset):
            today = UNSET
        elif isinstance(self.today, CopyFollowerToday):
            today = self.today.to_dict()
        else:
            today = self.today

        venue_state: Union[Unset, str] = UNSET
        if not isinstance(self.venue_state, Unset):
            venue_state = self.venue_state.value

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
        if close is not UNSET:
            field_dict["close"] = close
        if exposure is not UNSET:
            field_dict["exposure"] = exposure
        if drift is not UNSET:
            field_dict["drift"] = drift
        if limits_use is not UNSET:
            field_dict["limits_use"] = limits_use
        if today is not UNSET:
            field_dict["today"] = today
        if venue_state is not UNSET:
            field_dict["venue_state"] = venue_state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_bounds import CopyBounds
        from ..models.copy_close_summary import CopyCloseSummary
        from ..models.copy_follower_drift import CopyFollowerDrift
        from ..models.copy_follower_exposure import CopyFollowerExposure
        from ..models.copy_follower_symbol_map import CopyFollowerSymbolMap
        from ..models.copy_follower_today import CopyFollowerToday
        from ..models.copy_limits_use import CopyLimitsUse
        from ..models.copy_options import CopyOptions
        from ..models.copy_risk_limits import CopyRiskLimits
        from ..models.copy_scaling import CopyScaling
        from ..models.copy_stopout import CopyStopout

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue._read(d.pop("venue"))

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

        state = CopyFollowerState._read(d.pop("state"))

        stopouts = []
        _stopouts = d.pop("stopouts")
        for stopouts_item_data in _stopouts:
            stopouts_item = CopyStopout.from_dict(stopouts_item_data)

            stopouts.append(stopouts_item)

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_close(data: object) -> Union["CopyCloseSummary", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                close_type_0 = CopyCloseSummary.from_dict(data)

                return close_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyCloseSummary", None, Unset], data)

        close = _parse_close(d.pop("close", UNSET))

        def _parse_exposure(data: object) -> Union["CopyFollowerExposure", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                exposure_type_0 = CopyFollowerExposure.from_dict(data)

                return exposure_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyFollowerExposure", None, Unset], data)

        exposure = _parse_exposure(d.pop("exposure", UNSET))

        def _parse_drift(data: object) -> Union["CopyFollowerDrift", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                drift_type_0 = CopyFollowerDrift.from_dict(data)

                return drift_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyFollowerDrift", None, Unset], data)

        drift = _parse_drift(d.pop("drift", UNSET))

        def _parse_limits_use(data: object) -> Union["CopyLimitsUse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                limits_use_type_0 = CopyLimitsUse.from_dict(data)

                return limits_use_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyLimitsUse", None, Unset], data)

        limits_use = _parse_limits_use(d.pop("limits_use", UNSET))

        def _parse_today(data: object) -> Union["CopyFollowerToday", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                today_type_0 = CopyFollowerToday.from_dict(data)

                return today_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyFollowerToday", None, Unset], data)

        today = _parse_today(d.pop("today", UNSET))

        _venue_state = d.pop("venue_state", UNSET)
        venue_state: Union[Unset, CopyFollowerVenueState]
        if isinstance(_venue_state, Unset):
            venue_state = UNSET
        else:
            venue_state = CopyFollowerVenueState._read(_venue_state)

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
            close=close,
            exposure=exposure,
            drift=drift,
            limits_use=limits_use,
            today=today,
            venue_state=venue_state,
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
