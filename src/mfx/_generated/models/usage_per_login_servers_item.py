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

from ..models.usage_per_login_servers_item_max_sessions_source_type_1 import (
    UsagePerLoginServersItemMaxSessionsSourceType1,
)
from ..models.usage_per_login_servers_item_max_sessions_source_type_2_type_1 import (
    UsagePerLoginServersItemMaxSessionsSourceType2Type1,
)
from ..models.usage_per_login_servers_item_max_sessions_source_type_3_type_1 import (
    UsagePerLoginServersItemMaxSessionsSourceType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref import Ref


T = TypeVar("T", bound="UsagePerLoginServersItem")


@_attrs_define
class UsagePerLoginServersItem:
    """
    Attributes:
        broker (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        server (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        max_sessions (Union[None, int]): Null: not known yet
        max_sessions_source (Union[None, UsagePerLoginServersItemMaxSessionsSourceType1,
            UsagePerLoginServersItemMaxSessionsSourceType2Type1, UsagePerLoginServersItemMaxSessionsSourceType3Type1]):
            `probed`: seen to hold this many, a lower bound; `limit`: the ceiling found; `operator`: entered, final
    """

    broker: "Ref"
    server: "Ref"
    max_sessions: Union[None, int]
    max_sessions_source: Union[
        None,
        UsagePerLoginServersItemMaxSessionsSourceType1,
        UsagePerLoginServersItemMaxSessionsSourceType2Type1,
        UsagePerLoginServersItemMaxSessionsSourceType3Type1,
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ref import Ref

        broker = self.broker.to_dict()

        server = self.server.to_dict()

        max_sessions: Union[None, int]
        max_sessions = self.max_sessions

        max_sessions_source: Union[None, str]
        if isinstance(self.max_sessions_source, UsagePerLoginServersItemMaxSessionsSourceType1):
            max_sessions_source = self.max_sessions_source.value
        elif isinstance(
            self.max_sessions_source, UsagePerLoginServersItemMaxSessionsSourceType2Type1
        ):
            max_sessions_source = self.max_sessions_source.value
        elif isinstance(
            self.max_sessions_source, UsagePerLoginServersItemMaxSessionsSourceType3Type1
        ):
            max_sessions_source = self.max_sessions_source.value
        else:
            max_sessions_source = self.max_sessions_source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "broker": broker,
                "server": server,
                "max_sessions": max_sessions,
                "max_sessions_source": max_sessions_source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ref import Ref

        d = dict(src_dict)
        broker = Ref.from_dict(d.pop("broker"))

        server = Ref.from_dict(d.pop("server"))

        def _parse_max_sessions(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_sessions = _parse_max_sessions(d.pop("max_sessions"))

        def _parse_max_sessions_source(
            data: object,
        ) -> Union[
            None,
            UsagePerLoginServersItemMaxSessionsSourceType1,
            UsagePerLoginServersItemMaxSessionsSourceType2Type1,
            UsagePerLoginServersItemMaxSessionsSourceType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                max_sessions_source_type_1 = UsagePerLoginServersItemMaxSessionsSourceType1(data)

                return max_sessions_source_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                max_sessions_source_type_2_type_1 = (
                    UsagePerLoginServersItemMaxSessionsSourceType2Type1(data)
                )

                return max_sessions_source_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                max_sessions_source_type_3_type_1 = (
                    UsagePerLoginServersItemMaxSessionsSourceType3Type1(data)
                )

                return max_sessions_source_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    UsagePerLoginServersItemMaxSessionsSourceType1,
                    UsagePerLoginServersItemMaxSessionsSourceType2Type1,
                    UsagePerLoginServersItemMaxSessionsSourceType3Type1,
                ],
                data,
            )

        max_sessions_source = _parse_max_sessions_source(d.pop("max_sessions_source"))

        usage_per_login_servers_item = cls(
            broker=broker,
            server=server,
            max_sessions=max_sessions,
            max_sessions_source=max_sessions_source,
        )

        usage_per_login_servers_item.additional_properties = d
        return usage_per_login_servers_item

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
