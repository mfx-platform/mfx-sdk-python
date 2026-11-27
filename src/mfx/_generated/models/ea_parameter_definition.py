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

from ..models.ea_parameter_definition_type import EaParameterDefinitionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EaParameterDefinition")


@_attrs_define
class EaParameterDefinition:
    """One parameter of an advisor version, as its form shows it

    Attributes:
        key (str):
        label (str):
        type_ (EaParameterDefinitionType):
        default (Any): Fits the definition; null for none
        min_ (Union[None, float]):
        max_ (Union[None, float]):
        choices (Union[None, list[str]]): The words a choice offers; null for every other type
        help_ (Union[None, str]):
        position (int):
    """

    key: str
    label: str
    type_: EaParameterDefinitionType
    default: Any
    min_: Union[None, float]
    max_: Union[None, float]
    choices: Union[None, list[str]]
    help_: Union[None, str]
    position: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        label = self.label

        type_ = self.type_.value

        default = self.default

        min_: Union[None, float]
        min_ = self.min_

        max_: Union[None, float]
        max_ = self.max_

        choices: Union[None, list[str]]
        if isinstance(self.choices, list):
            choices = self.choices

        else:
            choices = self.choices

        help_: Union[None, str]
        help_ = self.help_

        position = self.position

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "label": label,
                "type": type_,
                "default": default,
                "min": min_,
                "max": max_,
                "choices": choices,
                "help": help_,
                "position": position,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        label = d.pop("label")

        type_ = EaParameterDefinitionType._read(d.pop("type"))

        default = d.pop("default")

        def _parse_min_(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        min_ = _parse_min_(d.pop("min"))

        def _parse_max_(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        max_ = _parse_max_(d.pop("max"))

        def _parse_choices(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                choices_type_0 = cast(list[str], data)

                return choices_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        choices = _parse_choices(d.pop("choices"))

        def _parse_help_(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        help_ = _parse_help_(d.pop("help"))

        position = d.pop("position")

        ea_parameter_definition = cls(
            key=key,
            label=label,
            type_=type_,
            default=default,
            min_=min_,
            max_=max_,
            choices=choices,
            help_=help_,
            position=position,
        )

        ea_parameter_definition.additional_properties = d
        return ea_parameter_definition

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
