from conexion import obtener_conexion
from mysql.connector import Error


def mostrar_reportes():
    print("\nReportes")
    print("1. Actividades con mayor cantidad de inscriptos confirmados")
    print("2. Actividades con cupos disponibles")
    print("3. Cantidad de inscriptos por disciplina deportiva")
    print("4. Cantidad de inscriptos por carrera y facultad")
    print("5. Porcentaje de ocupación de cada actividad")
    print("6. Porcentaje de asistencia por actividad")
    print("7. Estudiantes con tres o más inasistencias")
    print("8. Actividades con estudiantes en lista de espera")
    print("9. Estudiantes inscriptos en más de una actividad")
    print("10. Actividades sin inscriptos confirmados")
    print("0. Volver al menú principal")


def actividades_mayor_cantidad_confirmados():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT a.id_actividad,a.nombre,COUNT(i.id_inscripcion) AS cantidad_confirmados
            FROM actividades a
            JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
                AND i.estado = 'confirmada'
            GROUP BY a.id_actividad, a.nombre
            ORDER BY cantidad_confirmados DESC;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()


        for fila in resultados:
            print(f"ID actividad: {fila[0]}")
            print(f"Actividad: {fila[1]}")
            print(f"Inscriptos confirmados: {fila[2]}")
            print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def actividades_con_cupos_disponibles():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT a.id_actividad,a.nombre,a.cupo_maximo,COUNT(i.id_inscripcion) AS confirmados,a.cupo_maximo - COUNT(i.id_inscripcion) AS cupos_disponibles
            FROM actividades a
            LEFT JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
                AND i.estado = 'confirmada'
            GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
            HAVING cupos_disponibles > 0
            ORDER BY cupos_disponibles DESC, a.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        for fila in resultados:
            print(f"ID actividad: {fila[0]}")
            print(f"Actividad: {fila[1]}")
            print(f"Cupo máximo: {fila[2]}")
            print(f"Confirmados: {fila[3]}")
            print(f"Cupos disponibles: {fila[4]}")
            print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def inscriptos_por_disciplina():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT d.id_disciplina,d.nombre,COUNT(i.id_inscripcion) AS cantidad_confirmados
            FROM disciplinas d
            LEFT JOIN actividades a 
                ON d.id_disciplina = a.id_disciplina
            LEFT JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
                AND i.estado = 'confirmada'
            GROUP BY d.id_disciplina, d.nombre
            ORDER BY cantidad_confirmados DESC, d.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()


        for fila in resultados:
            print(f"ID disciplina: {fila[0]}")
            print(f"Disciplina: {fila[1]}")
            print(f"Inscriptos confirmados: {fila[2]}")
            print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def inscriptos_por_carrera_y_facultad():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT f.nombre AS facultad,c.nombre AS carrera,COUNT(i.id_inscripcion) AS cantidad_confirmados
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
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nCantidad de inscipriptos confirmados")

        for fila in resultados:
            print(f"Facultad: {fila[0]}")
            print(f"Carrera: {fila[1]}")
            print(f"Inscriptos confirmados: {fila[2]}")
            print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def porcentaje_ocupacion_por_actividad():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT a.id_actividad,a.nombre,a.cupo_maximo,COUNT(i.id_inscripcion) AS confirmados,ROUND((COUNT(i.id_inscripcion) / a.cupo_maximo) * 100, 2) AS porcentaje_ocupacion
            FROM actividades a
            LEFT JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
                AND i.estado = 'confirmada'
            GROUP BY a.id_actividad, a.nombre, a.cupo_maximo
            ORDER BY porcentaje_ocupacion DESC, a.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nPorcentaje de ocupacion")

        for fila in resultados:
            print(f"ID actividad: {fila[0]}")
            print(f"Actividad: {fila[1]}")
            print(f"Cupo máximo: {fila[2]}")
            print(f"Confirmados: {fila[3]}")
            print(f"Ocupación: {fila[4]}%")
            print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def porcentaje_asistencia_por_actividad():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT a.id_actividad,a.nombre,COUNT(asi.id_asistencia) AS total_registros,SUM(CASE WHEN asi.estado = 'presente' THEN 1 ELSE 0 END) AS presentes,ROUND((SUM(CASE WHEN asi.estado = 'presente' THEN 1 ELSE 0 END) / COUNT(asi.id_asistencia)) * 100,2) AS porcentaje_asistencia
            FROM actividades a
            JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
            JOIN asistencias asi 
                ON i.id_inscripcion = asi.id_inscripcion
            GROUP BY a.id_actividad, a.nombre
            ORDER BY porcentaje_asistencia DESC, a.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nPorcentaje de asistencia segun actividad")

        if len(resultados) == 0:
            print("No hay asistencias registradas para calcular porcentajes.")
        else:
            for fila in resultados:
                print(f"ID actividad: {fila[0]}")
                print(f"Actividad: {fila[1]}")
                print(f"Total registros de asistencia: {fila[2]}")
                print(f"Presentes: {fila[3]}")
                print(f"Porcentaje de asistencia: {fila[4]}%")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def estudiantes_tres_o_mas_inasistencias():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT e.id_estudiante,e.documento,e.nombre,e.apellido,COUNT(asi.id_asistencia) AS cantidad_inasistencias
            FROM estudiantes e
            JOIN inscripciones i 
                ON e.id_estudiante = i.id_estudiante
            JOIN asistencias asi 
                ON i.id_inscripcion = asi.id_inscripcion
            WHERE asi.estado = 'ausente'
            GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
            HAVING cantidad_inasistencias >= 3
            ORDER BY cantidad_inasistencias DESC, e.apellido, e.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nEstudiantes con 3 o mas asistencias")

        if len(resultados) == 0:
            print("No hay estudiantes con tres o más inasistencias.")
        else:
            for fila in resultados:
                print(f"ID estudiante: {fila[0]}")
                print(f"Documento: {fila[1]}")
                print(f"Estudiante: {fila[2]} {fila[3]}")
                print(f"Inasistencias: {fila[4]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def actividades_con_lista_espera():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT a.id_actividad,a.nombre,COUNT(i.id_inscripcion) AS cantidad_lista_espera
            FROM actividades a
            JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
            WHERE i.estado = 'lista_espera'
            GROUP BY a.id_actividad, a.nombre
            ORDER BY cantidad_lista_espera DESC, a.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nActividades con estudiantes en lista de espera")

        if len(resultados) == 0:
            print("No hay actividades con estudiantes en lista de espera.")
        else:
            for fila in resultados:
                print(f"ID actividad: {fila[0]}")
                print(f"Actividad: {fila[1]}")
                print(f"Estudiantes en lista de espera: {fila[2]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def estudiantes_en_mas_de_una_actividad():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT e.id_estudiante,e.documento,e.nombre,e.apellido,COUNT(i.id_inscripcion) AS cantidad_actividades
            FROM estudiantes e
            JOIN inscripciones i 
                ON e.id_estudiante = i.id_estudiante
            WHERE i.estado = 'confirmada'
            GROUP BY e.id_estudiante, e.documento, e.nombre, e.apellido
            HAVING cantidad_actividades > 1
            ORDER BY cantidad_actividades DESC, e.apellido, e.nombre;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nEstudiantes inscriptos a mas de una actividad")

        if len(resultados) == 0:
            print("No hay estudiantes confirmados en más de una actividad.")
        else:
            for fila in resultados:
                print(f"ID estudiante: {fila[0]}")
                print(f"Documento: {fila[1]}")
                print(f"Estudiante: {fila[2]} {fila[3]}")
                print(f"Cantidad de actividades confirmadas: {fila[4]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()


def actividades_sin_inscriptos_confirmados():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT a.id_actividad,a.nombre as Actividad,a.estado
            FROM actividades a
            LEFT JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
                AND i.estado = 'confirmada'
            WHERE i.id_inscripcion IS NULL;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        print("\nActividades sin estudiantes inscriptos")

        if len(resultados) == 0:
            print("No hay actividades vacias")
        else:
            for fila in resultados:
                print(f"ID actividad: {fila[0]}")
                print(f"Actividad: {fila[1]}")
                print(f"Estado: {fila[2]}")

        cursor.close()

    except Error as e:
        print("Error al generar reporte:", e)

    finally:
        conexion.close()

def menu_reportes():
    opcion = ""

    while opcion != "0":
        mostrar_reportes()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            actividades_mayor_cantidad_confirmados()
        elif opcion == "2":
            actividades_con_cupos_disponibles()
        elif opcion == "3":
            inscriptos_por_disciplina()
        elif opcion == "4":
            inscriptos_por_carrera_y_facultad()
        elif opcion == "5":
            porcentaje_ocupacion_por_actividad()
        elif opcion == "6":
            porcentaje_asistencia_por_actividad()
        elif opcion == "7":
            estudiantes_tres_o_mas_inasistencias()
        elif opcion == "8":
            actividades_con_lista_espera()
        elif opcion == "9":
            estudiantes_en_mas_de_una_actividad()
        elif opcion == "10":
            actividades_sin_inscriptos_confirmados()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")