import datetime

from sqlalchemy import TIMESTAMP, BigInteger, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column


class DbModel:
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    version_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_date: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_date: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
    )

    __table_args__ = {"schema": "app"}
    __mapped_args__ = {"version_id_col": version_id}

    @classmethod
    def get_table_args(cls) -> dict:
        return {"schema": "app"}


class HasAuthor:
    author_id: Mapped[str] = mapped_column(String(256), nullable=False)
    author_username: Mapped[str] = mapped_column(String(256), nullable=False)


class HasWebId:
    web_id: Mapped[str] = mapped_column(String[32], unique=True, nullable=False)
