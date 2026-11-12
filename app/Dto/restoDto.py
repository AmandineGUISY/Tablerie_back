import re
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

class FrenchPhone(PhoneNumber):
    default_region_code = "FR"
    phone_format = "E164"

class RestoRegister(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr 
    tel: FrenchPhone | None = None
    resto_name: str
    password: str = Field(min_length=12)

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v):
        if not re.search(r"[A-Z]", v): raise ValueError('Le mot de passe doit contenir au moins une majuscule')
        if not re.search(r"[a-z]", v): raise ValueError('Le mot de passe doit contenir au moins une minuscule')
        if not re.search(r"\d", v): raise ValueError('Le mot de passe doit contenir au moins un chiffre')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v): raise ValueError('Le mot de passe doit contenir au moins un caractère spécial')
        return v