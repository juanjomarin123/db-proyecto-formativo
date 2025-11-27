#toma todas las piezas funcionales (los routers con sus lógicas de 
# negocio y seguridad) y las conecta a la instancia principal de FastAPI,
#  aplicando las configuraciones globales necesarias para que la API pueda ser accedida y utilizada.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



from app.router import usuarios
from app.router import auth
from app.router import redes_conocimiento
from app.router import programas_formacion
from app.router import registro_calificado
from app.router import indicadores_programa
from app.router import cargar_archivos
from app.router import subir_pdf_programas
# from app.router import cargar_archivos


app = FastAPI()

# Montar directorio estático para servir archivos
# La ruta /static mapeará al directorio "static" del sistema de archivos.
# Esto permite servir archivos como CSS, JS o imágenes directamente.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir en el objeto app los routers
# Se adjuntan los routers importados a la aplicación principal, definiendo su prefijo de ruta y etiquetas.
app.include_router(usuarios.router, prefix="/usuario", tags=["SERVICIO USUARIOS"])
app.include_router(auth.router, prefix="/access", tags=["SERVICIO DE LOGIN"])
app.include_router(redes_conocimiento.router, prefix="/redes_conocimiento", tags=["SERVICIO REDES DE CONOCIMIENTO"])
app.include_router(cargar_archivos.router, prefix="/subir", tags=["CARGAR ARCHIVOS"])
app.include_router(programas_formacion.router, prefix="/programas_formacion", tags=["SERVICIO PROGRAMAS DE FORMACION"])
app.include_router(registro_calificado.router, prefix="/registro_calificado", tags=["SERVICIO REGISTRO CALIFICADO"])
app.include_router(indicadores_programa.router, prefix="/indicadores_programa", tags=["SERVICIO INDICADORES DE PROGRAMA"])
app.include_router(subir_pdf_programas.router, prefix="/subir_pdf", tags=["SUBIR PDF PROGRAMAS"])

# app.include_router(cargar_archivos.router, prefix="/cargar", tags=["cargar archivos excel"])
# Nota: El router de programas está importado, pero no incluido aquí en la lógica original.


# Configuración de CORS (Cross-Origin Resource Sharing)
# Esto es un middleware que se ejecuta en cada solicitud para permitir que clientes de diferentes dominios accedan a la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen (*)
    allow_credentials=True, # Permitir el uso de cookies y encabezados de autenticación
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

# Definición de la ruta raíz de la API
@app.get("/")
def read_root():
    # Retorna un diccionario simple al acceder a la URL base de la aplicación.
    return {
                "message": "ok",
                "autor": "ADSO 2925888"
            }