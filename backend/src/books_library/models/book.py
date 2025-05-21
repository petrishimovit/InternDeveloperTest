from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base


class Book(Base):

    
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    author: Mapped[str] = mapped_column(String, nullable=False)

    publication_year: Mapped[int | None] = mapped_column(nullable=True)

    isbn: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)

    copies: Mapped[int] = mapped_column(default=1)


    reader_id: Mapped[int | None] = mapped_column(ForeignKey("readers.id"), nullable=True)

    reader: Mapped["Reader | None"] = relationship(back_populates="books")



    