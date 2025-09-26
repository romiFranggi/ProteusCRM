## INTRODUCCION

Este proyecto es un CRM desarrollado con **Django**.

Se priorizó la entrega de funcionalidades clave y la interfaz gráfica, siguiendo este flujo de desarrollo:

1. **Prioridad en las tareas:** Decidi enfocarme primero en la conexión con la base de datos, el cálculo de métricas y la visualización de datos en el dashboard, para luego seguir con los filtros y snapshots, dejando la interfaz gráfica sencilla por falta de tiempo.  
2. **Elección de Django ORM:** Opte por utilizar directamente **Django ORM** para interactuar con la base de datos, en lugar de desarrollar una API separada, con el objetivo de simplificar la gestión de datos y acelerar el desarrollo.
3. **Persistencia de datos:**
   - La base de datos utilizada fue la proporcionada para la prueba
   -  Se aseguró la integración correcta de la base de datos con Django a través del ORM, manteniendo la integridad y consistencia de los datos existentes.  
   - Se creó una tabla adicional para los snapshots desde Django para registrar información específica generada por la aplicación, asegurando que se guarde correctamente en la base de datos.  
4. **Flujo de trabajo:**  
   - Descargar la base de datos y analizar las tablas y los datos de prueba.  
   - Configurar la conexión de Python con MySQL.  
   - Implementar el cálculo de las métricas de contactabilidad y penetraciones.  
   - Desarrollar el dashboard que muestra los resultados de manera visual.  
   - Implementar filtros y snapshots para facilitar la navegación y el análisis de los datos.  

Aunque la interfaz gráfica es sencilla, permite visualizar y analizar las métricas de forma clara, priorizando la funcionalidad sobre el diseño visual.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## TECNOLOGIAS UTILIZADAS

- **Lenguaje de programación:** Python 3.10+  
- **Framework:** Django 5.2.6  
- **Base de datos:** MySQL 8.0 CE  
- **IDE:** PyCharm Community 2024.2.4  
- **Dependencias principales:** mysqlclient, sqlparse, python-dateutil, pytz, Django  
- **Control de versiones:** GitHub
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## INSTALACION Y EJECUCION

### 1. Clonar el repositorio
- Abrir PyCharm Community 2024.2.4 y seleccionar **Get from Version Control**.  puede ser en cualquier ide.
- Pegar la URL del repositorio:  https://github.com/romiFranggi/ProteusCRM.git
- Seleccionar la carpeta donde se quiere clonar el proyecto y hacer clic en **Clone**.

### 2. Crear y activar entorno virtual
- Al abrir el proyecto, PyCharm sugerira crear un **entorno virtual (venv)**. Aceptá la sugerencia.  
- Si no se crea automáticamente, abrir la terminal de PyCharm dentro del proyecto y ejecutá:
python -m venv venv

-Activar el entorno virtual en la terminal:
.\venv\Scripts\Activate.ps1  (para windows)

### 3. Instalar dependencias
Con el entorno virtual activado, ejecutar:
pip install -r requirements.txt

### 4. Configurar la base de datos MySQL
-Abrir MySQL Workbench 8.0 CE y crear una base de datos para el proyecto.

-Copiar el nombre de la base de datos, usuario y contraseña.

-Editar el archivo settings.py de tu proyecto Django y reemplazá los datos en la sección DATABASES:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

### 5. Aplicar migracion (OPCIONAL)
en mi caso use prueba_tecnica_estructura_db.sql sin hacerle cambios.
-en la terminal: 
python manage.py migrate

### 7. Ejecutar proyecto

-python manage.py runserver
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## USUARIO DEMO PARA LOGUEARSE
usuario: amartinez
contraseña: hashabc
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## DATOS DE EJEMPLO Y FLUJO DEL SISTEMA

La aplicación incluye un botón en la interfaz que permite guardar snapshots de prueba en la tabla correspondiente (creada con Django en models.py)

Para generar los datos de ejemplo:

-Ejecutar el proyecto (python manage.py runserver).
-Abrir el navegador en http://127.0.0.1:8000.
-Loguearse con el usuario de un supervisor.
-Una vez ingresado al dashboard , seleccionar filtros (opcional)
-En caso de seleccionar filtros, presionar el boton "Aplicar filtros", si no se presiona no habrá cambios en los datos ni en los snapshots que se guarden
-Hacer clic en el botón “Guardar snapshot”.

Esto llenará la tabla con registros de snapshots de ejemplo, permitiendo probar la funcionalidad de la aplicación sin necesidad de cargar manualmente la base de datos.

La interfaz tambien contiene boton para resetear los filtros, volviendo a los datos normales, y otro para ver el historial de snapshots guardados.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## CALCULO DE METRICAS:

Contactabilidad % =  (Gestiones efectivas / Total gestiones) * 100


Penetración Bruta % =  (Gestiones exitosas / Total gestiones) * 100


Penetración Neta % =  (Gestiones exitosas / Gestiones efectivas) * 100

-----> IMPORTANTE <-----

En este contexto las gestiones EFECTIVAS (cualquier intento de llamada de un agente donde se logra hablar con alguien), asumo que son:
Coordinado, Contactado, No interesado, Volver a llamar, Menor de edad, Ya tiene el servicio, Coordinar por mail, Encuesta completada.

y gestiones EXITOSAS asumo que son:
Coordinado, Agendado

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## EJEMPLOS DE CONSULTAS SQL


El siguiente script se utilizó para pruebas de métricas y snapshots en el proyecto:

```sql
CREATE DATABASE IF NOT EXISTS proteus_crm;
USE proteus_crm;

-- contactabilidad
SELECT 
    COUNT(*) AS total,
    SUM(CASE WHEN id_resultado IN (1,2,8,9,10,13,14,15,16) AND id_tipo = 1 THEN 1 ELSE 0 END) AS efectivas,
    ROUND(
        SUM(CASE WHEN id_resultado IN (1,2,8,9,10,13,14,15,16) AND id_tipo = 1 THEN 1 ELSE 0 END) 
        / COUNT(*) * 100, 2
    ) AS porcentaje_contactabilidad
FROM gestiones;

-- penetracion bruta
SELECT 
    COUNT(*) AS total_llamadas,
    SUM(CASE WHEN id_resultado IN (1,8) AND id_tipo = 1 THEN 1 ELSE 0 END) AS exitosas,
    ROUND(
        SUM(CASE WHEN id_resultado IN (1,8) AND id_tipo = 1 THEN 1 ELSE 0 END)
        / COUNT(*) * 100, 2
    ) AS porcentaje_penetracion_bruta
FROM gestiones
WHERE id_tipo = 1;

-- penetracion neta
SELECT 
    SUM(CASE WHEN id_resultado IN (1,2,8,9,10,13,14,15,16) AND id_tipo = 1 THEN 1 ELSE 0 END) AS efectivas,
    SUM(CASE WHEN id_resultado IN (1,8) AND id_tipo = 1 THEN 1 ELSE 0 END) AS exitosas,
    ROUND(
        SUM(CASE WHEN id_resultado IN (1,8) AND id_tipo = 1 THEN 1 ELSE 0 END)
        / SUM(CASE WHEN id_resultado IN (1,2,8,9,10,13,14,15,16) AND id_tipo = 1 THEN 1 ELSE 0 END) * 100, 2
    ) AS porcentaje_penetracion_neta
FROM gestiones;

-- comandos para eliminar todos los snapshots:
SET SQL_SAFE_UPDATES = 0;
DELETE FROM crm_dashboardsnapshot;
SET SQL_SAFE_UPDATES = 1;

-- Ver todos los snapshots guardados
SELECT 
    id,
    contactabilidad,
    penetracion_bruta,
    penetracion_neta,
    filtros,
    created_at
FROM crm_dashboardsnapshot
ORDER BY created_at DESC;

-- Ejemplo contactabilidad para un agente id 1 y campaña id 2
SELECT 
    COUNT(*) AS total,
    SUM(CASE WHEN id_resultado IN (1,2,8,9,10,13,14,15,16) AND id_tipo = 1 THEN 1 ELSE 0 END) AS efectivas,
    ROUND(
        SUM(CASE WHEN id_resultado IN (1,2,8,9,10,13,14,15,16) AND id_tipo = 1 THEN 1 ELSE 0 END) 
        / COUNT(*) * 100, 2
    ) AS porcentaje_contactabilidad
FROM gestiones
WHERE id_broker = 1
  AND id_campaign = 2;

-- Obtener todos los contactos de una campaña con resultado "No contesta"
SET @busqueda = 2;  
SELECT id_contacto
FROM gestiones
WHERE id_campaign = @busqueda  
  AND id_resultado = 2
ORDER BY timestamp;

-- Buscar contactos por CI o teléfono
SET @busqueda = 66666666;

SELECT 
    c.id AS contacto_id,
    c.ci,
    CONCAT(c.nombre1, ' ', c.nombre2, ' ', c.apellido1, ' ', c.apellido2) AS nombre_completo,
    t1.numero AS tel_fijo1,
    t2.numero AS tel_fijo2,
    t3.numero AS tel_movil1,
    t4.numero AS tel_movil2,
    c.email
FROM contactos c
LEFT JOIN telefonos t1 ON c.id_tel_fijo1 = t1.id
LEFT JOIN telefonos t2 ON c.id_tel_fijo2 = t2.id
LEFT JOIN telefonos t3 ON c.id_tel_movil1 = t3.id
LEFT JOIN telefonos t4 ON c.id_tel_movil2 = t4.id
WHERE c.ci = @busqueda
   OR t1.numero = @busqueda
   OR t2.numero = @busqueda
   OR t3.numero = @busqueda
   OR t4.numero = @busqueda;
