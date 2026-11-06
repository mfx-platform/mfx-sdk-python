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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_policy_version_changes_item import RiskPolicyVersionChangesItem
    from ..models.risk_reset import RiskReset
    from ..models.risk_rules import RiskRules


T = TypeVar("T", bound="RiskPolicyVersion")


@_attrs_define
class RiskPolicyVersion:
    """
    Attributes:
        policy_id (UUID):
        version (int):
        rules (RiskRules): Every rule is optional; a rule present is evaluated. Nothing has a default the platform chose
        reset (RiskReset):
        relaxes (bool): Against the version before it: a limit rose, an action was removed, or a window widened
        changes (list['RiskPolicyVersionChangesItem']):
        created_at (datetime.datetime):
        reason (Union[None, str]):
    """

    policy_id: UUID
    version: int
    rules: "RiskRules"
    reset: "RiskReset"
    relaxes: bool
    changes: list["RiskPolicyVersionChangesItem"]
    created_at: datetime.datetime
    reason: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_policy_version_changes_item import (
            RiskPolicyVersionChangesItem,
        )
        from ..models.risk_reset import RiskReset
        from ..models.risk_rules import RiskRules

        policy_id = str(self.policy_id)

        version = self.version

        rules = self.rules.to_dict()

        reset = self.reset.to_dict()

        relaxes = self.relaxes

        changes = []
        for changes_item_data in self.changes:
            changes_item = changes_item_data.to_dict()
            changes.append(changes_item)

        created_at = self.created_at.isoformat()

        reason: Union[None, str]
        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy_id": policy_id,
                "version": version,
                "rules": rules,
                "reset": reset,
                "relaxes": relaxes,
                "changes": changes,
                "created_at": created_at,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_policy_version_changes_item import (
            RiskPolicyVersionChangesItem,
        )
        from ..models.risk_reset import RiskReset
        from ..models.risk_rules import RiskRules

        d = dict(src_dict)
        policy_id = UUID(d.pop("policy_id"))

        version = d.pop("version")

        rules = RiskRules.from_dict(d.pop("rules"))

        reset = RiskReset.from_dict(d.pop("reset"))

        relaxes = d.pop("relaxes")

        changes = []
        _changes = d.pop("changes")
        for changes_item_data in _changes:
            changes_item = RiskPolicyVersionChangesItem.from_dict(changes_item_data)

            changes.append(changes_item)

        created_at = isoparse(d.pop("created_at"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        risk_policy_version = cls(
            policy_id=policy_id,
            version=version,
            rules=rules,
            reset=reset,
            relaxes=relaxes,
            changes=changes,
            created_at=created_at,
            reason=reason,
        )

        risk_policy_version.additional_properties = d
        return risk_policy_version

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
