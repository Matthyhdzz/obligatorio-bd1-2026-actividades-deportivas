USE gestion_actividades_deportivas;


1. Actividades con mayor cantidad de inscriptos confirmados


SELECT 
    a.id_actividad,
    a.nombre AS actividad,
    COUNT(i.id_inscripcion) AS cantidad_confirmados
FROM actividades a
LEFT JOIN inscripciones i 
    ON a.id_actividad = i.id_actividad
    AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre
ORDER BY cantidad_confirmados DESC, a.nombre;



2. Actividades con cupos disponibles


SELECT 
    a.id_actividad,
    a.nombre AS actividad,
    a.cupo_maximo,
    COUNT(i.id_inscripcion) AS confirmados,
    a.cupo_maximo - COUNT(i.id_inscripcion) AS cupos_disponibles
FROM actividades a
LEFT JOIN inscripciones i 
    ON a.id_actividad = i.id_actividad
    AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
HAVING cupos_disponibles > 0
ORDER BY cupos_disponibles DESC, a.nombre;


3. Cantidad de inscriptos por disciplina deportiva

SELECT 
    d.id_disciplina,
    d.nombre AS disciplina,
    COUNT(i.id_inscripcion) AS cantidad_confirmados
FROM disciplinas d
LEFT JOIN actividades a 
    ON d.id_disciplina = a.id_disciplina
LEFT JOIN inscripciones i 
    ON a.id_actividad = i.id_actividad
    AND i.estado = 'confirmada'
GROUP BY d.id_disciplina, d.nombre
ORDER BY cantidad_confirmados DESC, d.nombre;


4. Cantidad de inscriptos por carrera y facultad


SELECT 
    f.nombre AS facultad,
    c.nombre AS carrera,
    COUNT(i.id_inscripcion) AS cantidad_confirmados
FROM facultades f
JOIN carreras c 
    ON f.id_facultad = c.id_facultad
LEFT JOIN estudiantes e 
    ON c.id_carrera = e.id_carrera
LEFT JOIN inscripciones i 
    ON e.id_estudiante = i.id_estudiante
    AND i.estado = 'confirmada'
GROUP BY f.nombre, c.nombre
ORDER BY f.nombre, c.nombre;


5. Porcentaje de ocupación de cada actividad


SELECT 
    a.id_actividad,
    a.nombre AS actividad,
    a.cupo_maximo,
    COUNT(i.id_inscripcion) AS confirmados,
    ROUND((COUNT(i.id_inscripcion) / a.cupo_maximo) * 100, 2) AS porcentaje_ocupacion
FROM actividades a
LEFT JOIN inscripciones i 
    ON a.id_actividad = i.id_actividad
    AND i.estado = 'confirmada'
GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
ORDER BY porcentaje_ocupacion DESC, a.nombre;


6. Porcentaje de asistencia por actividad

SELECT 
    a.id_actividad,
    a.nombre AS actividad,
    COUNT(asi.id_asistencia) AS total_registros_asistencia,
    SUM(CASE WHEN asi.estado = 'presente' THEN 1 ELSE 0 END) AS presentes,
    ROUND(
        CASE 
            WHEN COUNT(asi.id_asistencia) = 0 THEN 0
            ELSE (SUM(CASE WHEN asi.estado = 'presente' THEN 1 ELSE 0 END) / COUNT(asi.id_asistencia)) * 100
        END,
        2
    ) AS porcentaje_asistencia
FROM actividades a
LEFT JOIN inscripciones i 
    ON a.id_actividad = i.id_actividad
LEFT JOIN asistencias asi 
    ON i.id_inscripcion = asi.id_inscripcion
GROUP BY a.id_actividad, a.nombre
ORDER BY porcentaje_asistencia DESC, a.nombre;


7. Estudiantes con tres o más inasistencias registradas


SELECT 
    e.id_estudiante,
    e.documento,
    e.nombre,
    e.apellido,
    COUNT(asi.id_asistencia) AS cantidad_inasistencias
FROM estudiantes e
JOIN inscripciones i 
    ON e.id_estudiante = i.id_estudiante
JOIN asistencias asi 
    ON i.id_inscripcion = asi.id_inscripcion
WHERE asi.estado = 'ausente'
GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
HAVING cantidad_inasistencias >= 3
ORDER BY cantidad_inasistencias DESC, e.apellido, e.nombre;


8. Consulta adicional 1:
Actividades con estudiantes en lista de espera


SELECT 
    a.id_actividad,
    a.nombre AS actividad,
    COUNT(i.id_inscripcion) AS cantidad_lista_espera
FROM actividades a
JOIN inscripciones i 
    ON a.id_actividad = i.id_actividad
WHERE i.estado = 'lista_espera'
GROUP BY a.id_actividad, a.nombre
ORDER BY cantidad_lista_espera DESC, a.nombre;


9. Consulta adicional 2:
Estudiantes inscriptos en más de una actividad


SELECT 
    e.id_estudiante,
    e.documento,
    e.nombre,
    e.apellido,
    COUNT(i.id_inscripcion) AS cantidad_actividades
FROM estudiantes e
JOIN inscripciones i 
    ON e.id_estudiante = i.id_estudiante
WHERE i.estado = 'confirmada'
GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
HAVING cantidad_actividades > 1
ORDER BY cantidad_actividades DESC, e.apellido, e.nombre;


10. Consulta adicional 3:
Actividades sin inscriptos confirmados


SELECT a.id_actividad,a.nombre AS actividad,a.estado
FROM actividades a
LEFT JOIN inscripciones i
    ON a.id_actividad = i.id_actividad
    AND i.estado = 'confirmada'
WHERE i.id_inscripcion IS NULL
ORDER BY a.nombre;