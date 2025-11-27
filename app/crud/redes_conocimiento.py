from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging 
from sqlalchemy import text
from typing import Optional

from app.schemas.redes_conocimiento import CrearRedConocimiento, RetornoRedConocimiento, EditarRedConocimiento

logger = logging.getLogger(__name__)





def crear_RedConocimiento(db: Session, red: CrearRedConocimiento) -> Optional[bool]:
    try:
        dataRed = red.model_dump()
        query = text("""
            INSERT INTO Redes_conocimiento(
                     nombre
                     ) VALUES(
                     :nombre
            )
        """)
        db.execute(query,dataRed)
        db.commit()
        return True     
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")
    


    
def get_red_by_id_red(db: Session, id_red: int):
    try:
        query = text("""
            SELECT 
                id_red,
                nombre
            FROM Redes_conocimiento
            WHERE id_red = :id_red
        """)

        result = db.execute(query, {"id_red": id_red}).mappings().first()

        if result is None:
            raise HTTPException(status_code=404, detail="No existe la red de conocimiento")

        return {
            "id_red": result["id_red"],
            "nombre": result["nombre"]
        }

    except HTTPException:
        # Re-lanzar HTTPException para que se propague correctamente
        raise
    except Exception as e:
        logger.error(f"Error al obtener la red por ID: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error al obtener la red de conocimiento"
        )
    



def get_red_by_nombre(db: Session, nombre: str):
    try:
        query = text("""
            SELECT 
                id_red,
                nombre
            FROM Redes_conocimiento
            WHERE nombre = :nombre
        """)

        result = db.execute(query, {"nombre": nombre}).mappings().first()

        if result is None:
            raise HTTPException(status_code=404, detail="No existe la red de conocimiento")

        return {
            "id_red": result["id_red"],
            "nombre": result["nombre"]
        }

    except HTTPException:
        # Re-lanzar HTTPException para que se propague correctamente
        raise
    except Exception as e:
        logger.error(f"Error al obtener la red por nombre: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error al obtener la red de conocimiento"
        )






def delete_red(db: Session, id_red: int):
    try:
        query = text("""
            DELETE FROM Redes_conocimiento
            WHERE id_red = :el_id
        """)
        db.execute(query, {"el_id": id_red})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar red de conocimiento por id: {e}")
        raise Exception("Error de base de datos al eliminar la red de conocimiento")




def update_red(db: Session, id_red: int, red_update: EditarRedConocimiento) -> bool:
    try:
        # Convierte el esquema Pydantic a dict y excluye campos no enviados
        fields = red_update.model_dump(exclude_unset=True)

        # Si no hay campos para actualizar, retorna False
        if not fields:
            return False

        # Crea la parte dinámica del SET
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])

        # Agrega el id del registro a actualizar
        fields["id_red"] = id_red

        # Ejecuta el UPDATE
        query = text(f"""
            UPDATE Redes_conocimiento 
            SET {set_clause}
            WHERE id_red = :id_red
        """)

        db.execute(query, fields)
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar red de conocimiento: {e}")
        raise Exception("Error de base de datos al actualizar la red de conocimiento")
