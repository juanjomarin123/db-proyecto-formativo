
{
  "username": "admin@example.com",
  "password": "admin123"
}


## USUARIOS (/usuario)

POST /usuario/registrar
**Crear usuario (requiere token con id_rol = 1)**


{
  "nombre_completo": "Juan Pérez García",
  "id_rol": 2,
  "correo": "juan.perez@example.com",
  "num_documento": "1234567890",
  "contra_encript": "password123",
  "estado": true
}


GET /usuario/obtener-por-id/{id_usuario}
**Obtener usuario por ID (requiere token con id_rol = 1)**
- Parámetro de ruta: `id_usuario` = 1

GET /usuario/obtener-por-correo/{correo}
**Obtener usuario por correo (requiere token con id_rol = 1)**
- Parámetro de ruta: `correo` = "admin@example.com"

PUT /usuario/editar/{user_id}
**Editar usuario (requiere token con id_rol = 1)**
- Parámetro de ruta: `user_id` = 1


{
  "nombre_completo": "Juan Pérez García Actualizado",
  "correo": "juan.nuevo@example.com",
  "num_documento": "1234567890",
  "estado": true
}


### PUT /usuario/editar-contrasenia
**Cambiar contraseña (requiere token con id_rol = 1)**

{
  "id_usuario": 1,
  "contra_anterior": "password123",
  "contra_nueva": "nuevapassword456
  }


DELETE /usuario/eliminar-por-id/{id_usuario}
**Eliminar usuario (requiere token con id_rol = 1)**
- Parámetro de ruta: `id_usuario` = 1


 PROGRAMAS DE FORMACIÓN (/programas_formacion)

POST /programas_formacion/registrar
**Crear programa (requiere token con id_rol = 1)**

{
  "version": "0001",
  "nombre": "Tecnólogo en Desarrollo de Software",
  "nivel": "Tecnólogo",
  "id_red": 2,
  "tiempo_dur": 24,
  "unidad_dur": "Meses",
  "estado": "Activo",
  "url_pdf": "https://example.com/archivo.pdf"
}


GET /programas_formacion/obtener-por-cod/{cod_programa}
**Obtener programa por código**
- Parámetro de ruta: `cod_programa` = 12345

 GET /programas_formacion/obtener-por-id_red/{id_red}
**Obtener programa por ID de red**
- Parámetro de ruta: `id_red` = 2
PUT /programas_formacion/editar/{cod_programa}
**Editar programa (requiere token con id_rol = 1)**
- Parámetro de ruta: `cod_programa` = 12345

{
  "nombre": "Tecnólogo en Desarrollo de Software Actualizado",
  "nivel": "Tecnólogo",
  "tiempo_dur": 30,
  "unidad_dur": "Meses",
  "estado": "Activo"
}


DELETE /programas_formacion/eliminar-por-cod/{cod_programa}
**Eliminar programa (requiere token con id_rol = 1)**
- Parámetro de ruta: `cod_programa` = 12345



REDES DE CONOCIMIENTO (/redes_conocimiento)

POST /redes_conocimiento/registrar
**Crear red de conocimiento (requiere token con id_rol = 1)**


{
  "nombre": "Tecnologías de la Información"
}


GET /redes_conocimiento/obtener-por-id/{id_red}
**Obtener red por ID**
- Parámetro de ruta: `id_red` = 1

GET /redes_conocimiento/obtener-por-nombre/{nombre}
**Obtener red por nombre**
- Parámetro de ruta: `nombre` = "Tecnologías de la Información"

PUT /redes_conocimiento/editar/{id_red}
**Editar red (requiere token con id_rol = 1)**
- Parámetro de ruta: `id_red` = 1


{
  "nombre": "Tecnologías de la Información y Comunicación"
}


DELETE /redes_conocimiento/eliminar-por-id/{id_red}
**Eliminar red (requiere token con id_rol = 1)**
- Parámetro de ruta: `id_red` = 1


📋 REGISTRO CALIFICADO (/registro_calificado)

POST /registro_calificado/registrar
**Crear registro calificado (requiere token con id_rol = 1)**


{
  "cod_programa": 12345,
  "tipo_tramite": "Registro Calificado",
  "fecha_radicado": "2024-01-15",
  "numero_resolucion": 12345,
  "fecha_resolucion": "2024-02-20",
  "fecha_vencimiento": "2029-02-20",
  "vigencia": "5 años",
  "modalidad": "Presencial",
  "clasificacion": "Técnico",
  "estado_catalogo": true
}


GET /registro_calificado/obtener-por-cod_programa/{cod_programa}
**Obtener registro por código de programa**
- Parámetro de ruta: `cod_programa` = 12345

GET /registro_calificado/obtener-todos
**Obtener todos los registros calificados**
- No requiere parámetros

PUT /registro_calificado/editar/{cod_programa}
**Editar registro calificado (requiere token con id_rol = 1)**
- Parámetro de ruta: `cod_programa` = 12345

{
  "tipo_tramite": "Renovación de Registro Calificado",
  "vigencia": "7 años",
  "estado_catalogo": true
}


DELETE /registro_calificado/eliminar/{cod_programa}
**Eliminar registro calificado (requiere token con id_rol = 1)**
- Parámetro de ruta: `cod_programa` = 12345



INDICADORES DE PROGRAMA (/indicadores_programa)

POST /indicadores_programa/registrar
**Crear indicadores (requiere token con id_rol = 1)**


{
  "cod_programa": 12345,
  "indig_despl_viol_apr_tot": 5,
  "afro_despl_viol_apr_tot": 10,
  "despl_viol_apr_tot": 15,
  "discap_apr_tot": 8,
  "despojo_apr_tot": 2,
  "act_grup_arm_apr_tot": 1,
  "amenaza_apr_tot": 3,
  "del_sex_apr_tot": 0,
  "desap_forz_apr_tot": 0,
  "homi_masac_apr_tot": 0,
  "minas_exp_apr_tot": 0,
  "secuestro_apr_tot": 0,
  "tortura_apr_tot": 0,
  "uso_men_grup_arm_apr_tot": 0,
  "herido_apr_tot": 1,
  "reclut_forz_apr_tot": 0,
  "negro_apr_tot": 12,
  "afro_apr_tot": 15,
  "palenq_apr_tot": 0,
  "raizal_apr_tot": 0,
  "discap_aud_apr_tot": 2,
  "discap_vis_apr_tot": 1,
  "discap_fis_apr_tot": 3,
  "discap_int_apr_tot": 1,
  "discap_psico_apr_tot": 1,
  "discap_mult_apr_tot": 0,
  "sordoceg_apr_tot": 0,
  "despl_fen_nat_apr_tot": 4,
  "despl_fen_nat_cab_fam_apr_tot": 2,
  "adol_conf_ley_apr_tot": 0,
  "adol_trab_apr_tot": 5,
  "indig_apr_tot": 8,
  "inpec_apr_tot": 0,
  "jov_vuln_apr_tot": 20,
  "muj_cabfam_apr_tot": 15,
  "proc_reint_apr_tot": 0,
  "ado_desv_gr_arm_tot": 0,
  "rem_pal_tot": 0,
  "sob_min_ant_tot": 0,
  "sold_camp_tot": 0,
  "terc_edad_tot": 3,
  "rom_tot": 0,
  "camp_tot": 25,
  "ning_tot": 30,
  "artes_tot": 2,
  "empr_tot": 5,
  "mic_emp_tot": 8,
  "rem_cie_tot": 0,
  "gran_total": 150
}


GET /indicadores_programa/obtener-por-id/{cod_programa}
**Obtener indicadores por código de programa**
- Parámetro de ruta: `cod_programa` = 12345

PUT /indicadores_programa/editar/{cod_programa}
**Editar indicadores (requiere token con id_rol = 1)**
- Parámetro de ruta: `cod_programa` = 12345


{
  "gran_total": 200,
  "camp_tot": 30,
  "jov_vuln_apr_tot": 25
}


DELETE /indicadores_programa/eliminar/{cod_programa}
**Eliminar indicadores (requiere token con id_rol = 1)**
- Parámetro de ruta: `cod_programa` = 12345



CENTROS (/centro)

POST /centro/registrar
**Crear centro**


{
  "nombre_centro": "Centro de Formación Regional Norte",
  "cod_centro": 1001
}




