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

from ..models.risk_challenge_state import RiskChallengeState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_challenge_counts import RiskChallengeCounts
    from ..models.risk_challenge_rules import RiskChallengeRules


T = TypeVar("T", bound="RiskChallenge")


@_attrs_define
class RiskChallenge:
    """
    Attributes:
        id (UUID):
        name (str):
        state (RiskChallengeState):
        version (int):
        rules (RiskChallengeRules):
        counts (RiskChallengeCounts):
        created_at (datetime.datetime):
        archived_at (Union[None, Unset, datetime.datetime]): When it was archived; null while active
    """

    id: UUID
    name: str
    state: RiskChallengeState
    version: int
    rules: "RiskChallengeRules"
    counts: "RiskChallengeCounts"
    created_at: datetime.datetime
    archived_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_challenge_counts import RiskChallengeCounts
        from ..models.risk_challenge_rules import RiskChallengeRules

        id = str(self.id)

        name = self.name

        state = self.state.value

        version = self.version

        rules = self.rules.to_dict()

        counts = self.counts.to_dict()

        created_at = self.created_at.isoformat()

        archived_at: Union[None, Unset, str]
        if isinstance(self.archived_at, Unset):
            archived_at = UNSET
        elif isinstance(self.archived_at, datetime.datetime):
            archived_at = self.archived_at.isoformat()
        else:
            archived_at = self.archived_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "state": state,
                "version": version,
                "rules": rules,
                "counts": counts,
                "created_at": created_at,
            }
        )
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_challenge_counts import RiskChallengeCounts
        from ..models.risk_challenge_rules import RiskChallengeRules

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        state = RiskChallengeState._read(d.pop("state"))

        version = d.pop("version")

        rules = RiskChallengeRules.from_dict(d.pop("rules"))

        counts = RiskChallengeCounts.from_dict(d.pop("counts"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_archived_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                archived_at_type_0 = isoparse(data)

                return archived_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        archived_at = _parse_archived_at(d.pop("archived_at", UNSET))

        risk_challenge = cls(
            id=id,
            name=name,
            state=state,
            version=version,
            rules=rules,
            counts=counts,
            created_at=created_at,
            archived_at=archived_at,
        )

        risk_challenge.additional_properties = d
        return risk_challenge

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
