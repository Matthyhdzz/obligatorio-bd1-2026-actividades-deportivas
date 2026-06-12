# Instructivo de ejecución local

Este instructivo explica cómo ejecutar el sistema en una computadora local utilizando MySQL, DataGrip y PyCharm.

---

## 1. Abrir el proyecto

Abrir PyCharm y seleccionar la carpeta raíz del proyecto:

```text
obligatorio-bd1-2026-matias-hernandez
```

## 2. Verificar MySQL

Antes de ejecutar la aplicación, asegurarse de que el servicio de MySQL esté iniciado.

Luego abrir DataGrip y conectarse a MySQL con datos locales. Como ejemplo:

```text
Host: localhost
Puerto: 3306
Usuario: root
Contraseña: contraseña local de MySQL
```

---

## 3. Crear la base de datos

En DataGrip, abrir el archivo:

```text
sql/base_tablas.sql
```

Ejecutar el script completo.

Este script crea la base de datos:

```text
gestion_actividades_deportivas
```

y todas las tablas necesarias para el funcionamiento del sistema.

---

## 4. Cargar los datos iniciales

Luego de crear la base de datos, abrir y ejecutar el archivo:

```text
sql/datos_inserts.sql
```

Este script carga los datos iniciales del sistema, como facultades, carreras, disciplinas deportivas, espacios, actividades y estudiantes.

---

## 5. Verificar que la base se creó correctamente

En DataGrip, ejecutar:

```sql
USE gestion_actividades_deportivas;

SHOW TABLES;
```

Deben aparecer las siguientes tablas:

```text
actividades
asistencias
carreras
disciplinas
espacios
estudiantes
facultades
inscripciones
```

También se puede comprobar que los datos iniciales fueron cargados ejecutando:

```sql
SELECT * FROM estudiantes;
SELECT * FROM actividades;
SELECT * FROM disciplinas;
```

---

## 6. Instalar dependencias

Abrir la terminal de PyCharm en la raíz del proyecto y ejecutar:

```bash
py -m pip install -r instalador-mysql.txt
```

Si `pip` está configurado directamente, también puede utilizarse:

```bash
pip install -r instalador-mysql.txt
```

El archivo `instalador-mysql.txt` contiene la librería necesaria para conectar Python con MySQL.

---

## 7. Configurar la conexión a MySQL

Abrir el archivo:

```text
app/conexion.py
```

Dentro de ese archivo, modificar la contraseña de MySQL según corresponda:

```python
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="gestion_actividades_deportivas"
)
```

Cada usuario debe reemplazar:

```text
password
```

por la contraseña local de su instalación de MySQL.

No es necesario cambiar el nombre de la base de datos si se ejecutaron los scripts originales.

---

## 8. Ejecutar la aplicación

Abrir el archivo:

```text
app/main.py
```

Desde PyCharm, ejecutarlo con:

```text
Click derecho → Run 'main'
```

También puede ejecutarse desde terminal entrando a la carpeta `app`:

```bash
cd app
py main.py
```

O, si Python está configurado directamente:

```bash
python main.py
```

---

## 9. Uso básico del sistema

Al ejecutar la aplicación se muestra el menú principal:

```text
===== SISTEMA DE GESTIÓN =====

1. Gestión de estudiantes
2. Gestión de disciplinas deportivas
3. Gestión de espacios deportivos
4. Gestión de actividades deportivas
5. Gestión de inscripciones
6. Registro de asistencias
7. Reportes
0. Salir
```

Desde este menú se accede a las funcionalidades principales del sistema.

---

## 10. Prueba recomendada

Para verificar que el sistema funciona correctamente, se recomienda seguir este flujo:

1. Entrar a **Gestión de estudiantes** y listar estudiantes.
2. Entrar a **Gestión de disciplinas deportivas** y listar disciplinas.
3. Entrar a **Gestión de espacios deportivos** y listar espacios.
4. Entrar a **Gestión de actividades deportivas** y listar actividades.
5. Entrar a **Gestión de inscripciones** e inscribir un estudiante en una actividad abierta.
6. Entrar a **Registro de asistencias** y registrar asistencia para una inscripción confirmada.
7. Entrar a **Reportes** y ejecutar los reportes disponibles.

---

## 11. Consultas de reportes

Las consultas SQL solicitadas se encuentran en:

```text
consultas_reportes.sql
```

Ese archivo contiene los reportes obligatorios y tres consultas adicionales propuestas para el sistema.

---

## 12. Problemas frecuentes

### Error de conexión a MySQL

Si aparece un error de conexión, revisar el archivo:

```text
app/conexion.py
```

Verificar especialmente estos datos:

```python
host="localhost"
user="root"
password="PASSWORD"
database="gestion_actividades_deportivas"
```

También comprobar que MySQL esté iniciado.

---

### Error con pip

Si el comando `pip` no se reconoce en Windows, usar:

```bash
py -m pip install -r requirements.txt
```

---

### No aparecen las tablas

Si no aparecen las tablas, volver a ejecutar los scripts SQL en este orden:

```text
1. base_tablas.sql
2. datos_inserts.sql
```

---

### Algunos reportes aparecen vacíos

Algunos reportes dependen de que existan inscripciones, asistencias o inasistencias cargadas.

Por ejemplo, el reporte de estudiantes con tres o más inasistencias solo mostrará resultados si previamente se registraron al menos tres asistencias con estado `ausente` para un mismo estudiante.

Que un reporte aparezca vacío no significa necesariamente que esté mal; puede deberse a que todavía no hay datos suficientes cargados.

---

## 13. Consideraciones finales

La aplicación fue desarrollada en Python puro.

Todas las operaciones principales sobre la base de datos se realizan mediante consultas SQL. La información se almacena de forma persistente en MySQL.
