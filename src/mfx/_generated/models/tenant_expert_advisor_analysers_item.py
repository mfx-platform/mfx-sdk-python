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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tenant_expert_advisor_analysers_item_analyser import (
    TenantExpertAdvisorAnalysersItemAnalyser,
)
from ..models.tenant_expert_advisor_analysers_item_state import (
    TenantExpertAdvisorAnalysersItemState,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantExpertAdvisorAnalysersItem")


@_attrs_define
class TenantExpertAdvisorAnalysersItem:
    """
    Attributes:
        analyser (TenantExpertAdvisorAnalysersItemAnalyser):
        state (TenantExpertAdvisorAnalysersItemState):
        finished_at (Union[None, datetime.datetime]):
        failure (Union[None, str]):
    """

    analyser: TenantExpertAdvisorAnalysersItemAnalyser
    state: TenantExpertAdvisorAnalysersItemState
    finished_at: Union[None, datetime.datetime]
    failure: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        analyser = self.analyser.value

        state = self.state.value

        finished_at: Union[None, str]
        if isinstance(self.finished_at, datetime.datetime):
            finished_at = self.finished_at.isoformat()
        else:
            finished_at = self.finished_at

        failure: Union[None, str]
        failure = self.failure

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "analyser": analyser,
                "state": state,
                "finished_at": finished_at,
                "failure": failure,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        analyser = TenantExpertAdvisorAnalysersItemAnalyser(d.pop("analyser"))

        state = TenantExpertAdvisorAnalysersItemState(d.pop("state"))

        def _parse_finished_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_at_type_0 = isoparse(data)

                return finished_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        finished_at = _parse_finished_at(d.pop("finished_at"))

        def _parse_failure(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        failure = _parse_failure(d.pop("failure"))

        tenant_expert_advisor_analysers_item = cls(
            analyser=analyser,
            state=state,
            finished_at=finished_at,
            failure=failure,
        )

        tenant_expert_advisor_analysers_item.additional_properties = d
        return tenant_expert_advisor_analysers_item

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
