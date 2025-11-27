
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging  

from app.schemas.programas_formacion import CrearProgramaFormacion, RetornoProgramaFormacion, EditarProgramaFormacion 
# Importas los schemas (modelos Pydantic) que usas: para crear usuario, editar usuario, cambiar contraseña, y retornar usuario

# Creas un logger específico para este módulo, con su nombre
logger = logging.getLogger(__name__)


def crear_programa(db: Session, programa: CrearProgramaFormacion) -> Optional[bool]: #Crea un usuario en la base de datos usando los datos del schema CrearUsuario.
    try:
        # Convierte el objeto Pydantic (CrearUsuario) a un dict de Python
        dataUser = programa.model_dump()
        # Define la consulta SQL para insertar el usuario
        query = text("""
            INSERT INTO Programas_formacion (version,nombre,nivel,id_red,tiempo_dur,unidad_dur,estado,url_pdf
            )VALUES (:version,:nombre,:nivel,:id_red,:tiempo_dur,:unidad_dur,:estado,:url_pdf)
        """)

        # Ejecuta la consulta con los datos del usuario
        db.execute(query, dataUser)
        # Hace commit para guardar los cambios en la base de datos
        db.commit()

        return True  # Si todo sale bien, retorna True
    except Exception as e:
        # Si algo falla, deshace la transacción
        db.rollback()
        # Registra el error en el logger
        logger.error(f"Error al crear usuario: {e}")
        # Lanza una excepción genérica con un mensaje más amigable
        raise Exception("Error de base de datos al crear el usuario")
    



def get_programaFormacion_by_codPrograma(db: Session, id_programa_formacion: int): #Busca un usuario por su ID y retorna sus datos junto con el nombre del rol.
    try:
        query = text("""
            SELECT 
                pf.cod_programa,pf.version,pf.nombre,pf.nivel,pf.id_red,pf.tiempo_dur,pf.unidad_dur,
                pf.estado,pf.url_pdf,rc.nombre AS nombre_red
            FROM Programas_formacion pf
            LEFT JOIN Redes_conocimiento rc 
                ON pf.id_red = rc.id_red
            WHERE pf.cod_programa = :cod_programa
        """)

        # Ejecuta la consulta, mapea resultados y toma el primero (o None si no existe)
        result = db.execute(query, {"cod_programa": id_programa_formacion}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar programa de formacion por id: {e}")
        raise Exception("Error de base de datos al buscar el programa")
    


def get_programaFormacion_by_id_red(db: Session, id_red: int): # Busca un usuario por correo (sin traer la contraseña).
    try:
        query = text("""
            SELECT 
                pf.cod_programa,pf.version,pf.nombre,pf.nivel,pf.id_red,pf.tiempo_dur,pf.unidad_dur,
                pf.estado,pf.url_pdf,
                rc.nombre AS nombre_red
            FROM Programas_formacion pf
            INNER JOIN Redes_conocimiento rc
                ON pf.id_red = rc.id_red
            WHERE pf.id_red = :id_red
        """)

        result = db.execute(query, {"id_red": id_red}).mappings().first() #convierte el resultado en un diccionario y luego toma la primera fila.
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar Programa de Formacion por id_red: {e}")
        raise Exception("Error de base de datos el Programa de Formacion por id de red")
    


def programaFormacion_delete(db: Session, cod_programa: int) -> bool:
    try:
        # Consulta SQL para eliminar un programa por su clave primaria
        query = text("""
            DELETE FROM Programas_formacion
            WHERE cod_programa = :cod_programa
        """)

        # Ejecuta la consulta con el ID recibido
        result = db.execute(query, {"cod_programa": cod_programa})
        
        # Si no se afectó ninguna fila, el programa no existe
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

        # Guarda los cambios en la base de datos
        db.commit()
        return True

    except SQLAlchemyError as e:
        # Reversa la transacción si ocurre un error
        db.rollback()
        logger.error(f"Error al eliminar programa: {e}")
        # Lanza un error genérico para el cliente
        raise Exception("Error de base de datos al eliminar el programa")





def update_programaFormacion(
    db: Session, cod_programa: int, programa_update: EditarProgramaFormacion) -> bool:
    try:
        # Convierte el esquema Pydantic en un diccionario,
        # ignorando los campos que no fueron enviados por el cliente
        data = programa_update.model_dump(exclude_unset=True)

        # Si no se enviaron campos para actualizar, arrojar un error
        if not data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        # Construye dinámicamente la parte del SET:
        # ejemplo => "nombre = :nombre, nivel = :nivel, estado = :estado"
        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])

        # Agrega el ID del programa al diccionario de parámetros
        data["cod_programa"] = cod_programa

        # Consulta SQL completa para realizar la actualización
        query = text(f"""
            UPDATE Programas_formacion
            SET {set_clause}
            WHERE cod_programa = :cod_programa
        """)

        # Ejecuta la actualización
        result = db.execute(query, data)

        # Si no se modificó ninguna fila, el programa no existe
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

        # Guarda los cambios en la base de datos
        db.commit()
        return True

    except SQLAlchemyError as e:
        # Deshace la transacción si ocurre un error
        db.rollback()
        logger.error(f"Error al actualizar programa: {e}")
        raise Exception("Error de base de datos al actualizar programa")

