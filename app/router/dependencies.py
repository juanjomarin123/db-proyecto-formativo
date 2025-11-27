# En esencia, este archivo es el guardián de la API, asegurando que solo los usuarios válidos y autenticados puedan acceder a los recursos protegidos

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.usuarios import get_user_by_email_security, get_user_by_id
from core.security import verify_password, verify_token
from core.database import get_db
from fastapi.security import OAuth2PasswordBearer

# Inicialización de OAuth2PasswordBearer, que define el esquema de seguridad OAuth2.
# tokenUrl indica la URL donde el cliente debe enviar las credenciales para obtener el token.
# auto_error=False permite que Swagger y clientes sin token carguen la UI sin quedarse colgados
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/access/token",
    auto_error=False  # Permite que token sea None si no se envía
)


# Función de dependencia para obtener el usuario actual a partir de un token JWT
# Esta función se utiliza en las rutas protegidas para garantizar que el usuario esté autenticado y activo.
def get_current_user(
    token: str = Depends(oauth2_scheme),  # Dependencia que extrae el token de la cabecera 'Authorization'
    db: Session = Depends(get_db)        # Dependencia para obtener la sesión de la base de datos
):
    # 1. Verifica si se envió un token
    if token is None:
        # Lanza una excepción 401 (Unauthorized) indicando que se requiere token
        raise HTTPException(status_code=401, detail="Token requerido")

    # 2. Verifica la validez del token (firma, expiración, etc.) y extrae el ID del usuario
    user_id = verify_token(token)
    # Si la verificación falla (el token es inválido o expiró)
    if user_id is None:
        # Lanza una excepción 401 (Unauthorized) indicando token inválido
        raise HTTPException(status_code=401, detail="Token inválido")

    # 3. Busca el usuario en la base de datos usando el ID extraído del token
    user_db = get_user_by_id(db, user_id)
    # Si el usuario no existe en la BD (ej. fue eliminado)
    if user_db is None:
        # Lanza una excepción 404 (Not Found)
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 4. Verifica si el usuario está activo (su estado es True)
    if not user_db.estado:
        # Lanza una excepción 403 (Forbidden) si el usuario está inactivo
        raise HTTPException(status_code=403, detail="Usuario inactivo. No autorizado")

    # Retorna el objeto usuario de la base de datos si pasa todas las verificaciones
    return user_db


# Función para autenticar un usuario mediante su nombre de usuario (correo) y contraseña
# Esta función es típicamente usada durante el proceso de login para generar el token.
def authenticate_user(username: str, password: str, db: Session):
    # 1. Busca el usuario en la BD por su nombre de usuario (correo electrónico)
    user = get_user_by_email_security(db, username)
    # Si no se encuentra el usuario
    if not user:
        return False

    # 2. Verifica la contraseña proporcionada con la contraseña encriptada almacenada en la BD
    # 'contra_encript' es el campo que contiene el hash de la contraseña
    if not verify_password(password, user.contra_encript):
        return False

    # Si la autenticación es exitosa, retorna el objeto usuario
    return user
