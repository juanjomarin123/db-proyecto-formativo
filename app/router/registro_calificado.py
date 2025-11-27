from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.router.dependencies import get_current_user
from app.schemas.registro_calificado import CrearRegistroCalificado, EditarRegistroCalificado, RetornoRegistroCalificado
from app.schemas.usuarios import RetornoUsuario

from core.database import get_db
from app.crud import registro_calificado


# Creación de una instancia de APIRouter para definir las rutas de la API relacionadas con usuarios.
router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
# Función para crear un usuario.
# Recibe los datos del usuario a crear (CrearUsuario), la sesión de BD y el usuario del token (para verificación de permisos).
def crear_RegistroCalificado(
    registro: CrearRegistroCalificado,
    db: Session = Depends(get_db),  # Dependencia para obtener la sesión de la base de datos.
    user_token: RetornoUsuario = Depends(get_current_user)  # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede crear usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para crear un Registro Calificado")
        
        # Llama a la función CRUD para crear el usuario en la base de datos.
        crear = registro_calificado.crear_registro_calificado(db, registro)
        
        # Verifica si la creación fue exitosa.
        if crear:
            return {"message": "Registro Calificado creado correctamente"}
        else:
            return {"message": "El Registro Calificado no pudo ser creado correctamente"}
    
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    
    # Captura cualquier excepción que ocurra durante el proceso (ej. errores de validación, BD, etc.).
    except Exception as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))

    


# --- Ruta para obtener un usuario por su ID ---
@router.get("/obtener-por-cod_programa/{cod_programa}", status_code=status.HTTP_200_OK, response_model=RetornoRegistroCalificado)
# Función para obtener un usuario por ID.
# Recibe el ID del usuario como parámetro de ruta y la sesión de BD.
def get_registroCalificado_by_cod(
    cod_programa: int,
    db: Session = Depends(get_db)
):
    try:  
        # Llama a la función CRUD para buscar el registro por su cod_programa.
        registro = registro_calificado.get_registro_by_cod_programa(db, cod_programa)
        return registro
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))
    




@router.get("/obtener-todos", status_code=status.HTTP_200_OK, response_model=list[RetornoRegistroCalificado])
# Función para obtener todos los usuarios.
def get_todos_registrosCalificados(
    db: Session = Depends(get_db)
):
    try:
        # Llama a la función CRUD para obtener todos los registros calificados.
        registros = registro_calificado.get_todos_registros_calificados(db)
        return registros
    except SQLAlchemyError as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))





# --- Ruta para editar un usuario ---
@router.put("/editar/{cod_programa}", status_code=status.HTTP_200_OK)
# Función para editar un usuario.
# Recibe el ID del usuario a editar, los datos a actualizar (EditarUsuario), la sesión de BD y el usuario del token (para verificación de permisos).
def editar_registroCalificado(
    cod_programa: int,
    registro: EditarRegistroCalificado,
    db: Session = Depends(get_db), # Dependencia para obtener la sesión de la base de datos.
    user_token: RetornoUsuario = Depends(get_current_user) # Dependencia para obtener la información del usuario autenticado.
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede editar usuarios.
        if user_token.id_rol != 1:
            # Lanza una excepción 401 (No autorizado) si el usuario no tiene permisos.
            raise HTTPException(status_code=401, detail="No tienes permisos para editar un Registro Calificado")
        
        # Llama a la función CRUD para editar el usuario en la base de datos.
        editar = registro_calificado.update_registro_calificado(db, cod_programa, registro)
        # Verifica si la edición fue exitosa.
        if editar:
            return {"message": "Registro Calificado editado correctamente"}
        else:
            return {"message": "El Registro Calificado no pudo ser editado correctamente"}
    
    # Re-lanzar HTTPException para que se propague correctamente
    except HTTPException:
        raise
    # Captura cualquier excepción que ocurra durante el proceso (ej. errores de validación, BD, etc.).
    except Exception as e:
        # Lanza una excepción HTTP 500 (Error interno del servidor) con el detalle del error.
        raise HTTPException(status_code=500, detail=str(e))
    



    


@router.delete("/eliminar/{cod_programa}", status_code=status.HTTP_200_OK)
# Función para eliminar un usuario.
def eliminar_registroCalificado(
    cod_programa: int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        # **Lógica de verificación de permisos**: Solo el usuario con id_rol = 1 (ej. Administrador) puede eliminar usuarios.
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar un Registro Calificado")
        
        eliminar = registro_calificado.delete_registro_calificado(db, cod_programa)
        if eliminar:
            return {"message": "Registro Calificado eliminado correctamente"}
        else:
            return {"message": "El Registro Calificado no pudo ser eliminado correctamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    




