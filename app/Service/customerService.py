from app.Repository.customerRepository import Customer
from app.Dto.customerDto import CustomerRegister
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import timedelta
from db.database import engine
from app.Service.tokenService import create_access_token

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


def authenticate_customer(email: str, password: str) -> dict | None:
    customer = get_customer_by_email(email)
    if not customer or not pwd_context.verify(password, customer.password):
        return None

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(customer.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

def get_customer_by_email(email: str) -> Customer | None:
    with Session(engine) as db:
        statement = select(Customer).where(Customer.email == email)
        customer = db.exec(statement).first()
        return customer