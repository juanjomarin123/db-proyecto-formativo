DROP DATABASE IF EXISTS mi_proyecto_f;
CREATE DATABASE mi_proyecto_f;
USE mi_proyecto_f;

CREATE TABLE rol (
    id_rol SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(20)
);

CREATE TABLE usuario (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(80) NOT NULL,
    num_documento CHAR(12),
    correo VARCHAR(100) UNIQUE,
    contra_encript VARCHAR(140),
    id_rol SMALLINT UNSIGNED,
    estado BOOLEAN,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);
