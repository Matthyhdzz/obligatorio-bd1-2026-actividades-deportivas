# Sistema de Gestión de Actividades Deportivas Universitarias

## Descripción

Este proyecto corresponde al obligatorio de Bases de Datos 1.
El sistema permite administrar las inscripciones de estudiantes a actividades deportivas universitarias, controlando cupos, estados de inscripción, lista de espera y registro de asistencias.

La aplicación fue desarrollada en Python utilizando conexión directa a una base de datos MySQL. Todas las operaciones sobre la base de datos fueron realizadas mediante consultas SQL.

## Tecnologías utilizadas

* Python
* MySQL
* mysql-connector (Python)
* DataGrip
* PyCharm

## Funcionalidades principales

El sistema permite:

* ABM de estudiantes.
* ABM de disciplinas deportivas.
* ABM de espacios deportivos.
* ABM de actividades deportivas.
* Gestión de inscripciones.
* Manejo de cupos y lista de espera.
* Registro de asistencias.
* Consulta de reportes.

## Reglas de negocio implementadas

El sistema controla que:

* Solo se puedan realizar inscripciones en actividades abiertas.
* No se supere el cupo máximo de una actividad.
* Si no hay cupo disponible, la inscripción quede en lista de espera.
* Un estudiante no pueda inscribirse más de una vez a la misma actividad.
* Solo se registre asistencia de estudiantes con inscripción confirmada.
* Una actividad cancelada o finalizada no acepte nuevas inscripciones.

## Estructura del proyecto

```text
obligatorio-bd1-2026-matias-hernandez/
│
├── app/
│   ├── actividades.py
│   ├── asistencias.py
│   ├── conexion.py
│   ├── disciplinas.py
│   ├── espacios.py
│   ├── estudiantes.py
│   ├── inscripciones.py
│   ├── main.py
│   └── reportes.py
│
├── docs/
│   ├── Instructivo - Obligatorio 2026.md
│   ├── Informe - Obligatorio 2026, Matias Hernandez.docx
│   └── Obligatorio BD 1 2026_1.pdf
│
├── sql/
│   ├── base_tablas.sql
│   ├── datos_inserts.sql
│   └── consultas_reportes.sql
│
├── .gitignore
├── README.md
└── requirements.txt
```


## Scripts SQL

En la carpeta `sql` se encuentran los scripts necesarios para crear y probar la base de datos:

* `base_tablas.sql`: crea la base de datos y las tablas.
* `datos_inserts.sql`: carga datos maestros iniciales.
* `consultas_reportes`: contiene las consultas SQL solicitadas y tres consultas adicionales.

## Reportes implementados

El sistema permite obtener:

1. Actividades con mayor cantidad de inscriptos confirmados.
2. Actividades con cupos disponibles.
3. Cantidad de inscriptos por disciplina deportiva.
4. Cantidad de inscriptos por carrera y facultad.
5. Porcentaje de ocupación de cada actividad.
6. Porcentaje de asistencia por actividad.
7. Estudiantes con tres o más inasistencias registradas.
8. Actividades con estudiantes en lista de espera.
9. Estudiantes inscriptos en más de una actividad.
10. Actividades sin inscriptos confirmados.



## Instructivo de ejecución

El instructivo detallado para ejecutar la aplicación localmente se encuentra en la carpeta `docs`

```text
docs/Instructivo - Obligatorio 2026.md
```

