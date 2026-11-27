from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_parameter_definitions_put_definitions_item import (
        EaParameterDefinitionsPutDefinitionsItem,
    )


T = TypeVar("T", bound="EaParameterDefinitionsPut")


@_attrs_define
class EaParameterDefinitionsPut:
    """
    Attributes:
        definitions (list['EaParameterDefinitionsPutDefinitionsItem']):
    """

    definitions: list["EaParameterDefinitionsPutDefinitionsItem"]

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_parameter_definitions_put_definitions_item import (
            EaParameterDefinitionsPutDefinitionsItem,
        )

        definitions = []
        for definitions_item_data in self.definitions:
            definitions_item = definitions_item_data.to_dict()
            definitions.append(definitions_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "definitions": definitions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_parameter_definitions_put_definitions_item import (
            EaParameterDefinitionsPutDefinitionsItem,
        )

        d = dict(src_dict)
        definitions = []
        _definitions = d.pop("definitions")
        for definitions_item_data in _definitions:
            definitions_item = EaParameterDefinitionsPutDefinitionsItem.from_dict(
                definitions_item_data
            )

            definitions.append(definitions_item)

        ea_parameter_definitions_put = cls(
            definitions=definitions,
        )

        return ea_parameter_definitions_put
