from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.router.dependencies import get_current_user
from app.schemas.redes_conocimiento import CrearRedConocimiento, RetornoRedConocimiento, EditarRedConocimiento
from app.schemas.usuarios import RetornoUsuario

from core.database import get_db
from app.crud import redes_conocimiento as crud_redConocimiento


router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
# Función para crear un usuario.
# Recibe los datos del usuario a crear (CrearUsuario), la sesión de BD y el usuario del token (para verificación de permisos).
def crear_RedConocimiento(
    red: CrearRedConocimiento,
    db: Session = Depends(get_db), # Dependencia para obtener la sesión de la base de datos.
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para crear una Red de conocimiento")
        
        # Llama a la función CRUD para crear el usuario en la base de datos.
        crear = crud_redConocimiento.crear_RedConocimiento(db, red)
        # Verifica si la creación fue exitosa.
        if crear:
            return {"message": "Red de conocimiento creada correctamente"}
        else:
            return {"message": "La Red de conocimiento no pudo ser creado correctamente"}
    
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura cualquier excepción que ocurra durante el proceso (ej. errores de validación, BD, etc.).
    except Exception as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))



# --- Ruta para obtener un usuario por su ID ---
@router.get("/obtener-por-id/{id_red}", status_code=status.HTTP_200_OK, response_model=RetornoRedConocimiento)
# Función para obtener un usuario por ID.
# Recibe el ID del usuario como parámetro de ruta y la sesión de BD.
def get_by_id(
    id_red: int,
    db: Session = Depends(get_db)
):
    try:  
        # Llama a la función CRUD para buscar el usuario por su ID.
        red = crud_redConocimiento.get_red_by_id_red(db, id_red)
        # Verifica si se encontró el usuario.
        if red is None:
            # Lanza una excepción 404 (No encontrado) si el usuario no existe.
            raise HTTPException(status_code=404, detail="Red de conocimiento no encontrada")
        # Retorna el objeto usuario encontrado (serializado según RetornoUsuario).
        return red
        # Captura errores específicos de SQLAlchemy (ej. problemas de conexión, sintaxis SQL).
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/obtener-por-nombre/{nombre}", status_code=status.HTTP_200_OK, response_model=RetornoRedConocimiento)
# Función para obtener una red de conocimiento por nombre.
# Recibe el nombre como parámetro de ruta y la sesión de BD.
def get_by_nombre(
    nombre: str,
    db: Session = Depends(get_db)
):
    try:  
        # Llama a la función CRUD para buscar el usuario por su ID.
        red = crud_redConocimiento.get_red_by_nombre(db, nombre)
        # Verifica si se encontró el usuario.
        if red is None:
            # Lanza una excepción 404 (No encontrado) si el usuario no existe.
            raise HTTPException(status_code=404, detail="Red de conocimiento no encontrada")
        # Retorna el objeto usuario encontrado (serializado según RetornoUsuario).
        return red
        # Captura errores específicos de SQLAlchemy (ej. problemas de conexión, sintaxis SQL).
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))
    




@router.delete("/eliminar-por-id/{id_red}", status_code=status.HTTP_200_OK)
# Función para eliminar un usuario.
# Recibe el ID del usuario a eliminar y la sesión de BD.
def delete_by_id(
    id_red: int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar una red de conocimiento")
        # Llama a la función CRUD para eliminar el usuario.
        user = crud_redConocimiento.delete_red(db, id_red)
        # Verifica si la eliminación fue exitosa (el CRUD debería retornar True si se eliminó).
        if user:
            return {"message": "Red de conocimiento eliminada correctamente"}
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))
    



# --- Ruta para actualizar la información de un usuario ---
@router.put("/editar/{id_red}")
# Función para actualizar datos de un usuario.
# Recibe el ID del usuario a actualizar, los datos a editar (EditarUsuario) y la sesión de BD.
def update_red(
    id_red: int,
    red: EditarRedConocimiento,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):    

    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para actualizar una red de conocimiento")
        # Llama a la función CRUD para actualizar el usuario.
        success = crud_redConocimiento.update_red(db, id_red, red)
        # Verifica si la actualización fue exitosa.
        if not success:
            # Lanza una excepción 400 (Solicitud incorrecta) si no se pudo actualizar (ej. usuario no encontrado).
            raise HTTPException(status_code=400, detail="No se pudo actualizar la red de conocimiento")
        return {"message": "Red de conocimiento actualizada correctamente"}
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))