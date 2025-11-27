# Definir todas las rutas (endpoints) necesarias para realizar las operaciones básicas de CRUD
# (Crear, Leer, Actualizar y Eliminar) sobre la entidad Usuario


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.router.dependencies import get_current_user
from app.schemas.usuarios import CrearUsuario, EditarPass, EditarUsuario, RetornoUsuario
from core.database import get_db
from app.crud import usuarios as crud_users


# Creación de una instancia de APIRouter para definir las rutas de la API relacionadas con usuarios.
router = APIRouter()

#-----------------------------------------------------------------------------------------------------
# Endpoint sin segurdad para crear un usuario

#{
#  "nombre_completo": "Andres Felipe Moncayo Paez",
#  "id_rol": 1,
#  "correo": "admin@example.com",
#  "num_documento": "1092850345",
#  "contra_encript": "admin123",
#  "estado": true
#}

# @router.post("/registrar", status_code=status.HTTP_201_CREATED)
# def create_user(
#     user: CrearUsuario,
#     db: Session = Depends(get_db)  # Solo dejamos la BD
# ):
#     try:
#         # Crear usuario sin verificación de token ni rol
#         crear = crud_users.create_user(db, user)

#         if crear:
#             return {"message": "Usuario creado correctamente"}
#         else:
#             return {"message": "El Usuario no pudo ser creado correctamente"}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





# Ruta para el registro de un nuevo usuario 
@router.post("/registrar", status_code=status.HTTP_201_CREATED)
# Función para crear un usuario.
# Recibe los datos del usuario a crear (CrearUsuario), la sesión de BD y el usuario del token (para verificación de permisos).
def create_user(
    user: CrearUsuario,
    db: Session = Depends(get_db), # Dependencia para obtener la sesión de la base de datos.
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        # Llama a la función CRUD para crear el usuario en la base de datos.
        crear = crud_users.create_user(db, user)
        # Verifica si la creación fue exitosa.
        if crear:
            return {"message": "Usuario creado correctamente"}
        else:
            return {"message": "El Usuario no pudo ser creado correctamente"}
    
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura cualquier excepción que ocurra durante el proceso (ej. errores de validación, BD, etc.).
    except Exception as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------------------------





# --- Ruta para obtener un usuario por su ID ---
@router.get("/obtener-por-id/{id_usuario}", status_code=status.HTTP_200_OK, response_model=RetornoUsuario)
# Función para obtener un usuario por ID.
# Recibe el ID del usuario como parámetro de ruta y la sesión de BD.
def get_by_id(
    id_usuario: int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para obtener usuario")
        
        # Llama a la función CRUD para buscar el usuario por su ID.
        user = crud_users.get_user_by_id(db, id_usuario)
        # Verifica si se encontró el usuario.
        if user is None:
            # Lanza una excepción 404 (No encontrado) si el usuario no existe.
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        # Retorna el objeto usuario encontrado (serializado según RetornoUsuario).
        return user
        # Captura errores específicos de SQLAlchemy (ej. problemas de conexión, sintaxis SQL).
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))


# --- Ruta para obtener un usuario por su correo electrónico ---
@router.get("/obtener-por-correo/{correo}", status_code=status.HTTP_200_OK, response_model=RetornoUsuario)
# Función para obtener un usuario por correo.
# Recibe el correo como parámetro de ruta y la sesión de BD.
def get_by_email(
    correo:str,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)# Dependencia para obtener la información del usuario autenticado.
):      
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para obtener usuario por correo")
        # Llama a la función CRUD para buscar el usuario por correo electrónico.
        user = crud_users.get_user_by_email(db, correo)
        # Verifica si se encontró el usuario.
        if user is None:
            # Lanza una excepción 404.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        # Retorna el objeto usuario encontrado.
        return user
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))


# --- Ruta para eliminar un usuario por su ID ---
@router.delete("/eliminar-por-id/{id_usuario}", status_code=status.HTTP_200_OK)
# Función para eliminar un usuario.
# Recibe el ID del usuario a eliminar y la sesión de BD.
def delete_by_id(
    id_usuario: int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar un usuario")
        # Llama a la función CRUD para eliminar el usuario.
        user = crud_users.user_delete(db, id_usuario)
        # Verifica si la eliminación fue exitosa (el CRUD debería retornar True si se eliminó).
        if user:
            return {"message": "Usuario eliminado correctamente"}
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))


# --- Ruta para actualizar la información de un usuario ---
@router.put("/editar/{user_id}")
# Función para actualizar datos de un usuario.
# Recibe el ID del usuario a actualizar, los datos a editar (EditarUsuario) y la sesión de BD.
def update_user(
    user_id: int,
    user: EditarUsuario,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):    

    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para editar usuario")
        # Llama a la función CRUD para actualizar el usuario.
        success = crud_users.update_user(db, user_id, user)
        # Verifica si la actualización fue exitosa.
        if not success:
            # Lanza una excepción 400 (Solicitud incorrecta) si no se pudo actualizar (ej. usuario no encontrado).
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))


# --- Ruta para actualizar la contraseña de un usuario ---
@router.put("/editar-contrasenia")
# Función para actualizar la contraseña.
# Recibe el esquema con la contraseña actual, nueva contraseña y posiblemente el ID/correo (EditarPass).
def update_password(
    user: EditarPass,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para actualizar contraseña")
        # Primer paso: Llama a la función CRUD para verificar que la contraseña actual sea correcta.
        verificar = crud_users.verify_user_pass(db, user)
        # Si la verificación falla (la contraseña actual es incorrecta).
        if not verificar:
            # Lanza una excepción 400.
            raise HTTPException(status_code=400, detail="La contraseña actual no es igual a la enviada")

        # Segundo paso: Llama a la función CRUD para actualizar la contraseña en la base de datos.
        success = crud_users.update_password(db, user)
        # Verifica si la actualización de la contraseña fue exitosa.
        if not success:
            # Lanza una excepción 400 si no se pudo actualizar.
            raise HTTPException(status_code=400, detail="No se pudo actualizar la contraseña del usuario")
        return {"message": "Contraseña actualizada correctamente"}
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))





