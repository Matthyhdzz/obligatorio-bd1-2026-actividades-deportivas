from conexion import obtener_conexion
from mysql.connector import Error


def mostrar_menu_inscripciones():
    print("\n===== GESTIÓN DE INSCRIPCIONES =====")
    print("1. Listar inscripciones")
    print("2. Inscribir estudiante a actividad")
    print("3. Cancelar inscripción")
    print("4. Ver lista de espera por actividad")
    print("0. Volver al menú principal")


def listar_inscripciones():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT 
                i.id_inscripcion,
                e.documento,
                e.nombre,
                e.apellido,
                a.nombre AS actividad,
                i.fecha_inscripcion,
                i.estado
            FROM inscripciones i
            JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            JOIN actividades a ON i.id_actividad = a.id_actividad
            ORDER BY i.id_inscripcion;
        """

        cursor.execute(consulta)
        inscripciones = cursor.fetchall()

        if len(inscripciones) == 0:
            print("\nNo hay inscripciones registradas.")
        else:
            print("\n--- LISTADO DE INSCRIPCIONES ---")
            for inscripcion in inscripciones:
                print(f"ID inscripción: {inscripcion[0]}")
                print(f"Estudiante: {inscripcion[2]} {inscripcion[3]}")
                print(f"Documento: {inscripcion[1]}")
                print(f"Actividad: {inscripcion[4]}")
                print(f"Fecha inscripción: {inscripcion[5]}")
                print(f"Estado: {inscripcion[6]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al listar inscripciones:", e)

    finally:
        conexion.close()


def listar_estudiantes_activos():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT id_estudiante, documento, nombre, apellido
            FROM estudiantes
            WHERE estado = 'activo'
            ORDER BY apellido, nombre;
        """

        cursor.execute(consulta)
        estudiantes = cursor.fetchall()

        print("\n--- ESTUDIANTES ACTIVOS ---")
        for estudiante in estudiantes:
            print(f"{estudiante[0]}. {estudiante[2]} {estudiante[3]} - Documento: {estudiante[1]}")

        cursor.close()

    except Error as e:
        print("Error al listar estudiantes:", e)

    finally:
        conexion.close()


def listar_actividades_abiertas():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT 
                a.id_actividad,
                a.nombre,
                a.cupo_maximo,
                COUNT(i.id_inscripcion) AS confirmados,
                a.estado
            FROM actividades a
            LEFT JOIN inscripciones i 
                ON a.id_actividad = i.id_actividad
                AND i.estado = 'confirmada'
            WHERE a.estado = 'abierta'
            GROUP BY a.id_actividad, a.nombre, a.cupo_maximo, a.estado
            ORDER BY a.id_actividad;
        """

        cursor.execute(consulta)
        actividades = cursor.fetchall()

        print("\n--- ACTIVIDADES ABIERTAS ---")
        for actividad in actividades:
            cupos_disponibles = actividad[2] - actividad[3]
            print(f"{actividad[0]}. {actividad[1]} - Cupo: {actividad[3]}/{actividad[2]} - Disponibles: {cupos_disponibles}")

        cursor.close()

    except Error as e:
        print("Error al listar actividades abiertas:", e)

    finally:
        conexion.close()


def inscribir_estudiante():
    print("\n--- INSCRIBIR ESTUDIANTE A ACTIVIDAD ---")

    listar_estudiantes_activos()

    try:
        id_estudiante = int(input("ID del estudiante: "))
    except ValueError:
        print("El ID del estudiante debe ser numérico.")
        return

    listar_actividades_abiertas()

    try:
        id_actividad = int(input("ID de la actividad: "))
    except ValueError:
        print("El ID de la actividad debe ser numérico.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta_estudiante = """
            SELECT id_estudiante
            FROM estudiantes
            WHERE id_estudiante = %s AND estado = 'activo';
        """

        cursor.execute(consulta_estudiante, (id_estudiante,))
        estudiante = cursor.fetchone()

        if estudiante is None:
            print("El estudiante no existe o no está activo.")
            cursor.close()
            return

        consulta_actividad = """
            SELECT id_actividad, cupo_maximo, estado
            FROM actividades
            WHERE id_actividad = %s;
        """

        cursor.execute(consulta_actividad, (id_actividad,))
        actividad = cursor.fetchone()

        if actividad is None:
            print("La actividad no existe.")
            cursor.close()
            return

        cupo_maximo = actividad[1]
        estado_actividad = actividad[2]

        if estado_actividad != "abierta":
            print("No se puede inscribir en una actividad que no está abierta.")
            cursor.close()
            return

        consulta_duplicado = """
            SELECT id_inscripcion, estado
            FROM inscripciones
            WHERE id_estudiante = %s
              AND id_actividad = %s
              AND estado <> 'cancelada';
        """

        cursor.execute(consulta_duplicado, (id_estudiante, id_actividad))
        inscripcion_existente = cursor.fetchone()

        if inscripcion_existente is not None:
            print("El estudiante ya tiene una inscripción activa o en lista de espera para esta actividad.")
            cursor.close()
            return

        consulta_confirmados = """
            SELECT COUNT(*)
            FROM inscripciones
            WHERE id_actividad = %s
              AND estado = 'confirmada';
        """

        cursor.execute(consulta_confirmados, (id_actividad,))
        cantidad_confirmados = cursor.fetchone()[0]

        if cantidad_confirmados < cupo_maximo:
            estado_inscripcion = "confirmada"
        else:
            estado_inscripcion = "lista_espera"

        consulta_insert = """
            INSERT INTO inscripciones (
                id_estudiante,
                id_actividad,
                fecha_inscripcion,
                estado
            )
            VALUES (%s, %s, CURDATE(), %s);
        """

        cursor.execute(consulta_insert, (id_estudiante, id_actividad, estado_inscripcion))
        conexion.commit()

        if estado_inscripcion == "confirmada":
            print("Inscripción realizada correctamente. Estado: confirmada.")
        else:
            print("La actividad no tiene cupos disponibles. El estudiante quedó en lista de espera.")

        cursor.close()

    except Error as e:
        print("Error al realizar la inscripción:", e)
        conexion.rollback()

    finally:
        conexion.close()


def promover_lista_espera(cursor, id_actividad):
    consulta_lista_espera = """
        SELECT id_inscripcion
        FROM inscripciones
        WHERE id_actividad = %s
          AND estado = 'lista_espera'
        ORDER BY fecha_inscripcion, id_inscripcion
        LIMIT 1;
    """

    cursor.execute(consulta_lista_espera, (id_actividad,))
    siguiente = cursor.fetchone()

    if siguiente is not None:
        id_inscripcion_siguiente = siguiente[0]

        consulta_update = """
            UPDATE inscripciones
            SET estado = 'confirmada'
            WHERE id_inscripcion = %s;
        """

        cursor.execute(consulta_update, (id_inscripcion_siguiente,))
        print("Se promovió automáticamente a un estudiante de la lista de espera.")


def cancelar_inscripcion():
    print("\n--- CANCELAR INSCRIPCIÓN ---")

    try:
        id_inscripcion = int(input("Ingrese ID de la inscripción: "))
    except ValueError:
        print("El ID debe ser numérico.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta_busqueda = """
            SELECT id_actividad, estado
            FROM inscripciones
            WHERE id_inscripcion = %s;
        """

        cursor.execute(consulta_busqueda, (id_inscripcion,))
        inscripcion = cursor.fetchone()

        if inscripcion is None:
            print("No existe una inscripción con ese ID.")
            cursor.close()
            return

        id_actividad = inscripcion[0]
        estado_actual = inscripcion[1]

        if estado_actual == "cancelada":
            print("La inscripción ya se encuentra cancelada.")
            cursor.close()
            return

        consulta_cancelar = """
            UPDATE inscripciones
            SET estado = 'cancelada'
            WHERE id_inscripcion = %s;
        """

        cursor.execute(consulta_cancelar, (id_inscripcion,))

        if estado_actual == "confirmada":
            promover_lista_espera(cursor, id_actividad)

        conexion.commit()

        print("Inscripción cancelada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al cancelar inscripción:", e)
        conexion.rollback()

    finally:
        conexion.close()


def ver_lista_espera_por_actividad():
    print("\n--- LISTA DE ESPERA POR ACTIVIDAD ---")

    try:
        id_actividad = int(input("Ingrese ID de la actividad: "))
    except ValueError:
        print("El ID debe ser numérico.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT 
                i.id_inscripcion,
                e.documento,
                e.nombre,
                e.apellido,
                i.fecha_inscripcion
            FROM inscripciones i
            JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            WHERE i.id_actividad = %s
              AND i.estado = 'lista_espera'
            ORDER BY i.fecha_inscripcion, i.id_inscripcion;
        """

        cursor.execute(consulta, (id_actividad,))
        lista_espera = cursor.fetchall()

        if len(lista_espera) == 0:
            print("No hay estudiantes en lista de espera para esta actividad.")
        else:
            print("\n--- ESTUDIANTES EN LISTA DE ESPERA ---")
            for inscripcion in lista_espera:
                print(f"ID inscripción: {inscripcion[0]}")
                print(f"Estudiante: {inscripcion[2]} {inscripcion[3]}")
                print(f"Documento: {inscripcion[1]}")
                print(f"Fecha inscripción: {inscripcion[4]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al consultar lista de espera:", e)

    finally:
        conexion.close()


def menu_inscripciones():
    opcion = ""

    while opcion != "0":
        mostrar_menu_inscripciones()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_inscripciones()
        elif opcion == "2":
            inscribir_estudiante()
        elif opcion == "3":
            cancelar_inscripcion()
        elif opcion == "4":
            ver_lista_espera_por_actividad()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")