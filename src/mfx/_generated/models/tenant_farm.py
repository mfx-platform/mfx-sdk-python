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

from ..models.tenant_farm_os import TenantFarmOs
from ..models.tenant_farm_redundancy import TenantFarmRedundancy
from ..models.tenant_farm_refresh_ms import TenantFarmRefreshMs
from ..models.tenant_farm_status import TenantFarmStatus
from ..models.tenant_farm_usages_item import TenantFarmUsagesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantFarm")


@_attrs_define
class TenantFarm:
    """
    Attributes:
        id (UUID):
        name (str):
        os (TenantFarmOs):
        region (str):
        usages (list[TenantFarmUsagesItem]):
        redundancy (TenantFarmRedundancy):
        refresh_ms (TenantFarmRefreshMs): The default and fastest refresh rate for terminals on this farm
        instruments_max (int): Per terminal: 100 on Windows, 65 on Linux
        status (TenantFarmStatus):
        ha_region (Union[None, Unset, str]):
        depth_max (Union[Unset, int]): How many symbols a terminal on this farm may read the market depth of; 0 means
            the farm offers no depth. The platform's own per-terminal cap may be lower: a refusal names the number that
            applied
        customer_code (Union[Unset, bool]): Whether a terminal on this farm may run your own expert advisor. A terminal
            you create without naming a farm is never placed on such a farm: name it
    """

    id: UUID
    name: str
    os: TenantFarmOs
    region: str
    usages: list[TenantFarmUsagesItem]
    redundancy: TenantFarmRedundancy
    refresh_ms: TenantFarmRefreshMs
    instruments_max: int
    status: TenantFarmStatus
    ha_region: Union[None, Unset, str] = UNSET
    depth_max: Union[Unset, int] = UNSET
    customer_code: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        os = self.os.value

        region = self.region

        usages = []
        for usages_item_data in self.usages:
            usages_item = usages_item_data.value
            usages.append(usages_item)

        redundancy = self.redundancy.value

        refresh_ms = self.refresh_ms.value

        instruments_max = self.instruments_max

        status = self.status.value

        ha_region: Union[None, Unset, str]
        if isinstance(self.ha_region, Unset):
            ha_region = UNSET
        else:
            ha_region = self.ha_region

        depth_max = self.depth_max

        customer_code = self.customer_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "os": os,
                "region": region,
                "usages": usages,
                "redundancy": redundancy,
                "refresh_ms": refresh_ms,
                "instruments_max": instruments_max,
                "status": status,
            }
        )
        if ha_region is not UNSET:
            field_dict["ha_region"] = ha_region
        if depth_max is not UNSET:
            field_dict["depth_max"] = depth_max
        if customer_code is not UNSET:
            field_dict["customer_code"] = customer_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        os = TenantFarmOs(d.pop("os"))

        region = d.pop("region")

        usages = []
        _usages = d.pop("usages")
        for usages_item_data in _usages:
            usages_item = TenantFarmUsagesItem(usages_item_data)

            usages.append(usages_item)

        redundancy = TenantFarmRedundancy(d.pop("redundancy"))

        refresh_ms = TenantFarmRefreshMs(d.pop("refresh_ms"))

        instruments_max = d.pop("instruments_max")

        status = TenantFarmStatus(d.pop("status"))

        def _parse_ha_region(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ha_region = _parse_ha_region(d.pop("ha_region", UNSET))

        depth_max = d.pop("depth_max", UNSET)

        customer_code = d.pop("customer_code", UNSET)

        tenant_farm = cls(
            id=id,
            name=name,
            os=os,
            region=region,
            usages=usages,
            redundancy=redundancy,
            refresh_ms=refresh_ms,
            instruments_max=instruments_max,
            status=status,
            ha_region=ha_region,
            depth_max=depth_max,
            customer_code=customer_code,
        )

        tenant_farm.additional_properties = d
        return tenant_farm

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
