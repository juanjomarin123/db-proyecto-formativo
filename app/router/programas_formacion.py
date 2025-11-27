# Definir todas las rutas (endpoints) necesarias para realizar las operaciones básicas de CRUD
# (Crear, Leer, Actualizar y Eliminar) sobre la entidad Usuario


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.router.dependencies import get_current_user
from app.schemas.programas_formacion import CrearProgramaFormacion, EditarProgramaFormacion, RetornoProgramaFormacion
from app.schemas.usuarios import RetornoUsuario
from core.database import get_db
from app.crud import programas_formacion as crud_programaFormacion


# Creación de una instancia de APIRouter para definir las rutas de la API relacionadas con usuarios.
router = APIRouter()


# Ruta para el registro de un nuevo usuario 
@router.post("/registrar", status_code=status.HTTP_201_CREATED)
# Función para crear un usuario.
# Recibe los datos del usuario a crear (CrearUsuario), la sesión de BD y el usuario del token (para verificación de permisos).
def crear_programaFormacion(
    programa: CrearProgramaFormacion,
    db: Session = Depends(get_db), # Dependencia para obtener la sesión de la base de datos.
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para crear un Programa de Formación")
        
        # Llama a la función CRUD para crear el usuario en la base de datos.
        crear = crud_programaFormacion.crear_programa(db, programa)
        # Verifica si la creación fue exitosa.
        if crear:
            return {"message": "Programa creado correctamente"}
        else:
            return {"message": "El programa no pudo ser creado correctamente"}
    
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura cualquier excepción que ocurra durante el proceso (ej. errores de validación, BD, etc.).
    except Exception as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))
    




# --- Ruta para obtener un usuario por su ID ---
@router.get("/obtener-por-cod/{cod_programa}", status_code=status.HTTP_200_OK, response_model=RetornoProgramaFormacion)
# Función para obtener un usuario por ID.
# Recibe el ID del usuario como parámetro de ruta y la sesión de BD.
def get_programa_by_codPrograma(
    cod_programa: int,
    db: Session = Depends(get_db),
):
    try:
            # Llama a la función CRUD para buscar el usuario por su ID.
        programa = crud_programaFormacion.get_programaFormacion_by_codPrograma(db, cod_programa)
        # Verifica si se encontró el usuario.
        if programa is None:
            # Lanza una excepción 404 (No encontrado) si el usuario no existe.
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        # Retorna el objeto usuario encontrado (serializado según RetornoUsuario).
        return programa
        # Captura errores específicos de SQLAlchemy (ej. problemas de conexión, sintaxis SQL).
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))
    




# --- Ruta para obtener un usuario por su correo electrónico ---
@router.get("/obtener-por-id_red/{id_red}", status_code=status.HTTP_200_OK, response_model=RetornoProgramaFormacion)
# Función para obtener un usuario por correo.
# Recibe el correo como parámetro de ruta y la sesión de BD.
def get_programa_by_id_red(
    id_red: int,
    db: Session = Depends(get_db),
):      
    try:
        # Llama a la función CRUD para buscar el usuario por correo electrónico.
        programa = crud_programaFormacion.get_programaFormacion_by_id_red(db, id_red)
        # Verifica si se encontró el usuario.
        if programa is None:
            # Lanza una excepción 404.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programa de formacion no encontrado")
        # Retorna el objeto usuario encontrado.
        return programa
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))
    




# --- Ruta para eliminar un usuario por su ID ---
@router.delete("/eliminar-por-cod/{cod_programa}", status_code=status.HTTP_200_OK)
# Función para eliminar un usuario.
# Recibe el ID del usuario a eliminar y la sesión de BD.
def delete_by_cod(
    cod_programa: int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar un programa")
        # Llama a la función CRUD para eliminar el usuario.
        programa = crud_programaFormacion.programaFormacion_delete(db, cod_programa)
        # Verifica si la eliminación fue exitosa (el CRUD debería retornar True si se eliminó).
        if programa:
            return {"message": "Programa eliminado correctamente"}
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))


# --- Ruta para actualizar la información de un usuario ---
@router.put("/editar/{cod_programa}")
# Función para actualizar datos de un usuario.
# Recibe el ID del usuario a actualizar, los datos a editar (EditarUsuario) y la sesión de BD.
def update_user(
    cod_programa: int,
    programa: EditarProgramaFormacion,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):    

    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para crear un Programa de Formacion")
        # Llama a la función CRUD para actualizar el usuario.
        success = crud_programaFormacion.update_programaFormacion(db, cod_programa, programa)
        # Verifica si la actualización fue exitosa.
        if not success:
            # Lanza una excepción 400 (Solicitud incorrecta) si no se pudo actualizar (ej. usuario no encontrado).
            raise HTTPException(status_code=400, detail="No se pudo actualizar el Programa de Formacion")
        return {"message": "Programa actualizado correctamente"}
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura errores de SQLAlchemy.
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500.
        raise HTTPException(status_code=500, detail=str(e))