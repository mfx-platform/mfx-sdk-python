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

from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_copied_as import CopyCopiedAs
    from ..models.copy_leader_deal import CopyLeaderDeal
    from ..models.copy_stages import CopyStages


T = TypeVar("T", bound="CopyCopied")


@_attrs_define
class CopyCopied:
    """`data` of `copy.copied`: one follower's copy filled

    Attributes:
        schema_version (str):
        signal_id (UUID):
        leader_id (UUID):
        follower_id (UUID):
        account_id (UUID): The follower account
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        command_id (UUID):
        deal (CopyLeaderDeal): The leader's deal a copy came from, in venue-neutral terms
        as_ (CopyCopiedAs): What the copy became on the follower account
        latency_ms (Union[None, float]): MFX Hub's part (mfx_ms of the log row)
        slippage (Union[None, str]):
        stages (CopyStages): Milliseconds each stage took, each measured on its own machine. A stage that did not happen
            for this copy is absent. broker_ms is the venue's time and is not MFX Hub's.
        at (datetime.datetime):
    """

    schema_version: str
    signal_id: UUID
    leader_id: UUID
    follower_id: UUID
    account_id: UUID
    venue: Venue
    command_id: UUID
    deal: "CopyLeaderDeal"
    as_: "CopyCopiedAs"
    latency_ms: Union[None, float]
    slippage: Union[None, str]
    stages: "CopyStages"
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_copied_as import CopyCopiedAs
        from ..models.copy_leader_deal import CopyLeaderDeal
        from ..models.copy_stages import CopyStages

        schema_version = self.schema_version

        signal_id = str(self.signal_id)

        leader_id = str(self.leader_id)

        follower_id = str(self.follower_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        command_id = str(self.command_id)

        deal = self.deal.to_dict()

        as_ = self.as_.to_dict()

        latency_ms: Union[None, float]
        latency_ms = self.latency_ms

        slippage: Union[None, str]
        slippage = self.slippage

        stages = self.stages.to_dict()

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "signal_id": signal_id,
                "leader_id": leader_id,
                "follower_id": follower_id,
                "account_id": account_id,
                "venue": venue,
                "command_id": command_id,
                "deal": deal,
                "as": as_,
                "latency_ms": latency_ms,
                "slippage": slippage,
                "stages": stages,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_copied_as import CopyCopiedAs
        from ..models.copy_leader_deal import CopyLeaderDeal
        from ..models.copy_stages import CopyStages

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        signal_id = UUID(d.pop("signal_id"))

        leader_id = UUID(d.pop("leader_id"))

        follower_id = UUID(d.pop("follower_id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        command_id = UUID(d.pop("command_id"))

        deal = CopyLeaderDeal.from_dict(d.pop("deal"))

        as_ = CopyCopiedAs.from_dict(d.pop("as"))

        def _parse_latency_ms(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms"))

        def _parse_slippage(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        slippage = _parse_slippage(d.pop("slippage"))

        stages = CopyStages.from_dict(d.pop("stages"))

        at = isoparse(d.pop("at"))

        copy_copied = cls(
            schema_version=schema_version,
            signal_id=signal_id,
            leader_id=leader_id,
            follower_id=follower_id,
            account_id=account_id,
            venue=venue,
            command_id=command_id,
            deal=deal,
            as_=as_,
            latency_ms=latency_ms,
            slippage=slippage,
            stages=stages,
            at=at,
        )

        copy_copied.additional_properties = d
        return copy_copied

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
