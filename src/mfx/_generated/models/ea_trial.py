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

from ..models.ea_colour import EaColour
from ..models.ea_trial_state import EaTrialState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_trial_figure import EaTrialFigure


T = TypeVar("T", bound="EaTrial")


@_attrs_define
class EaTrial:
    """A trial with trading off on one terminal

    Attributes:
        state (EaTrialState):
        started_at (datetime.datetime):
        ended_at (Union[None, datetime.datetime]):
        minutes (int): The trial length in force when it started
        verdict (Union[EaColour, None]): Null while it runs, and for a trial that ended before it was judged (you
            detached the expert during it)
        figures (list['EaTrialFigure']): Always the seven, in the order of `key`'s values: the figures so far while it
            runs, the judged ones once it has ended
    """

    state: EaTrialState
    started_at: datetime.datetime
    ended_at: Union[None, datetime.datetime]
    minutes: int
    verdict: Union[EaColour, None]
    figures: list["EaTrialFigure"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_trial_figure import EaTrialFigure

        state = self.state.value

        started_at = self.started_at.isoformat()

        ended_at: Union[None, str]
        if isinstance(self.ended_at, datetime.datetime):
            ended_at = self.ended_at.isoformat()
        else:
            ended_at = self.ended_at

        minutes = self.minutes

        verdict: Union[None, str]
        if isinstance(self.verdict, EaColour):
            verdict = self.verdict.value
        else:
            verdict = self.verdict

        figures = []
        for figures_item_data in self.figures:
            figures_item = figures_item_data.to_dict()
            figures.append(figures_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "started_at": started_at,
                "ended_at": ended_at,
                "minutes": minutes,
                "verdict": verdict,
                "figures": figures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_trial_figure import EaTrialFigure

        d = dict(src_dict)
        state = EaTrialState(d.pop("state"))

        started_at = isoparse(d.pop("started_at"))

        def _parse_ended_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ended_at_type_0 = isoparse(data)

                return ended_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        ended_at = _parse_ended_at(d.pop("ended_at"))

        minutes = d.pop("minutes")

        def _parse_verdict(data: object) -> Union[EaColour, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                verdict_type_0 = EaColour(data)

                return verdict_type_0
            except:  # noqa: E722
                pass
            return cast(Union[EaColour, None], data)

        verdict = _parse_verdict(d.pop("verdict"))

        figures = []
        _figures = d.pop("figures")
        for figures_item_data in _figures:
            figures_item = EaTrialFigure.from_dict(figures_item_data)

            figures.append(figures_item)

        ea_trial = cls(
            state=state,
            started_at=started_at,
            ended_at=ended_at,
            minutes=minutes,
            verdict=verdict,
            figures=figures,
        )

        ea_trial.additional_properties = d
        return ea_trial

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
