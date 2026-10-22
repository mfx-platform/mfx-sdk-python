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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.credential_submission_cred_type import CredentialSubmissionCredType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CredentialSubmission")


@_attrs_define
class CredentialSubmission:
    """What a tenant sends to put its own broker login on a terminal. The only request body in MFX Hub that carries a
    secret: it is read once, wrapped, written to the platform's secret store and never kept anywhere else, logged or
    echoed. Unknown properties are refused rather than ignored, so a misspelled password is an error and not a
    credential with no password.

        Attributes:
            login (int): The MT5 account number
            password (str):
            server (str): Must be the terminal's own broker server; a mismatch is a 400
            cred_type (Union[Unset, CredentialSubmissionCredType]): An investor credential turns execution off Default:
                CredentialSubmissionCredType.MASTER.
    """

    login: int
    password: str
    server: str
    cred_type: Union[Unset, CredentialSubmissionCredType] = CredentialSubmissionCredType.MASTER

    def to_dict(self) -> dict[str, Any]:
        login = self.login

        password = self.password

        server = self.server

        cred_type: Union[Unset, str] = UNSET
        if not isinstance(self.cred_type, Unset):
            cred_type = self.cred_type.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "login": login,
                "password": password,
                "server": server,
            }
        )
        if cred_type is not UNSET:
            field_dict["cred_type"] = cred_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        login = d.pop("login")

        password = d.pop("password")

        server = d.pop("server")

        _cred_type = d.pop("cred_type", UNSET)
        cred_type: Union[Unset, CredentialSubmissionCredType]
        if isinstance(_cred_type, Unset):
            cred_type = UNSET
        else:
            cred_type = CredentialSubmissionCredType(_cred_type)

        credential_submission = cls(
            login=login,
            password=password,
            server=server,
            cred_type=cred_type,
        )

        return credential_submission
