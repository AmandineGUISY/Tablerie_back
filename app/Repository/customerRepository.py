from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Customer(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    )
    first_name:str = Field(index=True)
    last_name:str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    email:str = Field(unique=True, index=True)
    password:str = Field(nullable=False)
    tel: str | None = Field(default=None, nullable=True)

    @classmethod 
    def create(cls, first_name:str, last_name:str , email:str, password:str, tel:str | None) -> "Customer":
        return cls (
            first_name = first_name,
            last_name = last_name,
            email = email,
            password=pwd_context.hash(password),
            tel=tel
        )