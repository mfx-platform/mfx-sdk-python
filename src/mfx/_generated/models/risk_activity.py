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

from ..models.risk_activity_kind import RiskActivityKind
from ..models.risk_outcome import RiskOutcome
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_activity_evidence import RiskActivityEvidence
    from ..models.risk_activity_items_item import RiskActivityItemsItem
    from ..models.risk_activity_policy_type_0 import RiskActivityPolicyType0


T = TypeVar("T", bound="RiskActivity")


@_attrs_define
class RiskActivity:
    """
    Attributes:
        id (UUID):
        at (datetime.datetime):
        terminal_id (Union[None, UUID]): null for a row about several accounts (a daily reset)
        kind (RiskActivityKind):
        rule (Union[None, str]):
        policy (Union['RiskActivityPolicyType0', None]):
        plan_id (Union[None, UUID]):
        challenge_id (Union[None, UUID]):
        summary (str): What happened, in words
        outcome (RiskOutcome):
        items (list['RiskActivityItemsItem']):
        evidence (RiskActivityEvidence): The inputs the decision read, with their times
        by (Union[None, str]): Who changed something: a key id, or operator; null for the platform
    """

    id: UUID
    at: datetime.datetime
    terminal_id: Union[None, UUID]
    kind: RiskActivityKind
    rule: Union[None, str]
    policy: Union["RiskActivityPolicyType0", None]
    plan_id: Union[None, UUID]
    challenge_id: Union[None, UUID]
    summary: str
    outcome: RiskOutcome
    items: list["RiskActivityItemsItem"]
    evidence: "RiskActivityEvidence"
    by: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_activity_evidence import RiskActivityEvidence
        from ..models.risk_activity_items_item import RiskActivityItemsItem
        from ..models.risk_activity_policy_type_0 import RiskActivityPolicyType0

        id = str(self.id)

        at = self.at.isoformat()

        terminal_id: Union[None, str]
        if isinstance(self.terminal_id, UUID):
            terminal_id = str(self.terminal_id)
        else:
            terminal_id = self.terminal_id

        kind = self.kind.value

        rule: Union[None, str]
        rule = self.rule

        policy: Union[None, dict[str, Any]]
        if isinstance(self.policy, RiskActivityPolicyType0):
            policy = self.policy.to_dict()
        else:
            policy = self.policy

        plan_id: Union[None, str]
        if isinstance(self.plan_id, UUID):
            plan_id = str(self.plan_id)
        else:
            plan_id = self.plan_id

        challenge_id: Union[None, str]
        if isinstance(self.challenge_id, UUID):
            challenge_id = str(self.challenge_id)
        else:
            challenge_id = self.challenge_id

        summary = self.summary

        outcome = self.outcome.value

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        evidence = self.evidence.to_dict()

        by: Union[None, str]
        by = self.by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "at": at,
                "terminal_id": terminal_id,
                "kind": kind,
                "rule": rule,
                "policy": policy,
                "plan_id": plan_id,
                "challenge_id": challenge_id,
                "summary": summary,
                "outcome": outcome,
                "items": items,
                "evidence": evidence,
                "by": by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_activity_evidence import RiskActivityEvidence
        from ..models.risk_activity_items_item import RiskActivityItemsItem
        from ..models.risk_activity_policy_type_0 import RiskActivityPolicyType0

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        at = isoparse(d.pop("at"))

        def _parse_terminal_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                terminal_id_type_0 = UUID(data)

                return terminal_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        terminal_id = _parse_terminal_id(d.pop("terminal_id"))

        kind = RiskActivityKind(d.pop("kind"))

        def _parse_rule(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rule = _parse_rule(d.pop("rule"))

        def _parse_policy(data: object) -> Union["RiskActivityPolicyType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                policy_type_0 = RiskActivityPolicyType0.from_dict(data)

                return policy_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RiskActivityPolicyType0", None], data)

        policy = _parse_policy(d.pop("policy"))

        def _parse_plan_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_id_type_0 = UUID(data)

                return plan_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        plan_id = _parse_plan_id(d.pop("plan_id"))

        def _parse_challenge_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                challenge_id_type_0 = UUID(data)

                return challenge_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        challenge_id = _parse_challenge_id(d.pop("challenge_id"))

        summary = d.pop("summary")

        outcome = RiskOutcome(d.pop("outcome"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = RiskActivityItemsItem.from_dict(items_item_data)

            items.append(items_item)

        evidence = RiskActivityEvidence.from_dict(d.pop("evidence"))

        def _parse_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        by = _parse_by(d.pop("by"))

        risk_activity = cls(
            id=id,
            at=at,
            terminal_id=terminal_id,
            kind=kind,
            rule=rule,
            policy=policy,
            plan_id=plan_id,
            challenge_id=challenge_id,
            summary=summary,
            outcome=outcome,
            items=items,
            evidence=evidence,
            by=by,
        )

        risk_activity.additional_properties = d
        return risk_activity

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
