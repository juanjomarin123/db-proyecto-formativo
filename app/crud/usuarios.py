


from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging  

from app.schemas.usuarios import CrearUsuario, EditarPass, EditarUsuario, RetornoUsuario  
# Importas los schemas (modelos Pydantic) que usas: para crear usuario, editar usuario, cambiar contraseña, y retornar usuario
from core.security import get_hashed_password, verify_password  
# Importas funciones para manejar contraseñas: para encriptar y para verificar

# Creas un logger específico para este módulo, con su nombre
logger = logging.getLogger(__name__)  


def create_user(db: Session, user: CrearUsuario) -> Optional[bool]: #Crea un usuario en la base de datos usando los datos del schema CrearUsuario.
    try:
        # Convierte el objeto Pydantic (CrearUsuario) a un dict de Python
        dataUser = user.model_dump()
        # Obtiene la contraseña “sin encriptar” desde ese diccionario
        contraOrigin = dataUser["contra_encript"]
        # Encripta la contraseña original
        contraEncript = get_hashed_password(contraOrigin)
        # Reemplaza en el dict la contraseña sin encriptar por la encriptada
        dataUser["contra_encript"] = contraEncript

        # Define la consulta SQL para insertar el usuario
        query = text("""
            INSERT INTO usuario (
                nombre_completo, num_documento, 
                correo, contra_encript, id_rol,
                estado
            ) VALUES (
                :nombre_completo, :num_documento,
                :correo, :contra_encript, :id_rol,
                :estado
            )
        """)
        # Ejecuta la consulta con los datos del usuario
        db.execute(query, dataUser)
        # Hace commit para guardar los cambios en la base de datos
        db.commit()

        return True  # Si todo sale bien, retorna True
    except Exception as e:
        # Si algo falla, deshace la transacción
        db.rollback()
        # Registra el error en el logger
        logger.error(f"Error al crear usuario: {e}")
        # Lanza una excepción genérica con un mensaje más amigable
        raise Exception("Error de base de datos al crear el usuario")


def get_user_by_id(db: Session, id_usuario: int): #Busca un usuario por su ID y retorna sus datos junto con el nombre del rol.
    try:
        query = text("""
            SELECT usuario.id_usuario, usuario.nombre_completo, 
                   usuario.num_documento, usuario.correo, usuario.id_rol, 
                   usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
            WHERE usuario.id_usuario = :id_user
        """)
        # Ejecuta la consulta, mapea resultados y toma el primero (o None si no existe)
        result = db.execute(query, {"id_user": id_usuario}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar usuario por id: {e}")
        raise Exception("Error de base de datos al buscar el usuario")


def get_user_by_email(db: Session, un_correo: str): # Busca un usuario por correo (sin traer la contraseña).
    """Busca un usuario por correo (sin traer la contraseña)."""
    try:
        query = text("""
            SELECT usuario.id_usuario, usuario.nombre_completo, 
                   usuario.num_documento, usuario.correo, usuario.id_rol, 
                   usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
            WHERE usuario.correo = :email
        """)
        result = db.execute(query, {"email": un_correo}).mappings().first() #convierte el resultado en un diccionario y luego toma la primera fila.
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar usuario por email: {e}")
        raise Exception("Error de base de datos al buscar el usuario por correo")


def get_user_by_email_security(db: Session, un_correo: str): # Busca un usuario por correo incluyendo su contraseña encriptada (para autenticación).
    try:
        query = text("""
            SELECT usuario.id_usuario, usuario.nombre_completo, 
                   usuario.num_documento, usuario.contra_encript, 
                   usuario.correo, usuario.id_rol, 
                   usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
            WHERE usuario.correo = :email
        """)
        result = db.execute(query, {"email": un_correo}).mappings().first() #convierte el resultado en un diccionario y luego toma la primera fila.
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar usuario por email: {e}")
        raise Exception("Error de base de datos al buscar el usuario por correo")


def user_delete(db: Session, id: int): # Elimina un usuario de la base de datos por su ID
    try:
        query = text("""
            DELETE FROM usuario
            WHERE usuario.id_usuario = :el_id
        """)
        db.execute(query, {"el_id": id})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario por id: {e}")
        raise Exception("Error de base de datos al eliminar el usuario")


def update_user(db: Session, user_id: int, user_update: EditarUsuario) -> bool: # Actualiza los campos de un usuario (nombre, correo, documento, estado).
    try:
        # Convierte el esquema Pydantic a dict, excluyendo los campos que no se han seteado
        fields = user_update.model_dump(exclude_unset=True)
        # Si no hay ningún campo para actualizar, retorna False
        if not fields:
            return False
        # Crea la parte "SET campo = :campo" dinámicamente según los campos a actualizar
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        # Agrega el ID del usuario al diccionario de parámetros
        fields["user_id"] = user_id

        # Ejecuta la consulta de actualización
        query = text(f"UPDATE usuario SET {set_clause} WHERE id_usuario = :user_id")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")


def update_password(db: Session, user_data: EditarPass) -> bool: # Cambia la contraseña de un usuario
    try:
        datos_usuario = user_data.model_dump()  # Convierte el esquema Pydantic a dict
        # Encripta la nueva contraseña
        contra_encript = get_hashed_password(datos_usuario['contra_nueva'])
        datos_usuario['pass_encript'] = contra_encript

        # Consulta para actualizar la contraseña en la base
        query = text(f""" UPDATE usuario SET contra_encript = :pass_encript 
                        WHERE id_usuario = :id_usuario """)
        db.execute(query, datos_usuario)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar contraseña: {e}")
        raise Exception("Error de base de datos al actualizar la contraseña")


def verify_user_pass(db: Session, user_data: EditarPass) -> bool: # Verifica que la contraseña anterior ingresada por el usuario sea correcta.
    """"""
    try:
        query = text("""
            SELECT usuario.contra_encript
            FROM usuario
            WHERE usuario.id_usuario = :id_user
        """)
        # Obtiene la contraseña encriptada desde la base para el usuario dado
        result = db.execute(query, {"id_user": user_data.id_usuario}).mappings().first()
        if result is None:
            return False
        contra_en_db = result["contra_encript"]
        contra_anterior = user_data.contra_anterior

        # Verifica la contraseña antigua usando la función de seguridad
        validated = verify_password(contra_anterior, contra_en_db)

        # Retorna `True` si la contraseña ingresada coincide con la almacenada
        if not validated:
            return False
        else:
            return True
    except SQLAlchemyError as e:
        logger.error(f"Error al validar la contraseña: {e}")
        raise Exception("Error de base de datos al validar la contraseña")
