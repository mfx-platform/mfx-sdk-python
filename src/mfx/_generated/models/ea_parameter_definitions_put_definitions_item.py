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

from ..models.ea_parameter_definitions_put_definitions_item_type import (
    EaParameterDefinitionsPutDefinitionsItemType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="EaParameterDefinitionsPutDefinitionsItem")


@_attrs_define
class EaParameterDefinitionsPutDefinitionsItem:
    """
    Attributes:
        key (str):
        type_ (EaParameterDefinitionsPutDefinitionsItemType):
        label (Union[Unset, str]): The key when absent
        default (Union[Unset, Any]): Fits the definition
        min_ (Union[None, Unset, float]):
        max_ (Union[None, Unset, float]):
        choices (Union[None, Unset, list[str]]):
        help_ (Union[None, Unset, str]):
    """

    key: str
    type_: EaParameterDefinitionsPutDefinitionsItemType
    label: Union[Unset, str] = UNSET
    default: Union[Unset, Any] = UNSET
    min_: Union[None, Unset, float] = UNSET
    max_: Union[None, Unset, float] = UNSET
    choices: Union[None, Unset, list[str]] = UNSET
    help_: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        type_ = self.type_.value

        label = self.label

        default = self.default

        min_: Union[None, Unset, float]
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        max_: Union[None, Unset, float]
        if isinstance(self.max_, Unset):
            max_ = UNSET
        else:
            max_ = self.max_

        choices: Union[None, Unset, list[str]]
        if isinstance(self.choices, Unset):
            choices = UNSET
        elif isinstance(self.choices, list):
            choices = self.choices

        else:
            choices = self.choices

        help_: Union[None, Unset, str]
        if isinstance(self.help_, Unset):
            help_ = UNSET
        else:
            help_ = self.help_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "key": key,
                "type": type_,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if default is not UNSET:
            field_dict["default"] = default
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if choices is not UNSET:
            field_dict["choices"] = choices
        if help_ is not UNSET:
            field_dict["help"] = help_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        type_ = EaParameterDefinitionsPutDefinitionsItemType._read(d.pop("type"))

        label = d.pop("label", UNSET)

        default = d.pop("default", UNSET)

        def _parse_min_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        max_ = _parse_max_(d.pop("max", UNSET))

        def _parse_choices(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                choices_type_0 = cast(list[str], data)

                return choices_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        choices = _parse_choices(d.pop("choices", UNSET))

        def _parse_help_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        help_ = _parse_help_(d.pop("help", UNSET))

        ea_parameter_definitions_put_definitions_item = cls(
            key=key,
            type_=type_,
            label=label,
            default=default,
            min_=min_,
            max_=max_,
            choices=choices,
            help_=help_,
        )

        return ea_parameter_definitions_put_definitions_item
