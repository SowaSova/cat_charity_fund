from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: int = None
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
