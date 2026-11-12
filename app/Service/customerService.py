import random
from app.Repository.customerRepository import Customer
from app.Dto.customerDto import CustomerRegister
from sqlmodel import Session, select
from passlib.context import CryptContext
from db.database import engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_customer(user_data: CustomerRegister) -> dict:

    with Session(engine) as db:

        statement = select(Customer).where(Customer.email == user_data.email)
        existing_customer = db.exec(statement).first()

        if existing_customer:
            return {"message": "Email already registered", "status_code": 409}

        new_customer = Customer.create(
            first_name=user_data.first_name, 
            last_name=user_data.last_name, 
            email=user_data.email, 
            password=user_data.password, 
            tel=user_data.tel
            )

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return {"message": "Customer registered successfully", "status_code": 200}