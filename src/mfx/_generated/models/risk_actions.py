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

from ..models.risk_action_kind import RiskActionKind
from ..models.risk_actions_cancel_scope import RiskActionsCancelScope
from ..models.risk_actions_close_scope import RiskActionsCloseScope
from ..types import UNSET, Unset

T = TypeVar("T", bound="RiskActions")


@_attrs_define
class RiskActions:
    """
    Attributes:
        kinds (list[RiskActionKind]):
        cancel_scope (Union[Unset, RiskActionsCancelScope]): Which pending orders cancel_pending reaches
        close_scope (Union[Unset, RiskActionsCloseScope]): Which positions close_positions reaches; previewed before the
            version is saved
    """

    kinds: list[RiskActionKind]
    cancel_scope: Union[Unset, RiskActionsCancelScope] = UNSET
    close_scope: Union[Unset, RiskActionsCloseScope] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kinds = []
        for kinds_item_data in self.kinds:
            kinds_item = kinds_item_data.value
            kinds.append(kinds_item)

        cancel_scope: Union[Unset, str] = UNSET
        if not isinstance(self.cancel_scope, Unset):
            cancel_scope = self.cancel_scope.value

        close_scope: Union[Unset, str] = UNSET
        if not isinstance(self.close_scope, Unset):
            close_scope = self.close_scope.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kinds": kinds,
            }
        )
        if cancel_scope is not UNSET:
            field_dict["cancel_scope"] = cancel_scope
        if close_scope is not UNSET:
            field_dict["close_scope"] = close_scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kinds = []
        _kinds = d.pop("kinds")
        for kinds_item_data in _kinds:
            kinds_item = RiskActionKind(kinds_item_data)

            kinds.append(kinds_item)

        _cancel_scope = d.pop("cancel_scope", UNSET)
        cancel_scope: Union[Unset, RiskActionsCancelScope]
        if isinstance(_cancel_scope, Unset):
            cancel_scope = UNSET
        else:
            cancel_scope = RiskActionsCancelScope(_cancel_scope)

        _close_scope = d.pop("close_scope", UNSET)
        close_scope: Union[Unset, RiskActionsCloseScope]
        if isinstance(_close_scope, Unset):
            close_scope = UNSET
        else:
            close_scope = RiskActionsCloseScope(_close_scope)

        risk_actions = cls(
            kinds=kinds,
            cancel_scope=cancel_scope,
            close_scope=close_scope,
        )

        risk_actions.additional_properties = d
        return risk_actions

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
