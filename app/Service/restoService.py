from sqlmodel import Session, select

from app.Dto.restoDto import RestoRegister
from app.Repository.restoRepository import Resto
from db.database import engine


def register_resto(user_data: RestoRegister) -> dict:
    with Session(engine) as db:
        statement = select(Resto).where(Resto.email == user_data.email)
        existing_resto = db.exec(statement).first()

        if existing_resto:
            return {"message": "Email already registered", "status_code": 409}

        new_resto = Resto.create(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=str(user_data.email),
            resto_name=user_data.resto_name,
            password=user_data.password,
            tel=str(user_data.tel) if user_data.tel is not None else None,
        )

        db.add(new_resto)
        db.commit()
        db.refresh(new_resto)

        return {"message": "Restaurant registered successfully", "status_code": 200}
