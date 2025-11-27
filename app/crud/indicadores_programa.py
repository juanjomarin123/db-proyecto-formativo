from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging  

from app.schemas.indicadores_programa import (CrearIndicadoresPrograma,RetornoIndicadoresPrograma,EditarIndicadoresPrograma
)

logger = logging.getLogger(__name__)




def crear_indicadores(db: Session, indicadores: CrearIndicadoresPrograma) -> Optional[bool]:
    try:
        data = indicadores.model_dump()

        # Construcción dinámica del INSERT
        columnas = ", ".join(data.keys())
        valores = ", ".join([f":{k}" for k in data.keys()])

        query = text(f"""
            INSERT INTO Indicadores_programa ({columnas})
            VALUES ({valores})
        """)

        db.execute(query, data)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear indicadores: {e}")
        raise Exception("Error de base de datos al crear los indicadores")
    


def get_indicadores_by_codPrograma(db: Session, cod_programa: int):
    try:
        query = text("""
            SELECT *
            FROM Indicadores_programa
            WHERE cod_programa = :cod_programa
        """)

        result = db.execute(query, {"cod_programa": cod_programa}).mappings().first()

        if result is None:
            raise HTTPException(status_code=404, detail="No existen indicadores para este programa")

        return dict(result)

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener indicadores por cod_programa: {e}")
        raise Exception("Error de base de datos al obtener los indicadores")
    



def indicadores_delete(db: Session, cod_programa: int) -> bool:
    try:
        query = text("""
            DELETE FROM Indicadores_programa
            WHERE cod_programa = :cod_programa
        """)

        result = db.execute(query, {"cod_programa": cod_programa})

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Indicadores no encontrados")

        db.commit()
        return True

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar indicadores: {e}")
        raise Exception("Error de base de datos al eliminar los indicadores")
    



def update_indicadores(
    db: Session, cod_programa: int, indicadores_update: EditarIndicadoresPrograma
) -> bool:
    try:
        data = indicadores_update.model_dump(exclude_unset=True)

        if not data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        data["cod_programa"] = cod_programa

        query = text(f"""
            UPDATE Indicadores_programa
            SET {set_clause}
            WHERE cod_programa = :cod_programa
        """)

        result = db.execute(query, data)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Indicadores no encontrados")

        db.commit()
        return True

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar indicadores: {e}")
        raise Exception("Error de base de datos al actualizar los indicadores")
