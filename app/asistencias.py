from conexion import obtener_conexion
from mysql.connector import Error
from datetime import datetime


ESTADOS_ASISTENCIA = ["presente", "ausente"]


def mostrar_menu_asistencias():
    print("\nRegistro de asistencias")
    print("1. Listar asistencias")
    print("2. Registrar asistencia")
    print("3. Modificar asistencia")
    print("4. Ver asistencias por actividad y fecha")
    print("0. Volver al menú principal")


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validar_estado_asistencia(estado):
    return estado in ESTADOS_ASISTENCIA


def listar_inscripciones_confirmadas():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT i.id_inscripcion,e.nombre,e.apellido,e.documento,a.nombre AS actividad
            FROM inscripciones i
            JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            JOIN actividades a ON i.id_actividad = a.id_actividad
            WHERE i.estado = 'confirmada'
            ORDER BY a.nombre, e.apellido, e.nombre;
        """

        cursor.execute(consulta)
        inscripciones = cursor.fetchall()

        if len(inscripciones) == 0:
            print("\nNo hay inscripciones confirmadas.")
        else:
            print("\n--- INSCRIPCIONES CONFIRMADAS ---")
            for inscripcion in inscripciones:
                print(f"{inscripcion[0]}. {inscripcion[1]} {inscripcion[2]} - Documento: {inscripcion[3]} - Actividad: {inscripcion[4]}")

        cursor.close()

    except Error as e:
        print("Error al listar inscripciones confirmadas:", e)

    finally:
        conexion.close()


def listar_asistencias():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT asi.id_asistencia,asi.fecha,asi.estado,asi.observacion,e.nombre,e.apellido,e.documento,act.nombre AS actividad
            FROM asistencias asi
            JOIN inscripciones i ON asi.id_inscripcion = i.id_inscripcion
            JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            JOIN actividades act ON i.id_actividad = act.id_actividad
            ORDER BY asi.fecha DESC, act.nombre, e.apellido;
        """

        cursor.execute(consulta)
        asistencias = cursor.fetchall()

        if len(asistencias) == 0:
            print("\nNo hay asistencias registradas.")
        else:
            print("\n--- LISTADO DE ASISTENCIAS ---")
            for asistencia in asistencias:
                print(f"ID asistencia: {asistencia[0]}")
                print(f"Fecha: {asistencia[1]}")
                print(f"Estado: {asistencia[2]}")
                print(f"Observación: {asistencia[3]}")
                print(f"Estudiante: {asistencia[4]} {asistencia[5]}")
                print(f"Documento: {asistencia[6]}")
                print(f"Actividad: {asistencia[7]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al listar asistencias:", e)

    finally:
        conexion.close()


def registrar_asistencia():
    print("\nRegistrar asistencias")

    listar_inscripciones_confirmadas()

    try:
        id_inscripcion = int(input("ID de inscripción confirmada: "))
    except ValueError:
        print("El ID de inscripción debe ser numérico.")
        return

    fecha = input("Fecha de asistencia (YYYY-MM-DD): ").strip()

    if not validar_fecha(fecha):
        print("La fecha debe tener formato YYYY-MM-DD.")
        return

    estado = input("Estado (presente/ausente): ").strip().lower()

    if not validar_estado_asistencia(estado):
        print("Estado inválido. Debe ser 'presente' o 'ausente'.")
        return

    observacion = input("Observación opcional: ").strip()

    if observacion == "":
        observacion = None

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta_inscripcion = """
            SELECT id_inscripcion
            FROM inscripciones
            WHERE id_inscripcion = %s
              AND estado = 'confirmada';
        """

        cursor.execute(consulta_inscripcion, (id_inscripcion,))
        inscripcion = cursor.fetchone()

        if inscripcion is None:
            print("La inscripción no existe o no está confirmada.")
            cursor.close()
            return

        consulta_existente = """
            SELECT id_asistencia
            FROM asistencias
            WHERE id_inscripcion = %s
              AND fecha = %s;
        """

        cursor.execute(consulta_existente, (id_inscripcion, fecha))
        asistencia_existente = cursor.fetchone()

        if asistencia_existente is not None:
            print("Ya existe una asistencia registrada para esa inscripción en esa fecha.")
            cursor.close()
            return

        consulta_insert = """
            INSERT INTO asistencias (id_inscripcion,fecha,estado,observacion)
            VALUES (%s, %s, %s, %s);
        """

        cursor.execute(consulta_insert, (id_inscripcion, fecha, estado, observacion))
        conexion.commit()

        print("Asistencia registrada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al registrar asistencia:", e)
        conexion.rollback()

    finally:
        conexion.close()


def modificar_asistencia():
    print("\nModificar asistencia")

    try:
        id_asistencia = int(input("Ingrese ID de asistencia: "))
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
            SELECT fecha, estado, observacion
            FROM asistencias
            WHERE id_asistencia = %s;
        """

        cursor.execute(consulta_busqueda, (id_asistencia,))
        asistencia = cursor.fetchone()

        if asistencia is None:
            print("No existe una asistencia con ese ID.")
            cursor.close()
            return

        print("\nDejar vacio en caso de no modificar")

        nueva_fecha = input(f"Fecha actual ({asistencia[0]}): ").strip()
        nuevo_estado = input(f"Estado actual ({asistencia[1]}): ").strip().lower()
        nueva_observacion = input(f"Observación actual ({asistencia[2]}): ").strip()

        fecha = nueva_fecha if nueva_fecha != "" else asistencia[0]
        estado = nuevo_estado if nuevo_estado != "" else asistencia[1]
        observacion = nueva_observacion if nueva_observacion != "" else asistencia[2]

        if not validar_fecha(str(fecha)):
            print("La fecha debe tener formato YYYY-MM-DD.")
            cursor.close()
            return

        if not validar_estado_asistencia(estado):
            print("Estado inválido. Debe ser 'presente' o 'ausente'.")
            cursor.close()
            return

        consulta_update = """
            UPDATE asistencias
            SET fecha = %s,
                estado = %s,
                observacion = %s
            WHERE id_asistencia = %s;
        """

        cursor.execute(consulta_update, (fecha, estado, observacion, id_asistencia))
        conexion.commit()

        print("Asistencia modificada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al modificar asistencia:", e)
        conexion.rollback()

    finally:
        conexion.close()


def ver_asistencias_por_actividad_y_fecha():
    print("\n Asistencia por actividad y fecha")

    try:
        id_actividad = int(input("Ingrese ID de la actividad: "))
    except ValueError:
        print("El ID de actividad debe ser numérico.")
        return

    fecha = input("Fecha (YYYY-MM-DD): ").strip()

    if not validar_fecha(fecha):
        print("La fecha debe tener formato YYYY-MM-DD.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT e.documento,e.nombre,e.apellido,asi.estado,asi.observacion
            FROM asistencias asi
            JOIN inscripciones i ON asi.id_inscripcion = i.id_inscripcion
            JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            WHERE i.id_actividad = %s
              AND asi.fecha = %s
            ORDER BY e.apellido, e.nombre;
        """

        cursor.execute(consulta, (id_actividad, fecha))
        asistencias = cursor.fetchall()

        if len(asistencias) == 0:
            print("No hay asistencias registradas para esa actividad en esa fecha.")
        else:
            print("\n Resultado")
            for asistencia in asistencias:
                print(f"Estudiante: {asistencia[1]} {asistencia[2]}")
                print(f"Documento: {asistencia[0]}")
                print(f"Estado: {asistencia[3]}")
                print(f"Observación: {asistencia[4]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al consultar asistencias:", e)

    finally:
        conexion.close()


def menu_asistencias():
    opcion = ""

    while opcion != "0":
        mostrar_menu_asistencias()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_asistencias()
        elif opcion == "2":
            registrar_asistencia()
        elif opcion == "3":
            modificar_asistencia()
        elif opcion == "4":
            ver_asistencias_por_actividad_y_fecha()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")