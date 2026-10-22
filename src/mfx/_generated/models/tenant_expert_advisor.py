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
from ..models.tenant_expert_advisor_state import TenantExpertAdvisorState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_trial_count import EaTrialCount
    from ..models.tenant_expert_advisor_analysers_item import (
        TenantExpertAdvisorAnalysersItem,
    )
    from ..models.tenant_expert_advisor_decision_type_0 import (
        TenantExpertAdvisorDecisionType0,
    )
    from ..models.tenant_expert_advisor_findings import TenantExpertAdvisorFindings
    from ..models.tenant_expert_advisor_last_trial_type_0 import (
        TenantExpertAdvisorLastTrialType0,
    )
    from ..models.tenant_expert_advisor_terminals_item import (
        TenantExpertAdvisorTerminalsItem,
    )


T = TypeVar("T", bound="TenantExpertAdvisor")


@_attrs_define
class TenantExpertAdvisor:
    """One version of the tenant's expert advisor: where it stands, its verdict, and where it runs. Never the source.

    Attributes:
        id (UUID):
        name (str):
        version (int): Counts the uploads under this name, from 1
        state (TenantExpertAdvisorState): uploaded and analysing: being checked. held: a finding needs a person, and one
            is looking. approved: it may be attached to a terminal. rejected: refused, and the report says why. withdrawn:
            the tenant deleted it. revoked: an operator took it off every terminal
        verdict (Union[EaColour, None]): Null until it is judged
        findings (TenantExpertAdvisorFindings): How many findings of each colour, under the policy version it was judged
            by. All zero until it is judged
        policy_version (Union[None, int]): The policy version it was judged by; null until it is judged
        analysers (list['TenantExpertAdvisorAnalysersItem']): Each check and where it stands. One that could not run
            does not approve the version: it holds it for a person, and `failure` says which check and why, in plain words
        source_sha256 (str): SHA-256 of the bundle as it was uploaded: the version's identity
        build_sha256 (Union[None, str]): SHA-256 of the file the platform built from it; null until it is built
        size_bytes (int): The files of the bundle together
        file_count (int):
        terminals (list['TenantExpertAdvisorTerminalsItem']): The tenant's terminals this version is attached to now;
            empty while it is on none
        decision (Union['TenantExpertAdvisorDecisionType0', None]): The last thing a person at the platform decided on
            this version, with the reason written for you; null where the checks decided by themselves. `revoke`: it was
            taken off every terminal and can be attached to none again
        source_kept_until (Union[None, datetime.datetime]): A rejected or withdrawn version: when its source is deleted.
            Null while it is kept without an end
        source_deleted_at (Union[None, datetime.datetime]): When its source was deleted: past its keeping time, or at
            once where a broker login or a private key was found in it. Null while it is kept. The report stays
        created_at (datetime.datetime):
        trials (Union[Unset, EaTrialCount]): How this version's trials went, shown beside its colour: a trial colours
            the terminal's attachment, not the version, so the version says how many of its terminals' trials failed out of
            those judged. Every attachment of the version counts, on a terminal now or ended. Absent from older answers
        uploaded_by_operator (Union[Unset, bool]): true where the platform operator uploaded it for you rather than one
            of your keys. Absent from older answers
        last_trial (Union['TenantExpertAdvisorLastTrialType0', None, Unset]): The newest trial of this version on any of
            your terminals, running or ended, kept after the attachment has left the terminal so a failed trial can still be
            read: its figures, its verdict and, in the report (`EaReport.trial`), the rule each failed figure crossed. Null
            where it has never been on trial, and absent from older answers
    """

    id: UUID
    name: str
    version: int
    state: TenantExpertAdvisorState
    verdict: Union[EaColour, None]
    findings: "TenantExpertAdvisorFindings"
    policy_version: Union[None, int]
    analysers: list["TenantExpertAdvisorAnalysersItem"]
    source_sha256: str
    build_sha256: Union[None, str]
    size_bytes: int
    file_count: int
    terminals: list["TenantExpertAdvisorTerminalsItem"]
    decision: Union["TenantExpertAdvisorDecisionType0", None]
    source_kept_until: Union[None, datetime.datetime]
    source_deleted_at: Union[None, datetime.datetime]
    created_at: datetime.datetime
    trials: Union[Unset, "EaTrialCount"] = UNSET
    uploaded_by_operator: Union[Unset, bool] = UNSET
    last_trial: Union["TenantExpertAdvisorLastTrialType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_trial_count import EaTrialCount
        from ..models.tenant_expert_advisor_analysers_item import (
            TenantExpertAdvisorAnalysersItem,
        )
        from ..models.tenant_expert_advisor_decision_type_0 import (
            TenantExpertAdvisorDecisionType0,
        )
        from ..models.tenant_expert_advisor_findings import TenantExpertAdvisorFindings
        from ..models.tenant_expert_advisor_last_trial_type_0 import (
            TenantExpertAdvisorLastTrialType0,
        )
        from ..models.tenant_expert_advisor_terminals_item import (
            TenantExpertAdvisorTerminalsItem,
        )

        id = str(self.id)

        name = self.name

        version = self.version

        state = self.state.value

        verdict: Union[None, str]
        if isinstance(self.verdict, EaColour):
            verdict = self.verdict.value
        else:
            verdict = self.verdict

        findings = self.findings.to_dict()

        policy_version: Union[None, int]
        policy_version = self.policy_version

        analysers = []
        for analysers_item_data in self.analysers:
            analysers_item = analysers_item_data.to_dict()
            analysers.append(analysers_item)

        source_sha256 = self.source_sha256

        build_sha256: Union[None, str]
        build_sha256 = self.build_sha256

        size_bytes = self.size_bytes

        file_count = self.file_count

        terminals = []
        for terminals_item_data in self.terminals:
            terminals_item = terminals_item_data.to_dict()
            terminals.append(terminals_item)

        decision: Union[None, dict[str, Any]]
        if isinstance(self.decision, TenantExpertAdvisorDecisionType0):
            decision = self.decision.to_dict()
        else:
            decision = self.decision

        source_kept_until: Union[None, str]
        if isinstance(self.source_kept_until, datetime.datetime):
            source_kept_until = self.source_kept_until.isoformat()
        else:
            source_kept_until = self.source_kept_until

        source_deleted_at: Union[None, str]
        if isinstance(self.source_deleted_at, datetime.datetime):
            source_deleted_at = self.source_deleted_at.isoformat()
        else:
            source_deleted_at = self.source_deleted_at

        created_at = self.created_at.isoformat()

        trials: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.trials, Unset):
            trials = self.trials.to_dict()

        uploaded_by_operator = self.uploaded_by_operator

        last_trial: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_trial, Unset):
            last_trial = UNSET
        elif isinstance(self.last_trial, TenantExpertAdvisorLastTrialType0):
            last_trial = self.last_trial.to_dict()
        else:
            last_trial = self.last_trial

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "version": version,
                "state": state,
                "verdict": verdict,
                "findings": findings,
                "policy_version": policy_version,
                "analysers": analysers,
                "source_sha256": source_sha256,
                "build_sha256": build_sha256,
                "size_bytes": size_bytes,
                "file_count": file_count,
                "terminals": terminals,
                "decision": decision,
                "source_kept_until": source_kept_until,
                "source_deleted_at": source_deleted_at,
                "created_at": created_at,
            }
        )
        if trials is not UNSET:
            field_dict["trials"] = trials
        if uploaded_by_operator is not UNSET:
            field_dict["uploaded_by_operator"] = uploaded_by_operator
        if last_trial is not UNSET:
            field_dict["last_trial"] = last_trial

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_trial_count import EaTrialCount
        from ..models.tenant_expert_advisor_analysers_item import (
            TenantExpertAdvisorAnalysersItem,
        )
        from ..models.tenant_expert_advisor_decision_type_0 import (
            TenantExpertAdvisorDecisionType0,
        )
        from ..models.tenant_expert_advisor_findings import TenantExpertAdvisorFindings
        from ..models.tenant_expert_advisor_last_trial_type_0 import (
            TenantExpertAdvisorLastTrialType0,
        )
        from ..models.tenant_expert_advisor_terminals_item import (
            TenantExpertAdvisorTerminalsItem,
        )

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        version = d.pop("version")

        state = TenantExpertAdvisorState(d.pop("state"))

        def _parse_verdict(data: object) -> Union[EaColour, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verdict_type_0 = EaColour(data)

                return verdict_type_0
            except:  # noqa: E722
                pass
            return cast(Union[EaColour, None], data)

        verdict = _parse_verdict(d.pop("verdict"))

        findings = TenantExpertAdvisorFindings.from_dict(d.pop("findings"))

        def _parse_policy_version(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        policy_version = _parse_policy_version(d.pop("policy_version"))

        analysers = []
        _analysers = d.pop("analysers")
        for analysers_item_data in _analysers:
            analysers_item = TenantExpertAdvisorAnalysersItem.from_dict(analysers_item_data)

            analysers.append(analysers_item)

        source_sha256 = d.pop("source_sha256")

        def _parse_build_sha256(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        build_sha256 = _parse_build_sha256(d.pop("build_sha256"))

        size_bytes = d.pop("size_bytes")

        file_count = d.pop("file_count")

        terminals = []
        _terminals = d.pop("terminals")
        for terminals_item_data in _terminals:
            terminals_item = TenantExpertAdvisorTerminalsItem.from_dict(terminals_item_data)

            terminals.append(terminals_item)

        def _parse_decision(data: object) -> Union["TenantExpertAdvisorDecisionType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                decision_type_0 = TenantExpertAdvisorDecisionType0.from_dict(data)

                return decision_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TenantExpertAdvisorDecisionType0", None], data)

        decision = _parse_decision(d.pop("decision"))

        def _parse_source_kept_until(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                source_kept_until_type_0 = isoparse(data)

                return source_kept_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        source_kept_until = _parse_source_kept_until(d.pop("source_kept_until"))

        def _parse_source_deleted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                source_deleted_at_type_0 = isoparse(data)

                return source_deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        source_deleted_at = _parse_source_deleted_at(d.pop("source_deleted_at"))

        created_at = isoparse(d.pop("created_at"))

        _trials = d.pop("trials", UNSET)
        trials: Union[Unset, EaTrialCount]
        if isinstance(_trials, Unset):
            trials = UNSET
        else:
            trials = EaTrialCount.from_dict(_trials)

        uploaded_by_operator = d.pop("uploaded_by_operator", UNSET)

        def _parse_last_trial(
            data: object,
        ) -> Union["TenantExpertAdvisorLastTrialType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_trial_type_0 = TenantExpertAdvisorLastTrialType0.from_dict(data)

                return last_trial_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TenantExpertAdvisorLastTrialType0", None, Unset], data)

        last_trial = _parse_last_trial(d.pop("last_trial", UNSET))

        tenant_expert_advisor = cls(
            id=id,
            name=name,
            version=version,
            state=state,
            verdict=verdict,
            findings=findings,
            policy_version=policy_version,
            analysers=analysers,
            source_sha256=source_sha256,
            build_sha256=build_sha256,
            size_bytes=size_bytes,
            file_count=file_count,
            terminals=terminals,
            decision=decision,
            source_kept_until=source_kept_until,
            source_deleted_at=source_deleted_at,
            created_at=created_at,
            trials=trials,
            uploaded_by_operator=uploaded_by_operator,
            last_trial=last_trial,
        )

        tenant_expert_advisor.additional_properties = d
        return tenant_expert_advisor

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
