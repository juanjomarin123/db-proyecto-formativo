from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from core.database import get_db


router = APIRouter()

UPLOAD_DIR = "uploads/pdfs"

@router.post("/subir-pdf_Programa-Diseño curricular/")
async def upload_pdf(
    codigo: int = Form(None, description="Código del programa"),
    file: UploadFile = File(..., description="Diseño curricular en formato PDF"),
    db: Session = Depends(get_db)
):
    """
    Sube un PDF para un programa específico
    """
    
    # Validar que sea PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "Solo se permiten archivos PDF")
    
    # Verificar que el programa exista
    programa = db.execute(
        text("SELECT nombre FROM Programas_formacion WHERE cod_programa = :codigo"),
        {"codigo": codigo}
    ).fetchone()
    
    if not programa:
        raise HTTPException(404, f"Programa {codigo} no encontrado")
    
    # Crear directorio
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Guardar archivo
    file_path = os.path.join(UPLOAD_DIR, f"programa_{codigo}_{file.filename}")
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Actualizar BD
        db.execute(
            text("UPDATE Programas_formacion SET url_pdf = :path WHERE cod_programa = :codigo"),
            {"path": file_path, "codigo": codigo}
        )
        db.commit()
        
        return {
            "mensaje": "PDF subido exitosamente",
            "programa": programa.nombre,
            "ruta": file_path
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error: {str(e)}")


@router.get("/ver-pdf/{codigo}")
async def ver_pdf(codigo: int, db: Session = Depends(get_db)):
    """
    Descarga el PDF de un programa específico
    """
    # Buscar la ruta del PDF en la base de datos
    resultado = db.execute(
        text("SELECT url_pdf FROM Programas_formacion WHERE cod_programa = :codigo"),
        {"codigo": codigo}
    ).fetchone()
    
    if not resultado or not resultado.url_pdf:
        raise HTTPException(404, f"No se encontró PDF para el programa {codigo}")
    
    ruta_pdf = resultado.url_pdf
    
    # Verificar que el archivo existe físicamente
    if not os.path.exists(ruta_pdf):
        raise HTTPException(404, f"El archivo PDF no existe en la ruta: {ruta_pdf}")
    
    # Devolver el archivo
    return FileResponse(
        path=ruta_pdf,
        filename=f"programa_{codigo}.pdf",
        media_type='application/pdf'
    )

@router.get("/programas/{codigo}/info-pdf")
async def info_pdf(codigo: int, db: Session = Depends(get_db)):
    """
    Obtiene información sobre el PDF de un programa
    """
    resultado = db.execute(
        text("SELECT nombre, url_pdf FROM Programas_formacion WHERE cod_programa = :codigo"),
        {"codigo": codigo}
    ).fetchone()
    
    if not resultado:
        raise HTTPException(404, f"Programa {codigo} no encontrado")
    
    archivo_existe = os.path.exists(resultado.url_pdf) if resultado.url_pdf else False
    
    return {
        "codigo_programa": codigo,
        "nombre_programa": resultado.nombre,
        "url_pdf": resultado.url_pdf,
        "tiene_pdf": resultado.url_pdf is not None,
        "archivo_existe": archivo_existe
    }