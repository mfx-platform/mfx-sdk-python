from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpertAdvisorUploadFilesItem")


@_attrs_define
class ExpertAdvisorUploadFilesItem:
    """
    Attributes:
        path (str): Where the file sits inside the bundle, with forward slashes and no `..`: `MyEa.mq5`,
            `Include/risk.mqh`. Exactly one file is the `.mq5`; every other file is a `.mqh`. An `#include` is resolved
            inside the bundle or in MetaTrader's standard library, nowhere else
        content_base64 (str): The file, base64. Text, in UTF-8 or in UTF-16 with a byte order mark, as MetaEditor saves
            it
    """

    path: str
    content_base64: str

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        content_base64 = self.content_base64

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "content_base64": content_base64,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        content_base64 = d.pop("content_base64")

        expert_advisor_upload_files_item = cls(
            path=path,
            content_base64=content_base64,
        )

        return expert_advisor_upload_files_item
