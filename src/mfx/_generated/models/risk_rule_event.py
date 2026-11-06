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

from ..models.risk_action_kind import RiskActionKind
from ..models.risk_rule_event_cleared_by_type_1 import RiskRuleEventClearedByType1
from ..models.risk_rule_event_cleared_by_type_2_type_1 import (
    RiskRuleEventClearedByType2Type1,
)
from ..models.risk_rule_event_cleared_by_type_3_type_1 import (
    RiskRuleEventClearedByType3Type1,
)
from ..models.risk_rule_event_level import RiskRuleEventLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskRuleEvent")


@_attrs_define
class RiskRuleEvent:
    """`data` of `risk.rule_warning`, `risk.rule_breached` and `risk.rule_cleared`

    Attributes:
        schema_version (str):
        terminal_id (UUID):
        rule (str):
        policy_id (Union[None, UUID]):
        version (int):
        used (Union[None, str]):
        limit (Union[None, str]):
        level (RiskRuleEventLevel):
        actions (list[RiskActionKind]):
        at (datetime.datetime):
        challenge_id (Union[None, UUID, Unset]):
        cleared_by (Union[None, RiskRuleEventClearedByType1, RiskRuleEventClearedByType2Type1,
            RiskRuleEventClearedByType3Type1, Unset]):
    """

    schema_version: str
    terminal_id: UUID
    rule: str
    policy_id: Union[None, UUID]
    version: int
    used: Union[None, str]
    limit: Union[None, str]
    level: RiskRuleEventLevel
    actions: list[RiskActionKind]
    at: datetime.datetime
    challenge_id: Union[None, UUID, Unset] = UNSET
    cleared_by: Union[
        None,
        RiskRuleEventClearedByType1,
        RiskRuleEventClearedByType2Type1,
        RiskRuleEventClearedByType3Type1,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        rule = self.rule

        policy_id: Union[None, str]
        if isinstance(self.policy_id, UUID):
            policy_id = str(self.policy_id)
        else:
            policy_id = self.policy_id

        version = self.version

        used: Union[None, str]
        used = self.used

        limit: Union[None, str]
        limit = self.limit

        level = self.level.value

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.value
            actions.append(actions_item)

        at = self.at.isoformat()

        challenge_id: Union[None, Unset, str]
        if isinstance(self.challenge_id, Unset):
            challenge_id = UNSET
        elif isinstance(self.challenge_id, UUID):
            challenge_id = str(self.challenge_id)
        else:
            challenge_id = self.challenge_id

        cleared_by: Union[None, Unset, str]
        if isinstance(self.cleared_by, Unset):
            cleared_by = UNSET
        elif isinstance(self.cleared_by, RiskRuleEventClearedByType1):
            cleared_by = self.cleared_by.value
        elif isinstance(self.cleared_by, RiskRuleEventClearedByType2Type1):
            cleared_by = self.cleared_by.value
        elif isinstance(self.cleared_by, RiskRuleEventClearedByType3Type1):
            cleared_by = self.cleared_by.value
        else:
            cleared_by = self.cleared_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "rule": rule,
                "policy_id": policy_id,
                "version": version,
                "used": used,
                "limit": limit,
                "level": level,
                "actions": actions,
                "at": at,
            }
        )
        if challenge_id is not UNSET:
            field_dict["challenge_id"] = challenge_id
        if cleared_by is not UNSET:
            field_dict["cleared_by"] = cleared_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        rule = d.pop("rule")

        def _parse_policy_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_id_type_0 = UUID(data)

                return policy_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        policy_id = _parse_policy_id(d.pop("policy_id"))

        version = d.pop("version")

        def _parse_used(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        used = _parse_used(d.pop("used"))

        def _parse_limit(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit = _parse_limit(d.pop("limit"))

        level = RiskRuleEventLevel(d.pop("level"))

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = RiskActionKind(actions_item_data)

            actions.append(actions_item)

        at = isoparse(d.pop("at"))

        def _parse_challenge_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                challenge_id_type_0 = UUID(data)

                return challenge_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        challenge_id = _parse_challenge_id(d.pop("challenge_id", UNSET))

        def _parse_cleared_by(
            data: object,
        ) -> Union[
            None,
            RiskRuleEventClearedByType1,
            RiskRuleEventClearedByType2Type1,
            RiskRuleEventClearedByType3Type1,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cleared_by_type_1 = RiskRuleEventClearedByType1(data)

                return cleared_by_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cleared_by_type_2_type_1 = RiskRuleEventClearedByType2Type1(data)

                return cleared_by_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cleared_by_type_3_type_1 = RiskRuleEventClearedByType3Type1(data)

                return cleared_by_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    RiskRuleEventClearedByType1,
                    RiskRuleEventClearedByType2Type1,
                    RiskRuleEventClearedByType3Type1,
                    Unset,
                ],
                data,
            )

        cleared_by = _parse_cleared_by(d.pop("cleared_by", UNSET))

        risk_rule_event = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            rule=rule,
            policy_id=policy_id,
            version=version,
            used=used,
            limit=limit,
            level=level,
            actions=actions,
            at=at,
            challenge_id=challenge_id,
            cleared_by=cleared_by,
        )

        risk_rule_event.additional_properties = d
        return risk_rule_event

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
