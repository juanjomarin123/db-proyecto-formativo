from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class registroCalificadoBase(BaseModel):
    cod_programa: int
    tipo_tramite: str = Field(..., min_length=3, max_length=50)
    fecha_radicado: date
    numero_resolucion: int
    fecha_resolucion: date
    fecha_vencimiento: date
    vigencia: str = Field(..., min_length=1, max_length=25)
    modalidad: str = Field(..., min_length=3, max_length=25)
    clasificacion: str = Field(..., min_length=3, max_length=15)
    estado_catalogo: bool


class CrearRegistroCalificado(registroCalificadoBase):
    pass


class RetornoRegistroCalificado(registroCalificadoBase):
    cod_programa: int


class EditarRegistroCalificado(BaseModel):
    cod_programa: Optional[int] = None
    tipo_tramite: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_radicado: Optional[date] = None
    numero_resolucion: Optional[int] = None
    fecha_resolucion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    vigencia: Optional[str] = Field(None, min_length=1, max_length=25)
    modalidad: Optional[str] = Field(None, min_length=3, max_length=25)
    clasificacion: Optional[str] = Field(None, min_length=3, max_length=15)
    estado_catalogo: Optional[str] = Field(None, min_length=3, max_length=50)
