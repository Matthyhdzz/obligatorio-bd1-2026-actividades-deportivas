from conexion_estudiante import obtener_conexion


def solicitar_id_estudiante():
    while True:
        id_estudiante = input("Ingrese su ID de estudiante: ").strip()

        if id_estudiante.isdigit():
            return int(id_estudiante)

        print("El ID debe ser numérico.")


def validar_estudiante_activo(id_estudiante):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT id_estudiante, nombre, apellido
        FROM estudiantes
        WHERE id_estudiante = %s
          AND estado = 'activo';
    """

    cursor.execute(consulta, (id_estudiante,))
    estudiante = cursor.fetchone()

    cursor.close()
    conexion.close()

    return estudiante


def ver_actividades_disponibles():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT a.id_actividad,a.nombre,d.nombre AS disciplina,e.nombre AS espacio,a.dia_semana,a.hora_inicio,a.hora_fin,a.cupo_maximo,COUNT(i.id_inscripcion) AS confirmados,a.cupo_maximo - COUNT(i.id_inscripcion) AS cupos_disponibles
        FROM actividades a
        JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
        JOIN espacios e ON a.id_espacio = e.id_espacio
        LEFT JOIN inscripciones i 
            ON a.id_actividad = i.id_actividad 
            AND i.estado = 'confirmada'
        WHERE a.estado = 'abierta'
        GROUP BY a.id_actividad,a.nombre,d.nombre,e.nombre,a.dia_semana,a.hora_inicio,a.hora_fin,a.cupo_maximo
        ORDER BY a.id_actividad;
    """

    cursor.execute(consulta)
    actividades = cursor.fetchall()

    print("\nActividades disponibles")

    if not actividades:
        print("No hay actividades disponibles.")
    else:
        for actividad in actividades:
            print(
                f"ID: {actividad[0]} | {actividad[1]} | "
                f"Disciplina: {actividad[2]} | Espacio: {actividad[3]} | "
                f"Día: {actividad[4]} | Hora: {actividad[5]} - {actividad[6]} | "
                f"Cupo máximo: {actividad[7]} | Confirmados: {actividad[8]} | "
                f"Cupos disponibles: {actividad[9]}"
            )

    cursor.close()
    conexion.close()


def ver_mis_inscripciones(id_estudiante):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT i.id_inscripcion,a.nombre AS actividad,d.nombre AS disciplina,i.estado,i.fecha_inscripcion
        FROM inscripciones i
        JOIN actividades a ON i.id_actividad = a.id_actividad
        JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
        WHERE i.id_estudiante = %s
        ORDER BY i.fecha_inscripcion DESC;
    """

    cursor.execute(consulta, (id_estudiante,))
    inscripciones = cursor.fetchall()

    print("\nMis inscripciones")

    if not inscripciones:
        print("No tenés inscripciones registradas.")
    else:
        for inscripcion in inscripciones:
            print(
                f"ID inscripción: {inscripcion[0]} | "
                f"Actividad: {inscripcion[1]} | "
                f"Disciplina: {inscripcion[2]} | "
                f"Estado: {inscripcion[3]} | "
                f"Fecha: {inscripcion[4]}"
            )

    cursor.close()
    conexion.close()


def inscribirme_a_actividad(id_estudiante):
    id_actividad = input("Ingrese ID de la actividad: ").strip()

    if not id_actividad.isdigit():
        print("El ID de actividad debe ser numérico.")
        return

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        consulta_actividad = """
            SELECT id_actividad, cupo_maximo, estado
            FROM actividades
            WHERE id_actividad = %s;
        """

        cursor.execute(consulta_actividad, (id_actividad,))
        actividad = cursor.fetchone()

        if not actividad:
            print("La actividad no existe.")
            return

        if actividad[2] != "abierta":
            print("La actividad no se encuentra abierta para inscripciones.")
            return

        consulta_duplicado = """
            SELECT id_inscripcion
            FROM inscripciones
            WHERE id_estudiante = %s
              AND id_actividad = %s
              AND estado IN ('confirmada', 'lista_espera');
        """

        cursor.execute(consulta_duplicado, (id_estudiante, id_actividad))
        duplicado = cursor.fetchone()

        if duplicado:
            print("Ya tenés una inscripción activa o en lista de espera para esta actividad.")
            return

        consulta_confirmados = """
            SELECT COUNT(*)
            FROM inscripciones
            WHERE id_actividad = %s
              AND estado = 'confirmada';
        """

        cursor.execute(consulta_confirmados, (id_actividad,))
        cantidad_confirmados = cursor.fetchone()[0]

        cupo_maximo = actividad[1]

        if cantidad_confirmados < cupo_maximo:
            estado_inscripcion = "confirmada"
        else:
            estado_inscripcion = "lista_espera"

        consulta_insert = """
            INSERT INTO inscripciones (id_estudiante, id_actividad, estado, fecha_inscripcion)
            VALUES (%s, %s, %s, CURDATE());
    
        """

        cursor.execute(
            consulta_insert,
            (id_estudiante, id_actividad, estado_inscripcion)
        )

        conexion.commit()
        print(f"Inscripción realizada correctamente. Estado: {estado_inscripcion}")

    except Exception as e:
        conexion.rollback()
        print("Error al realizar la inscripción.")
        print(e)

    finally:
        cursor.close()
        conexion.close()


def cancelar_mi_inscripcion(id_estudiante):
    id_inscripcion = input("Ingrese ID de inscripción a cancelar: ").strip()

    if not id_inscripcion.isdigit():
        print("El ID de inscripción debe ser numérico.")
        return

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        consulta_inscripcion = """
            SELECT id_inscripcion, id_actividad, estado
            FROM inscripciones
            WHERE id_inscripcion = %s
              AND id_estudiante = %s
              AND estado IN ('confirmada', 'lista_espera');
        """

        cursor.execute(consulta_inscripcion, (id_inscripcion, id_estudiante))
        inscripcion = cursor.fetchone()

        if not inscripcion:
            print("No se encontró una inscripción activa tuya con ese ID.")
            return

        id_actividad = inscripcion[1]
        estado_anterior = inscripcion[2]

        consulta_cancelar = """
            UPDATE inscripciones
            SET estado = 'cancelada'
            WHERE id_inscripcion = %s
              AND id_estudiante = %s;
        """

        cursor.execute(consulta_cancelar, (id_inscripcion, id_estudiante))

        if estado_anterior == "confirmada":
            consulta_lista_espera = """
                SELECT id_inscripcion
                FROM inscripciones
                WHERE id_actividad = %s
                  AND estado = 'lista_espera'
                ORDER BY fecha_inscripcion ASC, id_inscripcion ASC
                LIMIT 1;
            """

            cursor.execute(consulta_lista_espera, (id_actividad,))
            siguiente = cursor.fetchone()

            if siguiente:
                consulta_promover = """
                    UPDATE inscripciones
                    SET estado = 'confirmada'
                    WHERE id_inscripcion = %s;
                """

                cursor.execute(consulta_promover, (siguiente[0],))

        conexion.commit()
        print("Inscripción cancelada correctamente.")

    except Exception as e:
        conexion.rollback()
        print("Error al cancelar inscripción.")
        print(e)

    finally:
        cursor.close()
        conexion.close()


def ver_mis_asistencias(id_estudiante):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT a.nombre AS actividad,asi.fecha,asi.estado,asi.observacion
        FROM asistencias asi
        JOIN inscripciones i ON asi.id_inscripcion = i.id_inscripcion
        JOIN actividades a ON i.id_actividad = a.id_actividad
        WHERE i.id_estudiante = %s
        ORDER BY asi.fecha DESC;
    """

    cursor.execute(consulta, (id_estudiante,))
    asistencias = cursor.fetchall()

    print("\nMis asistencias")

    if not asistencias:
        print("No tenés asistencias registradas.")
    else:
        for asistencia in asistencias:
            print(
                f"Actividad: {asistencia[0]} | "
                f"Fecha: {asistencia[1]} | "
                f"Estado: {asistencia[2]} | "
                f"Observación: {asistencia[3]}"
            )

    cursor.close()
    conexion.close()


def menu_estudiante():
    id_estudiante = solicitar_id_estudiante()
    estudiante = validar_estudiante_activo(id_estudiante)

    if not estudiante:
        print("No existe un estudiante activo con ese ID.")
        return

    while True:
        print("\nMenu estudiante")
        print("1. Ver actividades disponibles")
        print("2. Inscribirme a una actividad")
        print("3. Ver mis inscripciones")
        print("4. Darme de baja de una actividad")
        print("5. Ver mis asistencias")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_actividades_disponibles()
        elif opcion == "2":
            inscribirme_a_actividad(id_estudiante)
        elif opcion == "3":
            ver_mis_inscripciones(id_estudiante)
        elif opcion == "4":
            cancelar_mi_inscripcion(id_estudiante)
        elif opcion == "5":
            ver_mis_asistencias(id_estudiante)
        elif opcion == "0":
            print("Saliendo del sistema")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu_estudiante()