from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.router.dependencies import get_current_user
from app.schemas.indicadores_programa import (CrearIndicadoresPrograma,RetornoIndicadoresPrograma,EditarIndicadoresPrograma)
from app.schemas.usuarios import RetornoUsuario
from core.database import get_db
from app.crud.indicadores_programa import (crear_indicadores,get_indicadores_by_codPrograma,update_indicadores,indicadores_delete)

router = APIRouter()


@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def crear_indicadores_programa(
    indicadores: CrearIndicadoresPrograma,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear indicadores de programa")
        
        creado = crear_indicadores(db, indicadores)

        if creado:
            return {"message": "Indicadores de programa creados correctamente"}
        else:
            return {"message": "Los indicadores de programa no pudieron ser creados correctamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/obtener-por-id/{cod_programa}", status_code=status.HTTP_200_OK, response_model=RetornoIndicadoresPrograma)
def get_indicadores_by_cod(
    cod_programa: int,
    db: Session = Depends(get_db)
):
    try:
        resultado = get_indicadores_by_codPrograma(db, cod_programa)
        return resultado
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/editar/{cod_programa}", status_code=status.HTTP_200_OK)
def editar_indicadores_programa(
    cod_programa: int,
    indicadores_update: EditarIndicadoresPrograma,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para editar indicadores de programa")
        
        actualizado = update_indicadores(db, cod_programa, indicadores_update)

        if actualizado:
            return {"message": "Indicadores de programa editados correctamente"}
        else:
            return {"message": "Los indicadores de programa no pudieron ser editados correctamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/eliminar/{cod_programa}", status_code=status.HTTP_200_OK)
def eliminar_indicadores_programa(
    cod_programa: int,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar indicadores de programa")
        
        eliminado = indicadores_delete(db, cod_programa)

        if eliminado:
            return {"message": "Indicadores de programa eliminados correctamente"}
        else:
            return {"message": "Los indicadores de programa no pudieron ser eliminados correctamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

