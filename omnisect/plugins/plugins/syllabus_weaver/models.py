from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator


class Teacher(BaseModel):
    title: str
    fullname: str
    email: str


class CourseContentWeek(BaseModel):
    week: int
    topic: str
    contract_hours: int
    sss: int


class AssessmentMethod(BaseModel):
    week: int
    title: str
    topic: str
    form: str
    points: int
    weight: int


class CourseContext(BaseModel):
    teacher_name: str
    university_name: Literal["narxoz"] = Field(
        default="narxoz"
    )  # add other universities here
    course_title: str
    course_code: str
    course_type: Literal["Compulsory", "Elective"]
    course_level: Literal["Bachelor - first cycle", "Master - second cycle"]
    course_academic_year: int
    course_semester: Literal["Fall", "Spring"]
    course_credits: Literal[5, 6]

    course_teachers: list[Teacher]

    course_outcomes: str
    course_prerequisites: str

    course_content: list[CourseContentWeek] | None
    course_content_contact_hours_total: int = Field(45)
    course_content_sss_total: int = Field(60)

    course_required_literature: list[str]
    course_recommended_literature: list[str]
    course_internet_sources: list[str]
    course_other_sources: list[str]

    course_languages: list[
        Literal["Kazakh language", "English language", "Russian language"]
    ]

    course_assessment_methods_isc_1: list[AssessmentMethod] | None
    course_assessment_methods_isc_2: list[AssessmentMethod] | None

    course_assessment_final_exam_topic: str
    course_assessment_final_exam_form: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Do things after Pydantic validation
        if self.course_content is not None:
            for i in range(len(self.course_content)):
                # contract_hours must be 3 or 4 depending on number of credits
                self.course_content[i].contract_hours = (
                    3 if self.course_credits == 5 else 4
                )
                # sss must be 5 or 6 depending on number of credits
                self.course_content[i].sss = 5 if self.course_credits == 5 else 6
            self.course_content_contact_hours_total = sum(
                item.contract_hours for item in self.course_content
            )
            self.course_content_sss_total = sum(
                item.sss for item in self.course_content
            )

    # --- Валидация бизнес-правил ---
    @model_validator(mode="after")
    def validate_weeks(self) -> Self:
        if self.course_content is None:
            return self
        if len(self.course_content) != 15:
            raise ValueError("Course must have exactly 15 weeks of content")
        return self

    @model_validator(mode="after")
    def validate_assessment1(self):
        if self.course_assessment_methods_isc_1 is None:
            return self
        total = sum(item.weight for item in self.course_assessment_methods_isc_1)
        if total != 100:
            raise ValueError(f"ISC1 weights must sum to 100, got {total}")
        return self

    @model_validator(mode="after")
    def validate_assessment2(self, v):
        if self.course_assessment_methods_isc_2 is None:
            return self
        total = sum(item.weight for item in self.course_assessment_methods_isc_2)
        if total != 100:
            raise ValueError(f"ISC2 weights must sum to 100, got {total}")
        return v
