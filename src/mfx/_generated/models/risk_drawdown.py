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

from ..models.risk_drawdown_kind import RiskDrawdownKind
from ..models.risk_drawdown_peak_basis import RiskDrawdownPeakBasis
from ..models.risk_drawdown_peak_when import RiskDrawdownPeakWhen
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_actions import RiskActions
    from ..models.risk_amount import RiskAmount


T = TypeVar("T", bound="RiskDrawdown")


@_attrs_define
class RiskDrawdown:
    """
    Attributes:
        kind (RiskDrawdownKind):
        limit (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        initial (str): The reference: the balance at activation, or a stated account size
        warn_at (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        act_at (RiskAmount): A limit as money in the account currency, or as a percentage of the rule's reference;
            exactly one
        actions (RiskActions):
        peak_basis (Union[Unset, RiskDrawdownPeakBasis]): trailing only
        peak_when (Union[Unset, RiskDrawdownPeakWhen]): trailing only: every read, or at each reset
    """

    kind: RiskDrawdownKind
    limit: "RiskAmount"
    initial: str
    warn_at: "RiskAmount"
    act_at: "RiskAmount"
    actions: "RiskActions"
    peak_basis: Union[Unset, RiskDrawdownPeakBasis] = UNSET
    peak_when: Union[Unset, RiskDrawdownPeakWhen] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount

        kind = self.kind.value

        limit = self.limit.to_dict()

        initial = self.initial

        warn_at = self.warn_at.to_dict()

        act_at = self.act_at.to_dict()

        actions = self.actions.to_dict()

        peak_basis: Union[Unset, str] = UNSET
        if not isinstance(self.peak_basis, Unset):
            peak_basis = self.peak_basis.value

        peak_when: Union[Unset, str] = UNSET
        if not isinstance(self.peak_when, Unset):
            peak_when = self.peak_when.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "limit": limit,
                "initial": initial,
                "warn_at": warn_at,
                "act_at": act_at,
                "actions": actions,
            }
        )
        if peak_basis is not UNSET:
            field_dict["peak_basis"] = peak_basis
        if peak_when is not UNSET:
            field_dict["peak_when"] = peak_when

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_actions import RiskActions
        from ..models.risk_amount import RiskAmount

        d = dict(src_dict)
        kind = RiskDrawdownKind(d.pop("kind"))

        limit = RiskAmount.from_dict(d.pop("limit"))

        initial = d.pop("initial")

        warn_at = RiskAmount.from_dict(d.pop("warn_at"))

        act_at = RiskAmount.from_dict(d.pop("act_at"))

        actions = RiskActions.from_dict(d.pop("actions"))

        _peak_basis = d.pop("peak_basis", UNSET)
        peak_basis: Union[Unset, RiskDrawdownPeakBasis]
        if isinstance(_peak_basis, Unset):
            peak_basis = UNSET
        else:
            peak_basis = RiskDrawdownPeakBasis(_peak_basis)

        _peak_when = d.pop("peak_when", UNSET)
        peak_when: Union[Unset, RiskDrawdownPeakWhen]
        if isinstance(_peak_when, Unset):
            peak_when = UNSET
        else:
            peak_when = RiskDrawdownPeakWhen(_peak_when)

        risk_drawdown = cls(
            kind=kind,
            limit=limit,
            initial=initial,
            warn_at=warn_at,
            act_at=act_at,
            actions=actions,
            peak_basis=peak_basis,
            peak_when=peak_when,
        )

        risk_drawdown.additional_properties = d
        return risk_drawdown

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
