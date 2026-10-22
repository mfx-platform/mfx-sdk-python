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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tenant_terminal_conditions_additional_property_attributed_to_type_1 import (
    TenantTerminalConditionsAdditionalPropertyAttributedToType1,
)
from ..models.tenant_terminal_conditions_additional_property_attributed_to_type_2_type_1 import (
    TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1,
)
from ..models.tenant_terminal_conditions_additional_property_attributed_to_type_3_type_1 import (
    TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1,
)
from ..models.tenant_terminal_conditions_additional_property_status import (
    TenantTerminalConditionsAdditionalPropertyStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantTerminalConditionsAdditionalProperty")


@_attrs_define
class TenantTerminalConditionsAdditionalProperty:
    """
    Attributes:
        status (Union[Unset, TenantTerminalConditionsAdditionalPropertyStatus]):
        reason (Union[None, Unset, str]): Why, when it is not ok. TicksFresh failed with slow_feed or broker_quiet is
            your broker's feed, timed against its own usual pace
        since (Union[None, Unset, datetime.datetime]):
        attributed_to (Union[None, TenantTerminalConditionsAdditionalPropertyAttributedToType1,
            TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1,
            TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1, Unset]): `broker` when the terminal is
            running, logged in and answering and what is wrong is the broker's own feed (TicksFresh failed with slow_feed or
            broker_quiet): the broker's, not MFX Hub's. Null otherwise (not attributed). `terminal.condition_changed`
            carries the same field, and is sent again when a slow feed becomes a quiet broker or the reverse.
    """

    status: Union[Unset, TenantTerminalConditionsAdditionalPropertyStatus] = UNSET
    reason: Union[None, Unset, str] = UNSET
    since: Union[None, Unset, datetime.datetime] = UNSET
    attributed_to: Union[
        None,
        TenantTerminalConditionsAdditionalPropertyAttributedToType1,
        TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1,
        TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        since: Union[None, Unset, str]
        if isinstance(self.since, Unset):
            since = UNSET
        elif isinstance(self.since, datetime.datetime):
            since = self.since.isoformat()
        else:
            since = self.since

        attributed_to: Union[None, Unset, str]
        if isinstance(self.attributed_to, Unset):
            attributed_to = UNSET
        elif isinstance(
            self.attributed_to, TenantTerminalConditionsAdditionalPropertyAttributedToType1
        ):
            attributed_to = self.attributed_to.value
        elif isinstance(
            self.attributed_to, TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1
        ):
            attributed_to = self.attributed_to.value
        elif isinstance(
            self.attributed_to, TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1
        ):
            attributed_to = self.attributed_to.value
        else:
            attributed_to = self.attributed_to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if reason is not UNSET:
            field_dict["reason"] = reason
        if since is not UNSET:
            field_dict["since"] = since
        if attributed_to is not UNSET:
            field_dict["attributed_to"] = attributed_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: Union[Unset, TenantTerminalConditionsAdditionalPropertyStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TenantTerminalConditionsAdditionalPropertyStatus(_status)

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_since(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                since_type_0 = isoparse(data)

                return since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        since = _parse_since(d.pop("since", UNSET))

        def _parse_attributed_to(
            data: object,
        ) -> Union[
            None,
            TenantTerminalConditionsAdditionalPropertyAttributedToType1,
            TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1,
            TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                attributed_to_type_1 = TenantTerminalConditionsAdditionalPropertyAttributedToType1(
                    data
                )

                return attributed_to_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                attributed_to_type_2_type_1 = (
                    TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1(data)
                )

                return attributed_to_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                attributed_to_type_3_type_1 = (
                    TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1(data)
                )

                return attributed_to_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TenantTerminalConditionsAdditionalPropertyAttributedToType1,
                    TenantTerminalConditionsAdditionalPropertyAttributedToType2Type1,
                    TenantTerminalConditionsAdditionalPropertyAttributedToType3Type1,
                    Unset,
                ],
                data,
            )

        attributed_to = _parse_attributed_to(d.pop("attributed_to", UNSET))

        tenant_terminal_conditions_additional_property = cls(
            status=status,
            reason=reason,
            since=since,
            attributed_to=attributed_to,
        )

        tenant_terminal_conditions_additional_property.additional_properties = d
        return tenant_terminal_conditions_additional_property

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
