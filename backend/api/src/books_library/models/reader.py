from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base

class Reader(Base):

    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship(back_populates="reader")