from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging 
from sqlalchemy import text
from typing import Optional

from app.schemas.registro_calificado import CrearRegistroCalificado, RetornoRegistroCalificado, EditarRegistroCalificado

logger = logging.getLogger(__name__)

def crear_registro_calificado(db: Session, registro: CrearRegistroCalificado) -> Optional[bool]:
    try:
        dataRegistro = registro.model_dump()

        query = text("""
            INSERT INTO Registro_calificado(
                     cod_programa,
                     tipo_tramite,
                     fecha_radicado,
                     numero_resolucion,
                     fecha_resolucion,
                     fecha_vencimiento,
                     vigencia,
                     modalidad,
                     clasificacion,
                     estado_catalogo
                     ) VALUES(
                     :cod_programa,
                     :tipo_tramite,
                     :fecha_radicado,
                     :numero_resolucion,
                     :fecha_resolucion,
                     :fecha_vencimiento,
                     :vigencia,
                     :modalidad,
                     :clasificacion,
                     :estado_catalogo
            )
        """)
        db.execute(query,dataRegistro)
        db.commit()
        return True     
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear registro calificado: {e}")
        raise Exception("Error de base de datos al crear el registro calificado")
    





def get_registro_by_cod_programa(db: Session, cod_programa: int):
    try:
        query = text("""
            SELECT 
                cod_programa,
                tipo_tramite,
                fecha_radicado,
                numero_resolucion,
                fecha_resolucion,
                fecha_vencimiento,
                vigencia,
                modalidad,
                clasificacion,
                estado_catalogo
            FROM Registro_calificado
            WHERE cod_programa = :cod_programa
        """)

        result = db.execute(query, {"cod_programa": cod_programa}).mappings().first()

        if result is None:
            raise HTTPException(status_code=404, detail="No existe el registro calificado")

        return dict(result)

    except HTTPException:
        # Re-lanzar HTTPException para que se propague correctamente
        raise
    except Exception as e:
        logger.error(f"Error al obtener el registro calificado: {e}")
        raise Exception("Error de base de datos al obtener el registro calificado")
    





def get_todo_by_cod_programa(db: Session, cod_programa: int):
    try:
        # Se construye una consulta SQL cruda usando text()
        query = text("""
            SELECT 
                cod_programa,
                tipo_tramite,
                fecha_radicado,
                numero_resolucion,
                fecha_resolucion,
                fecha_vencimiento,
                vigencia,
                modalidad,
                clasificacion,
                estado_catalogo
            FROM Registro_calificado
            WHERE cod_programa = :cod_programa
        """)

        # Se ejecuta la consulta pasando el parámetro cod_programa
        # .mappings() transforma cada fila en un diccionario-like
        # .all() devuelve todas las coincidencias
        results = db.execute(query, {"cod_programa": cod_programa}).mappings().all()

        # Si no se encontraron filas, se lanza un error 404
        if not results:
            raise HTTPException(status_code=404, detail="No existen registros para este cod_programa")

        # Se convierten los resultados a una lista de diccionarios estándar
        return [dict(result) for result in results]

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        # Se captura cualquier error de base de datos y se relanza con un mensaje claro
        raise Exception(f"Error de base de datos: {e}")






def get_todos_registros_calificados(db: Session):
    try:
        query = text("""
            SELECT 
                cod_programa,
                tipo_tramite,
                fecha_radicado,
                numero_resolucion,
                fecha_resolucion,
                fecha_vencimiento,
                vigencia,
                modalidad,
                clasificacion,
                estado_catalogo
            FROM Registro_calificado
        """)

        results = db.execute(query).mappings().all()

        return [dict(result) for result in results]

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todos los registros calificados: {e}")
        raise Exception("Error de base de datos al obtener todos los registros calificados")

    




def update_registro_calificado(db: Session, cod_programa: int, registro: EditarRegistroCalificado) -> Optional[bool]:
    try:
        dataRegistro = registro.model_dump(exclude_unset=True)
        
        # Construir dinámicamente la parte SET de la consulta SQL
        set_clause = ", ".join([f"{key} = :{key}" for key in dataRegistro.keys()])
        
        query = text(f"""
            UPDATE Registro_calificado
            SET {set_clause}
            WHERE cod_programa = :cod_programa
        """)
        
        # Agregar cod_programa a los parámetros
        dataRegistro["cod_programa"] = cod_programa
        
        result = db.execute(query, dataRegistro)
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Registro calificado no encontrado")
        
        db.commit()
        return True

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar el registro calificado: {e}")
        raise Exception("Error de base de datos al actualizar el registro calificado")
    






def delete_registro_calificado(db: Session, cod_programa: int) -> Optional[bool]:
    try:
        query = text("""
            DELETE FROM Registro_calificado
            WHERE cod_programa = :cod_programa
        """)
        
        result = db.execute(query, {"cod_programa": cod_programa})
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Registro calificado no encontrado")
        
        db.commit()
        return True

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar el registro calificado: {e}")
        raise Exception("Error de base de datos al eliminar el registro calificado")




