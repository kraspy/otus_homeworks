from sqlalchemy import Identity, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
