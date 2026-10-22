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

from ..models.ea_trial_figure_grade_type_1 import EaTrialFigureGradeType1
from ..models.ea_trial_figure_grade_type_2_type_1 import EaTrialFigureGradeType2Type1
from ..models.ea_trial_figure_grade_type_3_type_1 import EaTrialFigureGradeType3Type1
from ..models.ea_trial_figure_key import EaTrialFigureKey
from ..types import UNSET, Unset

T = TypeVar("T", bound="EaTrialFigure")


@_attrs_define
class EaTrialFigure:
    """One thing a trial measured, with the platform's grade. Show `display` in the colour of `grade` and work nothing out
    yourself.

        Attributes:
            key (EaTrialFigureKey):
            label (str): e.g. Processor, worst minute
            value (Union[None, float]): Null until the cell has reported it. While the trial runs, the figure so far
            display (Union[None, str]): The value as the page shows it, e.g. "41 % of its cap" or "every time"
            grade (Union[EaTrialFigureGradeType1, EaTrialFigureGradeType2Type1, EaTrialFigureGradeType3Type1, None]):
                Against the trial line in force when it was judged; null while there is no value, and while the trial runs
    """

    key: EaTrialFigureKey
    label: str
    value: Union[None, float]
    display: Union[None, str]
    grade: Union[
        EaTrialFigureGradeType1, EaTrialFigureGradeType2Type1, EaTrialFigureGradeType3Type1, None
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key.value

        label = self.label

        value: Union[None, float]
        value = self.value

        display: Union[None, str]
        display = self.display

        grade: Union[None, str]
        if isinstance(self.grade, EaTrialFigureGradeType1):
            grade = self.grade.value
        elif isinstance(self.grade, EaTrialFigureGradeType2Type1):
            grade = self.grade.value
        elif isinstance(self.grade, EaTrialFigureGradeType3Type1):
            grade = self.grade.value
        else:
            grade = self.grade

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "label": label,
                "value": value,
                "display": display,
                "grade": grade,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = EaTrialFigureKey(d.pop("key"))

        label = d.pop("label")

        def _parse_value(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        value = _parse_value(d.pop("value"))

        def _parse_display(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        display = _parse_display(d.pop("display"))

        def _parse_grade(
            data: object,
        ) -> Union[
            EaTrialFigureGradeType1,
            EaTrialFigureGradeType2Type1,
            EaTrialFigureGradeType3Type1,
            None,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grade_type_1 = EaTrialFigureGradeType1(data)

                return grade_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grade_type_2_type_1 = EaTrialFigureGradeType2Type1(data)

                return grade_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grade_type_3_type_1 = EaTrialFigureGradeType3Type1(data)

                return grade_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    EaTrialFigureGradeType1,
                    EaTrialFigureGradeType2Type1,
                    EaTrialFigureGradeType3Type1,
                    None,
                ],
                data,
            )

        grade = _parse_grade(d.pop("grade"))

        ea_trial_figure = cls(
            key=key,
            label=label,
            value=value,
            display=display,
            grade=grade,
        )

        ea_trial_figure.additional_properties = d
        return ea_trial_figure

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
