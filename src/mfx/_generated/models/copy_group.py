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

from ..models.copy_group_state import CopyGroupState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_group_exposure import CopyGroupExposure
    from ..models.copy_group_template import CopyGroupTemplate


T = TypeVar("T", bound="CopyGroup")


@_attrs_define
class CopyGroup:
    """
    Attributes:
        id (UUID):
        name (str):
        template (CopyGroupTemplate): What a follower created into the group starts from, for every field it leaves out
        gross_exposure_cap (Union[None, str]): In US dollars; null is no cap
        placement_policy (Union[None, str]): Deprecated: stored and returned; placement never reads it. Each follower is
            placed by its own venue (an MT5 terminal near its leader's cell, a cTrader account by the connector's pool),
            never by its group
        state (CopyGroupState):
        followers_live (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        exposure (Union['CopyGroupExposure', None, Unset]): Gross exposure held against the cap, in US dollars
        out_of_step (Union[None, Unset, int]): Its live members whose newest drift is above 0; null where it was not
            read
    """

    id: UUID
    name: str
    template: "CopyGroupTemplate"
    gross_exposure_cap: Union[None, str]
    placement_policy: Union[None, str]
    state: CopyGroupState
    followers_live: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    exposure: Union["CopyGroupExposure", None, Unset] = UNSET
    out_of_step: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_exposure import CopyGroupExposure
        from ..models.copy_group_template import CopyGroupTemplate

        id = str(self.id)

        name = self.name

        template = self.template.to_dict()

        gross_exposure_cap: Union[None, str]
        gross_exposure_cap = self.gross_exposure_cap

        placement_policy: Union[None, str]
        placement_policy = self.placement_policy

        state = self.state.value

        followers_live = self.followers_live

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        exposure: Union[None, Unset, dict[str, Any]]
        if isinstance(self.exposure, Unset):
            exposure = UNSET
        elif isinstance(self.exposure, CopyGroupExposure):
            exposure = self.exposure.to_dict()
        else:
            exposure = self.exposure

        out_of_step: Union[None, Unset, int]
        if isinstance(self.out_of_step, Unset):
            out_of_step = UNSET
        else:
            out_of_step = self.out_of_step

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "template": template,
                "gross_exposure_cap": gross_exposure_cap,
                "placement_policy": placement_policy,
                "state": state,
                "followers_live": followers_live,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if exposure is not UNSET:
            field_dict["exposure"] = exposure
        if out_of_step is not UNSET:
            field_dict["out_of_step"] = out_of_step

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_exposure import CopyGroupExposure
        from ..models.copy_group_template import CopyGroupTemplate

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        template = CopyGroupTemplate.from_dict(d.pop("template"))

        def _parse_gross_exposure_cap(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        gross_exposure_cap = _parse_gross_exposure_cap(d.pop("gross_exposure_cap"))

        def _parse_placement_policy(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        placement_policy = _parse_placement_policy(d.pop("placement_policy"))

        state = CopyGroupState._read(d.pop("state"))

        followers_live = d.pop("followers_live")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_exposure(data: object) -> Union["CopyGroupExposure", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                exposure_type_0 = CopyGroupExposure.from_dict(data)

                return exposure_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CopyGroupExposure", None, Unset], data)

        exposure = _parse_exposure(d.pop("exposure", UNSET))

        def _parse_out_of_step(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        out_of_step = _parse_out_of_step(d.pop("out_of_step", UNSET))

        copy_group = cls(
            id=id,
            name=name,
            template=template,
            gross_exposure_cap=gross_exposure_cap,
            placement_policy=placement_policy,
            state=state,
            followers_live=followers_live,
            created_at=created_at,
            updated_at=updated_at,
            exposure=exposure,
            out_of_step=out_of_step,
        )

        copy_group.additional_properties = d
        return copy_group

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
