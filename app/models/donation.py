from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import AbstractBase


class Donation(AbstractBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))
