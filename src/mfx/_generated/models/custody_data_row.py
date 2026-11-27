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

from ..models.custody_data_row_data import CustodyDataRowData
from ..models.custody_data_row_held import CustodyDataRowHeld
from ..models.custody_data_row_readers_item import CustodyDataRowReadersItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustodyDataRow")


@_attrs_define
class CustodyDataRow:
    """One kind of trading data: where it is held and who can read it

    Attributes:
        data (CustodyDataRowData): broker_password: the broker password. account_identity: the broker login, the account
            name and the server. trading_records: orders, fills, positions, balances and the account profile.
            instrument_names: the names of the instruments.
        label (str): The kind of data in words, e.g. "Broker password"
        held (CustodyDataRowHeld): vault_released_to_attested_machine: in a hardware-protected vault, released only to
            an attested confidential machine and wrapped to that machine's own trusted platform module.
            encrypted_under_your_key: stored encrypted under the organisation's key; trading records pass through the
            machine's own short-lived streams only. in_clear: not encrypted under the organisation's key.
        held_text (str): Where it is held, in words, as the page shows it
        readers (list[CustodyDataRowReadersItem]): Who can read it. account_signed_in: the platform, in memory on the
            attested machine, while the account is signed in. you_through_the_api: the organisation, through the API.
            attested_machine: the attested confidential machine that runs the account. operators: MFX Hub's operators.
        readers_text (str): Who can read it, in words, as the page shows it
        why (Union[None, str]): Why a kind of data is held in clear (instrument names: quotes are routed by symbol);
            null for the rest
    """

    data: CustodyDataRowData
    label: str
    held: CustodyDataRowHeld
    held_text: str
    readers: list[CustodyDataRowReadersItem]
    readers_text: str
    why: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.value

        label = self.label

        held = self.held.value

        held_text = self.held_text

        readers = []
        for readers_item_data in self.readers:
            readers_item = readers_item_data.value
            readers.append(readers_item)

        readers_text = self.readers_text

        why: Union[None, str]
        why = self.why

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "label": label,
                "held": held,
                "held_text": held_text,
                "readers": readers,
                "readers_text": readers_text,
                "why": why,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data = CustodyDataRowData._read(d.pop("data"))

        label = d.pop("label")

        held = CustodyDataRowHeld._read(d.pop("held"))

        held_text = d.pop("held_text")

        readers = []
        _readers = d.pop("readers")
        for readers_item_data in _readers:
            readers_item = CustodyDataRowReadersItem._read(readers_item_data)

            readers.append(readers_item)

        readers_text = d.pop("readers_text")

        def _parse_why(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        why = _parse_why(d.pop("why"))

        custody_data_row = cls(
            data=data,
            label=label,
            held=held,
            held_text=held_text,
            readers=readers,
            readers_text=readers_text,
            why=why,
        )

        custody_data_row.additional_properties = d
        return custody_data_row

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
