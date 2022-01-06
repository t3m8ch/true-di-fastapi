from sqlalchemy import Integer, Column, Unicode, Boolean
from sqlalchemy.sql import expression

from ..model_base import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    text = Column(Unicode(200), nullable=False)
    is_completed = Column(Boolean, nullable=False, server_default=expression.false())
