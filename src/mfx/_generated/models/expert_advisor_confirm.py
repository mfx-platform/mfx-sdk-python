from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpertAdvisorConfirm")


@_attrs_define
class ExpertAdvisorConfirm:
    """
    Attributes:
        code (str): The one-time code from the trial email sent to the tenant's representative. It is bound to the build
            and the terminal and expires with the trial window plus a day
    """

    code: str

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        expert_advisor_confirm = cls(
            code=code,
        )

        return expert_advisor_confirm
