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

from ..models.expert_advisor_attachment_changed_reason_type_1 import (
    ExpertAdvisorAttachmentChangedReasonType1,
)
from ..models.expert_advisor_attachment_changed_reason_type_2_type_1 import (
    ExpertAdvisorAttachmentChangedReasonType2Type1,
)
from ..models.expert_advisor_attachment_changed_reason_type_3_type_1 import (
    ExpertAdvisorAttachmentChangedReasonType3Type1,
)
from ..models.expert_advisor_attachment_changed_state import (
    ExpertAdvisorAttachmentChangedState,
)
from ..models.expert_advisor_attachment_changed_was_type_1 import (
    ExpertAdvisorAttachmentChangedWasType1,
)
from ..models.expert_advisor_attachment_changed_was_type_2_type_1 import (
    ExpertAdvisorAttachmentChangedWasType2Type1,
)
from ..models.expert_advisor_attachment_changed_was_type_3_type_1 import (
    ExpertAdvisorAttachmentChangedWasType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpertAdvisorAttachmentChanged")


@_attrs_define
class ExpertAdvisorAttachmentChanged:
    """`data` of an `expert_advisor.attachment_changed` message on the `events` channel: sent once each time an EA on one
    of the tenant's terminals takes a new state: its trial started (`trial`), ended green on a real-money account and
    waits for the representative (`awaiting_confirmation`), went live (`running`), or ended (`detached`). `reason` says
    why when the platform ended it; it is null for the tenant's own detach. The trial's figures and verdict are read on
    the version (`TenantExpertAdvisor.terminals[].trial`).

        Attributes:
            schema_version (str):
            terminal_id (UUID):
            expert_advisor_id (UUID):
            attachment_id (UUID): One attach of a version to a terminal; a new attach is a new id
            state (ExpertAdvisorAttachmentChangedState):
            was (Union[ExpertAdvisorAttachmentChangedWasType1, ExpertAdvisorAttachmentChangedWasType2Type1,
                ExpertAdvisorAttachmentChangedWasType3Type1, None]): The state before; null when the attachment was made
            changed_at (datetime.datetime):
            reason (Union[ExpertAdvisorAttachmentChangedReasonType1, ExpertAdvisorAttachmentChangedReasonType2Type1,
                ExpertAdvisorAttachmentChangedReasonType3Type1, None, Unset]): Why the platform ended it; null for the tenant's
                own detach and for every state but detached
    """

    schema_version: str
    terminal_id: UUID
    expert_advisor_id: UUID
    attachment_id: UUID
    state: ExpertAdvisorAttachmentChangedState
    was: Union[
        ExpertAdvisorAttachmentChangedWasType1,
        ExpertAdvisorAttachmentChangedWasType2Type1,
        ExpertAdvisorAttachmentChangedWasType3Type1,
        None,
    ]
    changed_at: datetime.datetime
    reason: Union[
        ExpertAdvisorAttachmentChangedReasonType1,
        ExpertAdvisorAttachmentChangedReasonType2Type1,
        ExpertAdvisorAttachmentChangedReasonType3Type1,
        None,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        expert_advisor_id = str(self.expert_advisor_id)

        attachment_id = str(self.attachment_id)

        state = self.state.value

        was: Union[None, str]
        if isinstance(self.was, ExpertAdvisorAttachmentChangedWasType1):
            was = self.was.value
        elif isinstance(self.was, ExpertAdvisorAttachmentChangedWasType2Type1):
            was = self.was.value
        elif isinstance(self.was, ExpertAdvisorAttachmentChangedWasType3Type1):
            was = self.was.value
        else:
            was = self.was

        changed_at = self.changed_at.isoformat()

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        elif isinstance(self.reason, ExpertAdvisorAttachmentChangedReasonType1):
            reason = self.reason.value
        elif isinstance(self.reason, ExpertAdvisorAttachmentChangedReasonType2Type1):
            reason = self.reason.value
        elif isinstance(self.reason, ExpertAdvisorAttachmentChangedReasonType3Type1):
            reason = self.reason.value
        else:
            reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "expert_advisor_id": expert_advisor_id,
                "attachment_id": attachment_id,
                "state": state,
                "was": was,
                "changed_at": changed_at,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        expert_advisor_id = UUID(d.pop("expert_advisor_id"))

        attachment_id = UUID(d.pop("attachment_id"))

        state = ExpertAdvisorAttachmentChangedState(d.pop("state"))

        def _parse_was(
            data: object,
        ) -> Union[
            ExpertAdvisorAttachmentChangedWasType1,
            ExpertAdvisorAttachmentChangedWasType2Type1,
            ExpertAdvisorAttachmentChangedWasType3Type1,
            None,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                was_type_1 = ExpertAdvisorAttachmentChangedWasType1(data)

                return was_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                was_type_2_type_1 = ExpertAdvisorAttachmentChangedWasType2Type1(data)

                return was_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                was_type_3_type_1 = ExpertAdvisorAttachmentChangedWasType3Type1(data)

                return was_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    ExpertAdvisorAttachmentChangedWasType1,
                    ExpertAdvisorAttachmentChangedWasType2Type1,
                    ExpertAdvisorAttachmentChangedWasType3Type1,
                    None,
                ],
                data,
            )

        was = _parse_was(d.pop("was"))

        changed_at = isoparse(d.pop("changed_at"))

        def _parse_reason(
            data: object,
        ) -> Union[
            ExpertAdvisorAttachmentChangedReasonType1,
            ExpertAdvisorAttachmentChangedReasonType2Type1,
            ExpertAdvisorAttachmentChangedReasonType3Type1,
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = ExpertAdvisorAttachmentChangedReasonType1(data)

                return reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_2_type_1 = ExpertAdvisorAttachmentChangedReasonType2Type1(data)

                return reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_3_type_1 = ExpertAdvisorAttachmentChangedReasonType3Type1(data)

                return reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    ExpertAdvisorAttachmentChangedReasonType1,
                    ExpertAdvisorAttachmentChangedReasonType2Type1,
                    ExpertAdvisorAttachmentChangedReasonType3Type1,
                    None,
                    Unset,
                ],
                data,
            )

        reason = _parse_reason(d.pop("reason", UNSET))

        expert_advisor_attachment_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            expert_advisor_id=expert_advisor_id,
            attachment_id=attachment_id,
            state=state,
            was=was,
            changed_at=changed_at,
            reason=reason,
        )

        expert_advisor_attachment_changed.additional_properties = d
        return expert_advisor_attachment_changed

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
