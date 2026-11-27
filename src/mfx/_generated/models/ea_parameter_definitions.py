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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_parameter_definition import EaParameterDefinition


T = TypeVar("T", bound="EaParameterDefinitions")


@_attrs_define
class EaParameterDefinitions:
    """
    Attributes:
        definitions (list['EaParameterDefinition']):
        proposed_from_source (bool): True when the list is a draft read from the source, not kept yet
        inherited_from (Union[None, UUID]): The previous version whose definitions these are, until this version keeps
            its own
    """

    definitions: list["EaParameterDefinition"]
    proposed_from_source: bool
    inherited_from: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_parameter_definition import EaParameterDefinition

        definitions = []
        for definitions_item_data in self.definitions:
            definitions_item = definitions_item_data.to_dict()
            definitions.append(definitions_item)

        proposed_from_source = self.proposed_from_source

        inherited_from: Union[None, str]
        if isinstance(self.inherited_from, UUID):
            inherited_from = str(self.inherited_from)
        else:
            inherited_from = self.inherited_from

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "definitions": definitions,
                "proposed_from_source": proposed_from_source,
                "inherited_from": inherited_from,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_parameter_definition import EaParameterDefinition

        d = dict(src_dict)
        definitions = []
        _definitions = d.pop("definitions")
        for definitions_item_data in _definitions:
            definitions_item = EaParameterDefinition.from_dict(definitions_item_data)

            definitions.append(definitions_item)

        proposed_from_source = d.pop("proposed_from_source")

        def _parse_inherited_from(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                inherited_from_type_0 = UUID(data)

                return inherited_from_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        inherited_from = _parse_inherited_from(d.pop("inherited_from"))

        ea_parameter_definitions = cls(
            definitions=definitions,
            proposed_from_source=proposed_from_source,
            inherited_from=inherited_from,
        )

        ea_parameter_definitions.additional_properties = d
        return ea_parameter_definitions

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
