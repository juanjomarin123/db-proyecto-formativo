from sqlalchemy import text
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from io import BytesIO
from app.crud import programas_formacion, redes_conocimiento
from app.crud.cargar_archivos import actualizar_estado_y_duracion, insertar_indicadores_programa, insertar_registro_calificado
from core.database import get_db
from app.crud.cargar_archivos import insertar_redes_conocimiento
from app.crud.cargar_archivos import insertar_programas_formacion

router = APIRouter()

@router.post("/upload-redes/")
async def upload_redes(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_excel(BytesIO(await file.read()), engine="openpyxl", dtype=str)
        df.columns = df.columns.str.strip()

        # La columna exacta del Excel
        if "RED DE  CONOCIMIENTO" not in df.columns:
            raise HTTPException(status_code=400, detail="No se encontró la columna 'RED DE  CONOCIMIENTO' en el Excel")

        # Obtener redes y limpiar duplicados
        redes_excel = df["RED DE  CONOCIMIENTO"].dropna().astype(str).str.strip()

        # Quitar duplicados —> CLAVE
        redes_unicas = list(set(redes_excel))

        if not redes_unicas:
            raise HTTPException(status_code=400, detail="No se encontraron redes válidas para insertar")

        # Llamar al CRUD
        resultado = insertar_redes_conocimiento(db, redes_unicas)

        return {
            "mensaje": "Redes procesadas",
            "total_archivo": len(redes_excel),
            "total_unicas": len(redes_unicas),
            "resultado": resultado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-excel-programas-registro_calificado/")
async def upload_excel_programas(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_excel(BytesIO(await file.read()), engine="openpyxl", dtype=str)
        df.columns = df.columns.str.strip()

        # Renombrar columnas según CRUD
        df = df.rename(columns={
            "COD DEL PROGRAMA": "cod_programa",
            "VERSION": "version",
            "NOMBRE DEL PROGRAMA": "nombre",
            "NIVEL DE FORMACIÓN": "nivel",
            "RED DE  CONOCIMIENTO": "nombre_red",
        })

        # Columnas obligatorias
        required_cols = ["cod_programa", "version", "nombre", "nivel", "nombre_red"]
        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"No se encontró la columna obligatoria '{col}' en el Excel"
                )

        # LIMPIEZA DE NAN Y FILAS VACÍAS
        df = df.dropna(subset=["cod_programa", "nombre_red"], how="any")
        df = df[df["cod_programa"].str.strip() != ""]
        df = df[df["nombre_red"].str.strip() != ""]
        df = df[df["cod_programa"].str.lower() != "nan"]
        df = df[df["nombre_red"].str.lower() != "nan"]

        lista_programas = []

        for _, row in df.iterrows():

            # Validar cod_programa correctamente
            try:
                cod_programa = int(row["cod_programa"])
            except:
                continue  # ignora fila basura

            registro = {
                "cod_programa": cod_programa,
                "version": str(row["version"]).strip(),
                "nombre": str(row["nombre"]).strip(),
                "nivel": str(row["nivel"]).strip(),
                "nombre_red": str(row["nombre_red"]).strip(),
                "tiempo_dur": row["tiempo_dur"] if "tiempo_dur" in df.columns else None,
                "unidad_dur": str(row["unidad_dur"]).strip() if "unidad_dur" in df.columns else "",
                "url_pdf": str(row["url_pdf"]).strip() if "url_pdf" in df.columns else ""
            }

            lista_programas.append(registro)

        if not lista_programas:
            raise HTTPException(status_code=400, detail="No hay registros válidos en el Excel")

        # Llamar al CRUD
        resultado = insertar_programas_formacion(db, lista_programas)

        return {
            "mensaje": "Proceso completado",
            "total_procesados": len(lista_programas),
            "resultado": resultado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-excel-registro-calificado/")
async def upload_excel_registro_calificado(file: UploadFile = File(...), db: Session = Depends(get_db)):

    def limpiar(valor):
        if valor is None:
            return None
        valor = str(valor).strip()
        if valor == "" or valor.lower() == "nan":
            return None
        return valor

    try:
        df = pd.read_excel(BytesIO(await file.read()), engine="openpyxl", dtype=str)
        df.columns = df.columns.str.strip()

        df = df.rename(columns={
            "COD DEL PROGRAMA": "cod_programa",
            "TIPO DE TRÁMITE": "tipo_tramite",
            "FECHA RADICADO": "fecha_radicado",
            "NUMERO DE RESOLUCION": "numero_resolucion",
            "FECHA DE RESOLUCION": "fecha_resolucion",
            "Fecha de vencimiento": "fecha_vencimiento",
            "VIGENCIA RC": "vigencia",
            "MODALIDAD": "modalidad",
            "CLASIFICACIÓN PARA TRÁMITE": "clasificacion",
            "Estado Catálogo": "estado_catalogo"
        })

        registros = []

        for _, row in df.iterrows():

            # IGNORAR FILAS COMPLETAMENTE VACÍAS
            if row.isnull().all():
                continue

            # validar código
            try:
                cod_programa = int(row["cod_programa"])
            except:
                continue  # si falla, ignorar fila completa

            numero_res = limpiar(row.get("numero_resolucion"))
            numero_resolucion = int(numero_res) if numero_res and numero_res.isdigit() else None

            registro = {
                "cod_programa": cod_programa,
                "tipo_tramite": limpiar(row.get("tipo_tramite")),
                "fecha_radicado": limpiar(row.get("fecha_radicado")),
                "numero_resolucion": numero_resolucion,
                "fecha_resolucion": limpiar(row.get("fecha_resolucion")),
                "fecha_vencimiento": limpiar(row.get("fecha_vencimiento")),
                "vigencia": limpiar(row.get("vigencia")),
                "modalidad": limpiar(row.get("modalidad")),
                "clasificacion": limpiar(row.get("clasificacion")),
                "estado_catalogo": limpiar(row.get("estado_catalogo")),
            }

            # si TODOS los demás campos son None, no insertar
            if all(v is None for k, v in registro.items() if k != "cod_programa"):
                continue

            registros.append(registro)

        if not registros:
            raise HTTPException(status_code=400, detail="No hay registros válidos en el Excel")

        resultado = insertar_registro_calificado(db, registros)

        return {
            "mensaje": "Proceso completado",
            "total_registros": len(registros),
            "resultado": resultado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/upload-excel-programas-estado-duracion/")
async def upload_excel_estado_duracion(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Leer Excel y saltar las primeras 4 filas basura
        df = pd.read_excel(
            BytesIO(await file.read()),
            engine="openpyxl",
            skiprows=4
        )

        df.columns = df.columns.str.strip()
        print("COLUMNAS ENCONTRADAS:", df.columns.tolist())
        # Renombrar columnas para trabajarlas internas
        df = df.rename(columns={
            "NOMBRE\_PROGRAMA\_FORMACION": "nombre_programa",
            "NOMBRE_PROGRAMA_FORMACION": "nombre_programa",  # por si vienen sin escape
            "ESTADO_CURSO": "estado",
            "DURACION_PROGRAMA": "duracion"
        })

        # Validar columnas obligatorias
        required_cols = ["nombre_programa", "estado", "duracion"]
        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Falta la columna obligatoria '{col}' en el archivo"
                )

        # Lista final para el CRUD
        lista_registros = []

        for _, row in df.iterrows():

            nombre = str(row["nombre_programa"]).strip()
            if not nombre or nombre.lower() == "nan":
                continue  # saltar filas malas

            # Validar duración
            try:
                duracion = float(row["duracion"])
            except:
                continue

            registro = {
                "NOMBRE_PROGRAMA_FORMACION": nombre,
                "ESTADO_CURSO": str(row["estado"]).strip(),
                "DURACION_PROGRAMA": duracion
            }

            lista_registros.append(registro)

        if not lista_registros:
            raise HTTPException(status_code=400, detail="No hay registros válidos en el Excel")

        # Ejecutar CRUD
        resultado = actualizar_estado_y_duracion(db, lista_registros)

        return {
            "mensaje": "Actualización completada",
            "total_registros": len(lista_registros),
            "actualizados": resultado["actualizados"],
            "errores": resultado["errores"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/upload-excel-indicadores-programa/")
async def upload_excel_indicadores_programa(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint para subir Excel con indicadores de programas
    - Mapea TODAS las columnas relevantes del Excel
    - Convierte NULL/NaN a 0 automáticamente
    - Incluye poblaciones especiales como campesinos, indígenas, etc.
    """

    def limpiar_y_convertir(valor):
        """Limpia y convierte valores, retorna 0 si es None o vacío"""
        if pd.isna(valor) or valor is None:
            return 0
        if isinstance(valor, str):
            valor = valor.strip()
            if valor == "" or valor.lower() in ["nan", "none", "null", "na"]:
                return 0
        # Convertir a int si es numérico
        try:
            if valor is not None:
                # Manejar valores float como "13.0" -> 13
                valor_float = float(valor)
                return int(valor_float) if valor_float.is_integer() else int(round(valor_float))
        except (ValueError, TypeError):
            # Si no se puede convertir, retornar 0
            return 0
        return 0  # Por defecto retornar 0

    try:
        # Validar tipo de archivo
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")

        # Leer Excel y saltar las primeras 4 filas basura
        df = pd.read_excel(
            BytesIO(await file.read()),
            engine="openpyxl",
            skiprows=4,
            dtype=str  # Leer todo como string inicialmente para preservar formatos
        )

        # Validar que el DataFrame no esté vacío
        if df.empty:
            raise HTTPException(status_code=400, detail="El archivo Excel está vacío o no tiene datos válidos")

        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip().str.replace("\n", "_").str.replace("\r", "_").str.replace(" ", "_").str.upper()

        # Verificar que existe la columna obligatoria
        if "NOMBRE_PROGRAMA_FORMACION" not in df.columns:
            raise HTTPException(
                status_code=400, 
                detail="El archivo debe contener la columna 'NOMBRE_PROGRAMA_FORMACION'"
            )

        # MAPEO COMPLETO DE TODAS LAS COLUMNAS RELEVANTES
        mapeo_columnas = {
            # Columnas originales de violencia
            "INDIGENAS_DESPLAZADOS_POR_LA_VIOLENCIA___TOTAL_APRENDICES": "INDIGENAS_VIOLENCIA_TOTAL",
            "INDIGENAS_DESPLAZADOS_POR_LA_VIOLENCIA_CABEZA_DE_FAMILIA___TOTAL_APRENDICES": "INDIGENAS_VIOLENCIA_CDF_TOTAL",
            "AFROCOLOMBIANOS_DESPLAZADOS_POR_LA_VIOLENCIA__TOTAL_APRENDICES": "AFRO_VIOLENCIA_TOTAL",
            "AFROCOLOMBIANOS_DESPLAZADOS_POR_LA_VIOLENCIA_CABEZA_DE_FAMILIA__TOTAL_APRENDICES": "AFRO_VIOLENCIA_CDF_TOTAL",
            "DESPLAZADOS_POR_LA_VIOLENCIA__TOTAL_APRENDICES": "DESPLAZADOS_VIOLENCIA_TOTAL",
            "DESPLAZADOS_POR_LA_VIOLENCIA_CABEZA_DE_FAMILIA__TOTAL_APRENDICES": "DESPLAZADOS_VIOLENCIA_CDF_TOTAL",
            
            # Columnas de discapacidad
            "DISCAPACIDAD___TOTAL_APRENDICES": "DISCAPACIDAD_TOTAL",
            "DISCAPACIDAD_AUDITIVA__TOTAL_APRENDICES": "DISCAPACIDAD_AUDITIVA_TOTAL",
            "DISCAPACIDAD_VISUAL___TOTAL_APRENDICES": "DISCAPACIDAD_VISUAL_TOTAL",
            "DISCAPACIDAD_FISICA___TOTAL_APRENDICES": "DISCAPACIDAD_FISICA_TOTAL",
            "DISCAPACIDAD_INTELECTUAL__TOTAL_APRENDICES": "DISCAPACIDAD_INTELECTUAL_TOTAL",
            "DISCAPACIDAD_PSICOSOCIAL___TOTAL_APRENDICES": "DISCAPACIDAD_PSICOSOCIAL_TOTAL",
            "DISCAPACIDAD_MULTIPLE___TOTAL_APRENDICES": "DISCAPACIDAD_MULTIPLE_TOTAL",
            "SORDOCEGUERA___TOTAL_APRENDICES": "SORDOCEGUERA_TOTAL",
            
            # NUEVAS COLUMNAS - POBLACIONES ESPECIALES (TOTALES)
            "CAMPESINOS___TOTAL_APRENDICES": "CAMPESINOS_TOTAL",
            "INDIGENAS___TOTAL_APRENDICES": "INDIGENAS_TOTAL",
            "AFROCOLOMBIANOS___TOTAL_APRENDICES": "AFROCOLOMBIANOS_TOTAL",
            "RAIZALES___TOTAL_APRENDICES": "RAIZALES_TOTAL",
            "PALENQUEROS___TOTAL_APRENDICES": "PALENQUEROS_TOTAL",
            "ROM___TOTAL_APRENDICES": "ROM_TOTAL",
            "NEGRO___TOTAL_APRENDICES": "NEGRO_TOTAL",
            
            # Otras poblaciones especiales
            "DESPLAZADOS_POR_FENOMENOS_NATURALES___TOTAL_APRENDICES": "DESPLAZADOS_FENOMENOS_NAT_TOTAL",
            "MUJER_CABEZA_DE_FAMILIA___TOTAL_APRENDICES": "MUJER_CABEZA_FAMILIA_TOTAL",
            "ADOLESCENTE_TRABAJADOR__TOTAL_APRENDICES": "ADOLESCENTE_TRABAJADOR_TOTAL",
            "JOVENES_VULNERABLES___TOTAL_APRENDICES": "JOVENES_VULNERABLES_TOTAL",
            "TERCERA_EDAD___TOTAL_APRENDICES": "TERCERA_EDAD_TOTAL",
            "EMPRENDEDORES___TOTAL_APRENDICES": "EMPRENDEDORES_TOTAL",
            "ARTESANOS__TOTAL_APRENDICES": "ARTESANOS_TOTAL",
            "MICROEMPRESAS___TOTAL_APRENDICES": "MICROEMPRESAS_TOTAL",
            
            # Columnas de víctimas (sumar diferentes tipos para total víctimas)
            "DESPOJO___TOTAL_APRENDICES": "DESPOJO_TOTAL",
            "ACTOS_DE_GRUPOS_ARMADOS___TOTAL_APRENDICES": "ACTOS_GRUPOS_ARMADOS_TOTAL",
            "AMENAZA___TOTAL_APRENDICES": "AMENAZA_TOTAL",
            "DELITOS_SEXUALES___TOTAL_APRENDICES": "DELITOS_SEXUALES_TOTAL",
            "DESAPARICION_FORZADA___TOTAL_APRENDICES": "DESAPARICION_FORZADA_TOTAL",
            "HOMICIDIO_/_MASACRE___TOTAL_APRENDICES": "HOMICIDIO_MASACRE_TOTAL",
            "MINAS_ANTIPERSONALES_Y_EXPLOSIVOS___TOTAL_APRENDICES": "MINAS_ANTIPERSONALES_TOTAL",
            "SECUESTRO___TOTAL_APRENDICES": "SECUESTRO_TOTAL",
            "TORTURA___TOTAL_APRENDICES": "TORTURA_TOTAL",
            "USO_DE_MENORES_POR_GRUPOS_ARMADOS___TOTAL_APRENDICES": "USO_MENORES_GRUPOS_ARMADOS_TOTAL",
            "HERIDO___TOTAL_APRENDICES": "HERIDO_TOTAL",
            "RECLUTAMIENTO_FORZADO___TOTAL_APRENDICES": "RECLUTAMIENTO_FORZADO_TOTAL",
            "DESPLAZADOS_DISCAPACITADOS__TOTAL_APRENDICES": "DESPLAZADOS_DISCAPACITADOS_TOTAL",
            "ADOLESCENTE_EN_CONFLICTO_CON_LA_LEY_PENAL___TOTAL_APRENDICES": "ADOLESCENTE_CONFLICTO_LEY_TOTAL",
            "INPEC___TOTAL_APRENDICES": "INPEC_TOTAL",
            "PROC_REINTEGRACION___TOTAL_APRENDICES": "PROC_REINTEGRACION_TOTAL",
            "ADOLESCENTE_DESVINCULADO_DE_GRUPOS_ARMADOS_ORGANIZADOS_AL_MARGEN_DE_LA_LEY__TOTAL_APRENDICES": "ADOLESCENTE_DESVINCULADO_GRUPOS_ARMADOS_TOTAL",
            "REMITIDOS_POR_EL_PAL___TOTAL_APRENDICES": "REMITIDOS_PAL_TOTAL",
            "SOBREVIVIENTES_MINAS_ANTIPERSONALES___TOTAL_APRENDICES": "SOBREVIVIENTES_MINAS_TOTAL",
            "SOLDADOS_CAMPESINOS__TOTAL_APRENDICES": "SOLDADOS_CAMPESINOS_TOTAL",
            "NINGUNA__TOTAL_APRENDICES": "NINGUNA_TOTAL",
            "REMITIDOS_POR_EL_CIE___TOTAL_APRENDICES": "REMITIDOS_CIE_TOTAL",

            
            
            # Total general
            "GRAN_TOTAL_APRENDICES": "GRAN_TOTAL_APRENDICES"
        }

        # Aplicar renombrado solo para columnas que existen
        columnas_existentes = {k: v for k, v in mapeo_columnas.items() if k in df.columns}
        df = df.rename(columns=columnas_existentes)

        # Mostrar columnas disponibles para debugging
        print("Columnas disponibles después del mapeo:")
        for col in df.columns:
            print(f"  - {col}")

        registros = []
        filas_sin_nombre = 0
        filas_vacias = 0

        for numero_fila, (index, row) in enumerate(df.iterrows(), 1):
            # Saltar filas completamente vacías
            if row.isnull().all() or row.astype(str).str.strip().eq('').all():
                filas_vacias += 1
                continue

            # OBTENER Y VALIDAR NOMBRE DEL PROGRAMA (OBLIGATORIO)
            nombre_programa = row.get("NOMBRE_PROGRAMA_FORMACION")
            if pd.isna(nombre_programa) or not nombre_programa or str(nombre_programa).strip() == "":
                filas_sin_nombre += 1
                continue  # NO insertar filas sin nombre

            nombre_programa_limpio = str(nombre_programa).strip()

            # Crear registro con TODOS los campos, aplicando limpieza automática
            registro = {"NOMBRE_PROGRAMA_FORMACION": nombre_programa_limpio}
            
            # Agregar TODAS las columnas mapeadas con limpieza automática
            for col_db in set(columnas_existentes.values()):
                registro[col_db] = limpiar_y_convertir(row.get(col_db))
            
            # Calcular total víctimas si es necesario (sumando diferentes tipos)
            total_victimas = (
                registro.get("DESPOJO_TOTAL", 0) +
                registro.get("ACTOS_GRUPOS_ARMADOS_TOTAL", 0) +
                registro.get("AMENAZA_TOTAL", 0) +
                registro.get("DELITOS_SEXUALES_TOTAL", 0) +
                registro.get("DESAPARICION_FORZADA_TOTAL", 0) +
                registro.get("HOMICIDIO_MASACRE_TOTAL", 0) +
                registro.get("MINAS_ANTIPERSONALES_TOTAL", 0) +
                registro.get("SECUESTRO_TOTAL", 0) +
                registro.get("TORTURA_TOTAL", 0) +
                registro.get("USO_MENORES_GRUPOS_ARMADOS_TOTAL", 0) +
                registro.get("HERIDO_TOTAL", 0) +
                registro.get("RECLUTAMIENTO_FORZADO_TOTAL", 0)
            )
            registro["VICTIMAS_TOTAL"] = total_victimas

            registros.append(registro)

        # Validar que hay registros para procesar
        if not registros:
            raise HTTPException(
                status_code=400, 
                detail=f"""No hay registros válidos en el Excel. 
                         Filas sin nombre: {filas_sin_nombre}
                         Filas vacías: {filas_vacias}
                         Total filas en Excel: {len(df)}
                         Columnas encontradas: {list(df.columns)}"""
            )

        # Llamar a la función del CRUD
        resultado = insertar_indicadores_programa(db, registros)

        return {
            "mensaje": "Proceso de carga completado",
            "resumen": {
                "total_filas_excel": len(df),
                "registros_procesados": len(registros),
                "filas_sin_nombre_ignoradas": filas_sin_nombre,
                "filas_vacias_ignoradas": filas_vacias,
                "columnas_mapeadas": list(columnas_existentes.values())
            },
            "resultado_crud": resultado
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")