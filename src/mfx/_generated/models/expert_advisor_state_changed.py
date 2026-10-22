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

from ..models.ea_colour import EaColour
from ..models.expert_advisor_state_changed_state import ExpertAdvisorStateChangedState
from ..models.expert_advisor_state_changed_uploaded_by_operator import (
    ExpertAdvisorStateChangedUploadedByOperator,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpertAdvisorStateChanged")


@_attrs_define
class ExpertAdvisorStateChanged:
    """`data` of an `expert_advisor.state_changed` message on the `events` channel: sent once when a version of the
    tenant's EA takes a new state the platform gave it: its verdict (`approved`, `held` or `rejected`), and `revoked`
    when an operator takes it off every terminal. The report is read with `GET /expert-advisors/{id}/report` and an
    operator's reason on the version (`decision`); the event carries no finding and no source.

        Attributes:
            schema_version (str):
            expert_advisor_id (UUID):
            name (str):
            version (int): Counts the uploads under this name, from 1
            state (ExpertAdvisorStateChangedState):
            changed_at (datetime.datetime):
            verdict (Union[Unset, EaColour]): A verdict's colour. green: nothing found, or notes only. amber: needs a
                person. red: refused. grey: nothing could be judged yet. The verdict of a version is its worst finding under the
                policy version it was judged by.
            uploaded_by_operator (Union[Unset, ExpertAdvisorStateChangedUploadedByOperator]): Present, and true, on the
                uploaded message of a version the platform operator uploaded for you. Absent otherwise
    """

    schema_version: str
    expert_advisor_id: UUID
    name: str
    version: int
    state: ExpertAdvisorStateChangedState
    changed_at: datetime.datetime
    verdict: Union[Unset, EaColour] = UNSET
    uploaded_by_operator: Union[Unset, ExpertAdvisorStateChangedUploadedByOperator] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        expert_advisor_id = str(self.expert_advisor_id)

        name = self.name

        version = self.version

        state = self.state.value

        changed_at = self.changed_at.isoformat()

        verdict: Union[Unset, str] = UNSET
        if not isinstance(self.verdict, Unset):
            verdict = self.verdict.value

        uploaded_by_operator: Union[Unset, str] = UNSET
        if not isinstance(self.uploaded_by_operator, Unset):
            uploaded_by_operator = self.uploaded_by_operator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "expert_advisor_id": expert_advisor_id,
                "name": name,
                "version": version,
                "state": state,
                "changed_at": changed_at,
            }
        )
        if verdict is not UNSET:
            field_dict["verdict"] = verdict
        if uploaded_by_operator is not UNSET:
            field_dict["uploaded_by_operator"] = uploaded_by_operator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        expert_advisor_id = UUID(d.pop("expert_advisor_id"))

        name = d.pop("name")

        version = d.pop("version")

        state = ExpertAdvisorStateChangedState(d.pop("state"))

        changed_at = isoparse(d.pop("changed_at"))

        _verdict = d.pop("verdict", UNSET)
        verdict: Union[Unset, EaColour]
        if isinstance(_verdict, Unset):
            verdict = UNSET
        else:
            verdict = EaColour(_verdict)

        _uploaded_by_operator = d.pop("uploaded_by_operator", UNSET)
        uploaded_by_operator: Union[Unset, ExpertAdvisorStateChangedUploadedByOperator]
        if isinstance(_uploaded_by_operator, Unset):
            uploaded_by_operator = UNSET
        else:
            uploaded_by_operator = ExpertAdvisorStateChangedUploadedByOperator(
                _uploaded_by_operator
            )

        expert_advisor_state_changed = cls(
            schema_version=schema_version,
            expert_advisor_id=expert_advisor_id,
            name=name,
            version=version,
            state=state,
            changed_at=changed_at,
            verdict=verdict,
            uploaded_by_operator=uploaded_by_operator,
        )

        expert_advisor_state_changed.additional_properties = d
        return expert_advisor_state_changed

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
