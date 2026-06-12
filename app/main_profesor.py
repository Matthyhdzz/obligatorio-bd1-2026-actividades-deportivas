from datetime import datetime
from conexion_profesor import obtener_conexion


def listar_estudiantes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT e.id_estudiante,e.documento,e.nombre,e.apellido,e.correo,c.nombre AS carrera,f.nombre AS facultad,e.estado
        FROM estudiantes e
        JOIN carreras c ON e.id_carrera = c.id_carrera
        JOIN facultades f ON c.id_facultad = f.id_facultad
        ORDER BY e.apellido, e.nombre;
    """

    cursor.execute(consulta)
    estudiantes = cursor.fetchall()

    print("\nEstudiantes listados")

    if not estudiantes:
        print("No hay estudiantes registrados.")
    else:
        for estudiante in estudiantes:
            print(
                f"ID: {estudiante[0]} | Documento: {estudiante[1]} | "
                f"Nombre: {estudiante[2]} {estudiante[3]} | "
                f"Correo: {estudiante[4]} | Carrera: {estudiante[5]} | "
                f"Facultad: {estudiante[6]} | Estado: {estudiante[7]}"
            )

    cursor.close()
    conexion.close()


def buscar_estudiante():
    documento = input("Ingrese documento del estudiante: ").strip()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT e.id_estudiante,e.documento,e.nombre,e.apellido,e.correo,c.nombre AS carrera,f.nombre AS facultad,e.estado
        FROM estudiantes e
        JOIN carreras c ON e.id_carrera = c.id_carrera
        JOIN facultades f ON c.id_facultad = f.id_facultad
        WHERE e.documento = %s;
    """

    cursor.execute(consulta, (documento,))
    estudiante = cursor.fetchone()

    print("\nBuscar estudiante")

    if estudiante:
        print(f"ID: {estudiante[0]}")
        print(f"Documento: {estudiante[1]}")
        print(f"Nombre: {estudiante[2]} {estudiante[3]}")
        print(f"Correo: {estudiante[4]}")
        print(f"Carrera: {estudiante[5]}")
        print(f"Facultad: {estudiante[6]}")
        print(f"Estado: {estudiante[7]}")
    else:
        print("No se encontró un estudiante con ese documento.")

    cursor.close()
    conexion.close()


def ver_actividades():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT a.id_actividad,a.nombre,d.nombre AS disciplina,e.nombre AS espacio,a.dia,a.hora_inicio,a.hora_fin,a.cupo_maximo,a.estado
        FROM actividades a
        JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
        JOIN espacios e ON a.id_espacio = e.id_espacio
        ORDER BY a.id_actividad;
    """

    cursor.execute(consulta)
    actividades = cursor.fetchall()

    print("\nActividades")

    if not actividades:
        print("No hay actividades registradas.")
    else:
        for actividad in actividades:
            print(
                f"ID: {actividad[0]} | {actividad[1]} | "
                f"Disciplina: {actividad[2]} | Espacio: {actividad[3]} | "
                f"Día: {actividad[4]} | Hora: {actividad[5]} - {actividad[6]} | "
                f"Cupo: {actividad[7]} | Estado: {actividad[8]}"
            )

    cursor.close()
    conexion.close()


def ver_inscriptos_por_actividad():
    id_actividad = input("Ingrese ID de la actividad: ").strip()

    if not id_actividad.isdigit():
        print("El ID debe ser numérico.")
        return

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT e.id_estudiante,e.documento,e.nombre,e.apellido,i.estado,i.fecha_inscripcion
        FROM inscripciones i
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        WHERE i.id_actividad = %s
        ORDER BY i.estado, e.apellido, e.nombre;
    """

    cursor.execute(consulta, (id_actividad,))
    inscriptos = cursor.fetchall()

    print("\nInscriptos por actividad")

    if not inscriptos:
        print("No hay estudiantes inscriptos en esta actividad.")
    else:
        for inscripto in inscriptos:
            print(
                f"ID estudiante: {inscripto[0]} | Documento: {inscripto[1]} | "
                f"Nombre: {inscripto[2]} {inscripto[3]} | "
                f"Estado inscripción: {inscripto[4]} | Fecha: {inscripto[5]}"
            )

    cursor.close()
    conexion.close()


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def registrar_asistencia():
    id_inscripcion = input("Ingrese ID de inscripción confirmada: ").strip()
    fecha = input("Ingrese fecha de asistencia (YYYY-MM-DD): ").strip()
    estado = input("Ingrese estado (presente/ausente): ").strip().lower()
    observacion = input("Observación opcional: ").strip()

    if not id_inscripcion.isdigit():
        print("El ID de inscripción debe ser numérico.")
        return

    if not validar_fecha(fecha):
        print("La fecha debe tener formato YYYY-MM-DD.")
        return

    if estado not in ["presente", "ausente"]:
        print("Estado inválido. Debe ser presente o ausente.")
        return

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        consulta_validacion = """
            SELECT id_inscripcion
            FROM inscripciones
            WHERE id_inscripcion = %s
              AND estado = 'confirmada';
        """

        cursor.execute(consulta_validacion, (id_inscripcion,))
        inscripcion = cursor.fetchone()

        if not inscripcion:
            print("La inscripción no existe o no está confirmada.")
            return

        consulta_insert = """
            INSERT INTO asistencias (id_inscripcion, fecha, estado, observacion)
            VALUES (%s, %s, %s, %s);
        """

        cursor.execute(
            consulta_insert,
            (id_inscripcion, fecha, estado, observacion)
        )

        conexion.commit()
        print("Asistencia registrada correctamente.")

    except Exception as e:
        conexion.rollback()
        print("Error al registrar asistencia.")
        print(e)

    finally:
        cursor.close()
        conexion.close()


def modificar_asistencia():
    id_asistencia = input("Ingrese ID de asistencia a modificar: ").strip()
    nuevo_estado = input("Nuevo estado (presente/ausente): ").strip().lower()
    observacion = input("Nueva observación opcional: ").strip()

    if not id_asistencia.isdigit():
        print("El ID de asistencia debe ser numérico.")
        return

    if nuevo_estado not in ["presente", "ausente"]:
        print("Estado inválido. Debe ser presente o ausente.")
        return

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        consulta = """
            UPDATE asistencias
            SET estado = %s,
                observacion = %s
            WHERE id_asistencia = %s;
        """

        cursor.execute(consulta, (nuevo_estado, observacion, id_asistencia))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Asistencia modificada correctamente.")
        else:
            print("No se encontró una asistencia con ese ID.")

    except Exception as e:
        conexion.rollback()
        print("Error al modificar asistencia.")
        print(e)

    finally:
        cursor.close()
        conexion.close()


def ver_asistencias_por_actividad_fecha():
    id_actividad = input("Ingrese ID de actividad: ").strip()
    fecha = input("Ingrese fecha (YYYY-MM-DD): ").strip()

    if not id_actividad.isdigit():
        print("El ID de actividad debe ser numérico.")
        return

    if not validar_fecha(fecha):
        print("La fecha debe tener formato YYYY-MM-DD.")
        return

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        SELECT asi.id_asistencia,e.documento,e.nombre,e.apellido,asi.fecha,asi.estado,asi.observacion
        FROM asistencias asi
        JOIN inscripciones i ON asi.id_inscripcion = i.id_inscripcion
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        WHERE i.id_actividad = %s
          AND asi.fecha = %s
        ORDER BY e.apellido, e.nombre;
    """

    cursor.execute(consulta, (id_actividad, fecha))
    asistencias = cursor.fetchall()

    print("\nAsistencias por actividad y fecha")

    if not asistencias:
        print("No hay asistencias registradas para esa actividad y fecha.")
    else:
        for asistencia in asistencias:
            print(
                f"ID asistencia: {asistencia[0]} | Documento: {asistencia[1]} | "
                f"Nombre: {asistencia[2]} {asistencia[3]} | Fecha: {asistencia[4]} | "
                f"Estado: {asistencia[5]} | Observación: {asistencia[6]}"
            )

    cursor.close()
    conexion.close()


def menu_profesor():
    while True:
        print("\nMenu profesor")
        print("1. Listar estudiantes")
        print("2. Buscar estudiante")
        print("3. Ver actividades")
        print("4. Ver inscriptos por actividad")
        print("5. Registrar asistencia")
        print("6. Modificar asistencia")
        print("7. Ver asistencias por actividad y fecha")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_estudiantes()
        elif opcion == "2":
            buscar_estudiante()
        elif opcion == "3":
            ver_actividades()
        elif opcion == "4":
            ver_inscriptos_por_actividad()
        elif opcion == "5":
            registrar_asistencia()
        elif opcion == "6":
            modificar_asistencia()
        elif opcion == "7":
            ver_asistencias_por_actividad_fecha()
        elif opcion == "0":
            print("Saliendo del sistema")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_profesor()