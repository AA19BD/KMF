"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_model"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)


class BankStatement(Base):
    __tablename__ = "bank_statement"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user_model.id", ondelete="CASCADE"),
    )
    contract_number: Mapped[str] = mapped_column(Text, nullable=True)
    account_number: Mapped[str] = mapped_column(Text, nullable=True)
    card: Mapped[str] = mapped_column(Text, nullable=True)
    branch_of_the_bank: Mapped[str] = mapped_column(Text, nullable=True)
    main_currency: Mapped[str] = mapped_column(Text, nullable=True)
    period: Mapped[str] = mapped_column(Text, nullable=True)
    client_name: Mapped[str] = mapped_column(Text, nullable=True)
    transaction: Mapped[str] = mapped_column(Text, nullable=True)
    base64_bank_statement: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __str__(self):
        return f"BankStatement(id={self.id}, base64_bank_statement={self.base64_bank_statement}, contract_number={self.contract_number}, ...)"
