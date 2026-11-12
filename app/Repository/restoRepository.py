from datetime import datetime, timezone
from uuid import UUID, uuid4

from passlib.context import CryptContext
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, SQLModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Resto(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4),
    )
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    resto_name: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    email: str = Field(unique=True, index=True)
    password: str = Field(nullable=False)
    tel: str | None = Field(default=None, nullable=True)

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        resto_name: str,
        password: str,
        tel: str | None,
    ) -> "Resto":
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            resto_name=resto_name,
            password=pwd_context.hash(password),
            tel=tel,
        )
