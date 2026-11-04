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
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.broker_catalogue_source import BrokerCatalogueSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="BrokerCatalogue")


@_attrs_define
class BrokerCatalogue:
    """
    Attributes:
        server_id (UUID):
        account_type (str): The broker's symbol variant, as on GET /brokers/{id}/symbols
        source (BrokerCatalogueSource): As SymbolPage.source
        catalogue_hash (str): sha256 over every listed symbol's name, spec_hash, description and identity fields, in
            name order
        symbols (int): Symbols listed now (removed ones excluded)
        refreshed_at (datetime.datetime): The newest refreshed_at of its rows
    """

    server_id: UUID
    account_type: str
    source: BrokerCatalogueSource
    catalogue_hash: str
    symbols: int
    refreshed_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        server_id = str(self.server_id)

        account_type = self.account_type

        source = self.source.value

        catalogue_hash = self.catalogue_hash

        symbols = self.symbols

        refreshed_at = self.refreshed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "server_id": server_id,
                "account_type": account_type,
                "source": source,
                "catalogue_hash": catalogue_hash,
                "symbols": symbols,
                "refreshed_at": refreshed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_id = UUID(d.pop("server_id"))

        account_type = d.pop("account_type")

        source = BrokerCatalogueSource(d.pop("source"))

        catalogue_hash = d.pop("catalogue_hash")

        symbols = d.pop("symbols")

        refreshed_at = isoparse(d.pop("refreshed_at"))

        broker_catalogue = cls(
            server_id=server_id,
            account_type=account_type,
            source=source,
            catalogue_hash=catalogue_hash,
            symbols=symbols,
            refreshed_at=refreshed_at,
        )

        broker_catalogue.additional_properties = d
        return broker_catalogue

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
