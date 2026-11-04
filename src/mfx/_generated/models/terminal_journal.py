import datetime
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
from dateutil.parser import isoparse

from ..models.terminal_journal_from import TerminalJournalFrom
from ..models.terminal_journal_stopped_type_1 import TerminalJournalStoppedType1
from ..models.terminal_journal_stopped_type_2_type_1 import (
    TerminalJournalStoppedType2Type1,
)
from ..models.terminal_journal_stopped_type_3_type_1 import (
    TerminalJournalStoppedType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.journal_line import JournalLine


T = TypeVar("T", bound="TerminalJournal")


@_attrs_define
class TerminalJournal:
    """
    Attributes:
        terminal_id (UUID):
        from_ (TerminalJournalFrom): live: read from the running terminal now. last_words: kept by its cell when it
            stopped
        read_at (datetime.datetime): When the cell read the journal: now for live, the stop for last_words
        lines (list['JournalLine']): Newest first
        stopped (Union[None, TerminalJournalStoppedType1, TerminalJournalStoppedType2Type1,
            TerminalJournalStoppedType3Type1, Unset]): For last_words, why the cell kept them; null for live
    """

    terminal_id: UUID
    from_: TerminalJournalFrom
    read_at: datetime.datetime
    lines: list["JournalLine"]
    stopped: Union[
        None,
        TerminalJournalStoppedType1,
        TerminalJournalStoppedType2Type1,
        TerminalJournalStoppedType3Type1,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.journal_line import JournalLine

        terminal_id = str(self.terminal_id)

        from_ = self.from_.value

        read_at = self.read_at.isoformat()

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        stopped: Union[None, Unset, str]
        if isinstance(self.stopped, Unset):
            stopped = UNSET
        elif isinstance(self.stopped, TerminalJournalStoppedType1):
            stopped = self.stopped.value
        elif isinstance(self.stopped, TerminalJournalStoppedType2Type1):
            stopped = self.stopped.value
        elif isinstance(self.stopped, TerminalJournalStoppedType3Type1):
            stopped = self.stopped.value
        else:
            stopped = self.stopped

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "from": from_,
                "read_at": read_at,
                "lines": lines,
            }
        )
        if stopped is not UNSET:
            field_dict["stopped"] = stopped

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.journal_line import JournalLine

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        from_ = TerminalJournalFrom(d.pop("from"))

        read_at = isoparse(d.pop("read_at"))

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = JournalLine.from_dict(lines_item_data)

            lines.append(lines_item)

        def _parse_stopped(
            data: object,
        ) -> Union[
            None,
            TerminalJournalStoppedType1,
            TerminalJournalStoppedType2Type1,
            TerminalJournalStoppedType3Type1,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stopped_type_1 = TerminalJournalStoppedType1(data)

                return stopped_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stopped_type_2_type_1 = TerminalJournalStoppedType2Type1(data)

                return stopped_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stopped_type_3_type_1 = TerminalJournalStoppedType3Type1(data)

                return stopped_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TerminalJournalStoppedType1,
                    TerminalJournalStoppedType2Type1,
                    TerminalJournalStoppedType3Type1,
                    Unset,
                ],
                data,
            )

        stopped = _parse_stopped(d.pop("stopped", UNSET))

        terminal_journal = cls(
            terminal_id=terminal_id,
            from_=from_,
            read_at=read_at,
            lines=lines,
            stopped=stopped,
        )

        terminal_journal.additional_properties = d
        return terminal_journal

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
