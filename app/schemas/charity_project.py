from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1

    @validator("name")
    def name_cant_be_none(cls, value):
        if value is None:
            raise ValueError("Название проекта не может быть пустым!")
        return value

    @validator("description")
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("Описание проекта не может быть пустым!")
        return value

    @validator("full_amount")
    def check_full_amount(cls, value, values):
        if value is None:
            raise ValueError("Поле с требуемой суммой не может быть пустым!")
        if (
            "invested_amount" in values and
            values["invested_amount"] is not None
        ):
            if value < values["invested_amount"]:
                raise ValueError("Сумма не может быть меньше уже вложенной!")
        return value


class CharityProjectUpdate(CharityProjectBase):
    pass
