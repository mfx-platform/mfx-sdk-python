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
    from ..models.expert_advisor_upload_files_item import ExpertAdvisorUploadFilesItem


T = TypeVar("T", bound="ExpertAdvisorUpload")


@_attrs_define
class ExpertAdvisorUpload:
    """One expert advisor's source: its `.mq5` and its own includes (`.mqh`). The platform reads it, checks it and builds
    it, so what runs is what was checked. A compiled `.ex5` is refused: it cannot be read. The size of the whole bundle
    and the number of files are bounded (8 MiB and 30 files unless an operator has changed them).

        Attributes:
            name (str): What the tenant calls it. Each upload under a name is its next version
            files (list['ExpertAdvisorUploadFilesItem']):
    """

    name: str
    files: list["ExpertAdvisorUploadFilesItem"]

    def to_dict(self) -> dict[str, Any]:
        from ..models.expert_advisor_upload_files_item import (
            ExpertAdvisorUploadFilesItem,
        )

        name = self.name

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.expert_advisor_upload_files_item import (
            ExpertAdvisorUploadFilesItem,
        )

        d = dict(src_dict)
        name = d.pop("name")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = ExpertAdvisorUploadFilesItem.from_dict(files_item_data)

            files.append(files_item)

        expert_advisor_upload = cls(
            name=name,
            files=files,
        )

        return expert_advisor_upload
