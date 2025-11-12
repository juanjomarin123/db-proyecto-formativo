from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging


logger = logging.getLogger(__name__)


def update_url_pdf(db: Session, cod: int,url: str) -> bool:
    try:
        query = text(f""" UPDATE programas_formacion SET url_pdf = :url_pdf 
                    WHERE cod_programa = :codigo """) 
        db.execute(query, {"url_pdf": url, "codigo": cod})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")



def get_programa_by_code(db: Session, cod: int) :
    try:
        query = text(f""" SELECT * FROM programas_formacion
                    WHERE cod_programa = :codigo """) 
        result = db.execute(query, {"codigo": cod}).mappings().first()
        return result
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al consultar usuario: {e}")
        raise Exception("Error de base de datos al consultar el usuario")