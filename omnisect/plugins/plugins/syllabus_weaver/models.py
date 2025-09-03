from typing import Literal, Self

from pydantic import BaseModel, model_validator


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

    course_content: list[CourseContentWeek]
    course_content_contact_hours_total: int
    course_content_sss_total: int

    course_required_literature: list[str]
    course_recommended_literature: list[str]
    course_internet_sources: list[str]
    course_other_sources: list[str]

    course_languages: list[
        Literal["Kazakh language", "English language", "Russian language"]
    ]

    course_assessment_methods_isc_1: list[AssessmentMethod]
    course_assessment_methods_isc_2: list[AssessmentMethod]

    course_assessment_final_exam_topic: str
    course_assessment_final_exam_form: str

    # --- Валидация бизнес-правил ---
    @model_validator(mode="after")
    def validate_weeks(self) -> Self:
        if len(self.course_content) != 15:
            raise ValueError("Course must have exactly 15 weeks of content")
        return self

    @model_validator(mode="after")
    def validate_contact_hours(self) -> Self:
        total = sum(w.contract_hours for w in self.course_content)
        if self.course_content_contact_hours_total != total:
            raise ValueError(f"contact_hours_total must equal {total}")
        return self

    @model_validator(mode="after")
    def validate_sss(self) -> Self:
        total = sum(w.sss for w in self.course_content)
        if self.course_content_sss_total != total:
            raise ValueError(f"sss_total must equal {total}")
        return self

    @model_validator(mode="after")
    def validate_assessment1(self):
        total = sum(item.weight for item in self.course_assessment_methods_isc_1)
        if total != 100:
            raise ValueError(f"ISC1 weights must sum to 100, got {total}")
        return self

    @model_validator(mode="after")
    def validate_assessment2(self, v):
        total = sum(item.weight for item in self.course_assessment_methods_isc_2)
        if total != 100:
            raise ValueError(f"ISC2 weights must sum to 100, got {total}")
        return v
