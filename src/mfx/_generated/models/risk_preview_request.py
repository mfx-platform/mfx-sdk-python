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

from ..models.risk_preview_request_entry_type import RiskPreviewRequestEntryType
from ..models.risk_preview_request_side import RiskPreviewRequestSide
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_budget import RiskBudget
    from ..models.risk_preview_request_assumptions import RiskPreviewRequestAssumptions


T = TypeVar("T", bound="RiskPreviewRequest")


@_attrs_define
class RiskPreviewRequest:
    """
    Attributes:
        terminal_id (UUID):
        symbol (str):
        side (RiskPreviewRequestSide):
        entry_type (RiskPreviewRequestEntryType):
        sl (str):
        budget (RiskBudget):
        entry_price (Union[None, Unset, str]): Needed for limit and stop; market uses the current price
        tp (Union[None, Unset, str]):
        slippage (Union[None, Unset, str]): A price distance the caller assumes; null is none
        assumptions (Union[Unset, RiskPreviewRequestAssumptions]): Costs the specification does not give, stated by the
            caller
    """

    terminal_id: UUID
    symbol: str
    side: RiskPreviewRequestSide
    entry_type: RiskPreviewRequestEntryType
    sl: str
    budget: "RiskBudget"
    entry_price: Union[None, Unset, str] = UNSET
    tp: Union[None, Unset, str] = UNSET
    slippage: Union[None, Unset, str] = UNSET
    assumptions: Union[Unset, "RiskPreviewRequestAssumptions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_budget import RiskBudget
        from ..models.risk_preview_request_assumptions import (
            RiskPreviewRequestAssumptions,
        )

        terminal_id = str(self.terminal_id)

        symbol = self.symbol

        side = self.side.value

        entry_type = self.entry_type.value

        sl = self.sl

        budget = self.budget.to_dict()

        entry_price: Union[None, Unset, str]
        if isinstance(self.entry_price, Unset):
            entry_price = UNSET
        else:
            entry_price = self.entry_price

        tp: Union[None, Unset, str]
        if isinstance(self.tp, Unset):
            tp = UNSET
        else:
            tp = self.tp

        slippage: Union[None, Unset, str]
        if isinstance(self.slippage, Unset):
            slippage = UNSET
        else:
            slippage = self.slippage

        assumptions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.assumptions, Unset):
            assumptions = self.assumptions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "symbol": symbol,
                "side": side,
                "entry_type": entry_type,
                "sl": sl,
                "budget": budget,
            }
        )
        if entry_price is not UNSET:
            field_dict["entry_price"] = entry_price
        if tp is not UNSET:
            field_dict["tp"] = tp
        if slippage is not UNSET:
            field_dict["slippage"] = slippage
        if assumptions is not UNSET:
            field_dict["assumptions"] = assumptions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_budget import RiskBudget
        from ..models.risk_preview_request_assumptions import (
            RiskPreviewRequestAssumptions,
        )

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        symbol = d.pop("symbol")

        side = RiskPreviewRequestSide(d.pop("side"))

        entry_type = RiskPreviewRequestEntryType(d.pop("entry_type"))

        sl = d.pop("sl")

        budget = RiskBudget.from_dict(d.pop("budget"))

        def _parse_entry_price(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        entry_price = _parse_entry_price(d.pop("entry_price", UNSET))

        def _parse_tp(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tp = _parse_tp(d.pop("tp", UNSET))

        def _parse_slippage(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slippage = _parse_slippage(d.pop("slippage", UNSET))

        _assumptions = d.pop("assumptions", UNSET)
        assumptions: Union[Unset, RiskPreviewRequestAssumptions]
        if isinstance(_assumptions, Unset):
            assumptions = UNSET
        else:
            assumptions = RiskPreviewRequestAssumptions.from_dict(_assumptions)

        risk_preview_request = cls(
            terminal_id=terminal_id,
            symbol=symbol,
            side=side,
            entry_type=entry_type,
            sl=sl,
            budget=budget,
            entry_price=entry_price,
            tp=tp,
            slippage=slippage,
            assumptions=assumptions,
        )

        risk_preview_request.additional_properties = d
        return risk_preview_request

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
