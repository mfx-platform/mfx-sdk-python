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

from ..models.credential_accepted_cred_type import CredentialAcceptedCredType
from ..models.credential_accepted_takes_effect import CredentialAcceptedTakesEffect
from ..types import UNSET, Unset

T = TypeVar("T", bound="CredentialAccepted")


@_attrs_define
class CredentialAccepted:
    """The reference, and nothing else. There is no property here a secret could live in, and nothing a client could do
    with the reference that resubmitting would not do better.

        Attributes:
            rotated (bool): True when this replaced the credential the terminal already had
            takes_effect (CredentialAcceptedTakesEffect): When the terminal logs in with what was submitted. `first_login`
                for a first credential. For a rotation: `restart` (it was ACTIVE and is being restarted now), `retry_login` (it
                was FAILED and rejoins the login queue now), or `next_login` (nothing was started, or the operation was refused;
                its next login uses it).
            operation_id (Union[None, UUID]): The restart or retry-login a rotation opened, to follow on the operations
                routes; null when none
            credential_ref_id (UUID):
            terminal_id (UUID):
            cred_type (CredentialAcceptedCredType):
            execution_disabled (bool): True when this submission turned execution off, so the caller learns it here rather
                than from an order being refused later.
            not_applied_reason (Union[None, Unset, str]): Why a rotation of a running terminal was not applied now
                (`takes_effect` is `next_login` because the restart or retry-login was refused): the refusal's own `error.code`,
                such as `operation_in_progress`, `cooldown`, `tenant_rate` or `positions_open`. Null in every other answer. The
                credential is stored either way.
            same_login_terminals_stale (Union[Unset, int]): On a password change (`rotated: true`): how many of your OTHER
                live terminals use the same login and were last given their password before this submission. Each terminal holds
                its own credential, so after changing the password at the broker, submit it to each of them. 0 in every other
                answer.
    """

    rotated: bool
    takes_effect: CredentialAcceptedTakesEffect
    operation_id: Union[None, UUID]
    credential_ref_id: UUID
    terminal_id: UUID
    cred_type: CredentialAcceptedCredType
    execution_disabled: bool
    not_applied_reason: Union[None, Unset, str] = UNSET
    same_login_terminals_stale: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rotated = self.rotated

        takes_effect = self.takes_effect.value

        operation_id: Union[None, str]
        if isinstance(self.operation_id, UUID):
            operation_id = str(self.operation_id)
        else:
            operation_id = self.operation_id

        credential_ref_id = str(self.credential_ref_id)

        terminal_id = str(self.terminal_id)

        cred_type = self.cred_type.value

        execution_disabled = self.execution_disabled

        not_applied_reason: Union[None, Unset, str]
        if isinstance(self.not_applied_reason, Unset):
            not_applied_reason = UNSET
        else:
            not_applied_reason = self.not_applied_reason

        same_login_terminals_stale = self.same_login_terminals_stale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rotated": rotated,
                "takes_effect": takes_effect,
                "operation_id": operation_id,
                "credential_ref_id": credential_ref_id,
                "terminal_id": terminal_id,
                "cred_type": cred_type,
                "execution_disabled": execution_disabled,
            }
        )
        if not_applied_reason is not UNSET:
            field_dict["not_applied_reason"] = not_applied_reason
        if same_login_terminals_stale is not UNSET:
            field_dict["same_login_terminals_stale"] = same_login_terminals_stale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rotated = d.pop("rotated")

        takes_effect = CredentialAcceptedTakesEffect(d.pop("takes_effect"))

        def _parse_operation_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operation_id_type_0 = UUID(data)

                return operation_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        operation_id = _parse_operation_id(d.pop("operation_id"))

        credential_ref_id = UUID(d.pop("credential_ref_id"))

        terminal_id = UUID(d.pop("terminal_id"))

        cred_type = CredentialAcceptedCredType(d.pop("cred_type"))

        execution_disabled = d.pop("execution_disabled")

        def _parse_not_applied_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        not_applied_reason = _parse_not_applied_reason(d.pop("not_applied_reason", UNSET))

        same_login_terminals_stale = d.pop("same_login_terminals_stale", UNSET)

        credential_accepted = cls(
            rotated=rotated,
            takes_effect=takes_effect,
            operation_id=operation_id,
            credential_ref_id=credential_ref_id,
            terminal_id=terminal_id,
            cred_type=cred_type,
            execution_disabled=execution_disabled,
            not_applied_reason=not_applied_reason,
            same_login_terminals_stale=same_login_terminals_stale,
        )

        credential_accepted.additional_properties = d
        return credential_accepted

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
