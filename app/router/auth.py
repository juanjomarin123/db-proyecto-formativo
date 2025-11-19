from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.router.dependencies import authenticate_user
from app.schemas.auth import ResponseLoggin
from app.schemas.usuarios import RetornoUsuario
from core.security import create_access_token
from core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/token", response_model=ResponseLoggin)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    print("📌 Llegó a /token")
    print("usuario recibido:", form_data.username)
    print("password recibido:", form_data.password)

    user = authenticate_user(db, form_data.username, form_data.password)

    print("Resultado authenticate_user:", user)

    if not user:
        print("❌ No pasó autenticación")
        raise HTTPException(
            status_code=401,
            detail="Datos Incorrectos en email o password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id_usuario), "rol": user.id_rol}
    )
    print("TOKEN CREADO:", access_token)

    return ResponseLoggin(
        user=RetornoUsuario.model_validate(user, from_attributes=True),
        access_token=access_token
    )


