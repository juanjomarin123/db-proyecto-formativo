from typing import Optional
from pydantic import BaseModel, Field

class ProgramaFormacionBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=180)
    version: str = Field(..., min_length=1, max_length=4)
    nivel: str = Field(None, min_length=3, max_length=50)
    id_red: int = None
    tiempo_dur: int = Field(None, ge=0)
    unidad_dur: str = Field(None, max_length=20)
    estado: str = Field(None, max_length=20)
    url_pdf: str = Field(None, max_length=180)

class CrearProgramaFormacion(ProgramaFormacionBase):
    pass

class RetornoProgramaFormacion(ProgramaFormacionBase):
    cod_programa: int

class EditarProgramaFormacion(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=180)
    version: Optional[str] = Field(None, min_length=1, max_length=4)
    nivel: Optional[str] = Field(None, min_length=3, max_length=50)
    id_red: Optional[int] = None
    tiempo_dur: Optional[int] = Field(None, ge=0)
    unidad_dur: Optional[str] = Field(None, max_length=20)
    estado: Optional[str] = Field(None, min_length=3, max_length=20)
    url_pdf: Optional[str] = Field(None, max_length=180)