from conexion import obtener_conexion
from mysql.connector import Error


estados_posibles = ["abierta", "cerrada", "finalizada", "cancelada"]


def mostrar_menu_actividades():
    print("\n===== GESTIÓN DE ACTIVIDADES DEPORTIVAS =====")
    print("1. Listar actividades")
    print("2. Buscar actividad por ID")
    print("3. Agregar actividad")
    print("4. Modificar actividad")
    print("5. Cambiar estado de actividad")
    print("0. Volver al menú principal")


def listar_disciplinas_activas():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT id_disciplina, nombre
            FROM disciplinas
            WHERE estado = 'activa'
            ORDER BY nombre;
        """

        cursor.execute(consulta)
        disciplinas = cursor.fetchall()

        print("\n--- DISCIPLINAS ACTIVAS ---")
        for disciplina in disciplinas:
            print(f"{disciplina[0]}. {disciplina[1]}")

        cursor.close()

    except Error as e:
        print("Error al listar disciplinas:", e)

    finally:
        conexion.close()


def listar_espacios_activos():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT id_espacio, nombre, capacidad
            FROM espacios
            WHERE estado = 'activo'
            ORDER BY nombre;
        """

        cursor.execute(consulta)
        espacios = cursor.fetchall()

        print("\n--- ESPACIOS ACTIVOS ---")
        for espacio in espacios:
            print(f"{espacio[0]}. {espacio[1]} - Capacidad: {espacio[2]}")

        cursor.close()

    except Error as e:
        print("Error al listar espacios:", e)

    finally:
        conexion.close()


def listar_actividades():
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
                d.nombre AS disciplina,
                e.nombre AS espacio,
                a.cupo_maximo,
                a.dia_semana,
                a.hora_inicio,
                a.hora_fin,
                a.estado
            FROM actividades a
            JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
            JOIN espacios e ON a.id_espacio = e.id_espacio
            ORDER BY a.id_actividad;
        """

        cursor.execute(consulta)
        actividades = cursor.fetchall()

        if len(actividades) == 0:
            print("\nNo hay actividades registradas.")
        else:
            print("\n--- LISTADO DE ACTIVIDADES ---")
            for actividad in actividades:
                print(f"ID: {actividad[0]}")
                print(f"Nombre: {actividad[1]}")
                print(f"Disciplina: {actividad[2]}")
                print(f"Espacio: {actividad[3]}")
                print(f"Cupo máximo: {actividad[4]}")
                print(f"Día: {actividad[5]}")
                print(f"Horario: {actividad[6]} a {actividad[7]}")
                print(f"Estado: {actividad[8]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al listar actividades:", e)

    finally:
        conexion.close()


def buscar_actividad_por_id():
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
                a.id_actividad,
                a.nombre,
                d.nombre AS disciplina,
                e.nombre AS espacio,
                a.cupo_maximo,
                a.dia_semana,
                a.hora_inicio,
                a.hora_fin,
                a.estado
            FROM actividades a
            JOIN disciplinas d ON a.id_disciplina = d.id_disciplina
            JOIN espacios e ON a.id_espacio = e.id_espacio
            WHERE a.id_actividad = %s;
        """

        cursor.execute(consulta, (id_actividad,))
        actividad = cursor.fetchone()

        if actividad is None:
            print("\nNo se encontró una actividad con ese ID.")
        else:
            print("\n--- ACTIVIDAD ENCONTRADA ---")
            print(f"ID: {actividad[0]}")
            print(f"Nombre: {actividad[1]}")
            print(f"Disciplina: {actividad[2]}")
            print(f"Espacio: {actividad[3]}")
            print(f"Cupo máximo: {actividad[4]}")
            print(f"Día: {actividad[5]}")
            print(f"Horario: {actividad[6]} a {actividad[7]}")
            print(f"Estado: {actividad[8]}")

        cursor.close()

    except Error as e:
        print("Error al buscar actividad:", e)

    finally:
        conexion.close()


def validar_estado_actividad(estado):
    return estado in estados_posibles


def agregar_actividad():
    print("\n--- AGREGAR ACTIVIDAD ---")

    nombre = input("Nombre de la actividad: ").strip()

    listar_disciplinas_activas()
    try:
        id_disciplina = int(input("ID de disciplina: "))
    except ValueError:
        print("El ID de disciplina debe un numero.")
        return

    listar_espacios_activos()
    try:
        id_espacio = int(input("ID de espacio: "))
    except ValueError:
        print("El ID de espacio debe un numero.")
        return

    try:
        cupo_maximo = int(input("Cupo máximo: "))
    except ValueError:
        print("El cupo máximo debe un numero.")
        return

    dia_semana = input("Día de la semana: ").strip()
    hora_inicio = input("Hora de inicio (HH:MM:SS): ").strip()
    hora_fin = input("Hora de fin (HH:MM:SS): ").strip()

    if nombre == "" or dia_semana == "" or hora_inicio == "" or hora_fin == "":
        print("Escribe en todos los campos.")
        return

    if cupo_maximo <= 0:
        print("El cupo máximo debe ser mayor a 0.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta_disciplina = """
            SELECT id_disciplina
            FROM disciplinas
            WHERE id_disciplina = %s AND estado = 'activa';
        """

        cursor.execute(consulta_disciplina, (id_disciplina,))
        disciplina = cursor.fetchone()

        if disciplina is None:
            print("La disciplina seleccionada no existe o no está activa.")
            cursor.close()
            return

        consulta_espacio = """
            SELECT capacidad
            FROM espacios
            WHERE id_espacio = %s AND estado = 'activo';
        """

        cursor.execute(consulta_espacio, (id_espacio,))
        espacio = cursor.fetchone()

        if espacio is None:
            print("El espacio seleccionado no existe o no está activo.")
            cursor.close()
            return

        capacidad_espacio = espacio[0]

        if cupo_maximo > capacidad_espacio:
            print("El cupo máximo no puede superar la capacidad del espacio.")
            cursor.close()
            return

        consulta_insert = """
            INSERT INTO actividades (
                nombre,
                id_disciplina,
                id_espacio,
                cupo_maximo,
                dia_semana,
                hora_inicio,
                hora_fin,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'abierta');
        """

        cursor.execute(
            consulta_insert,
            (
                nombre,
                id_disciplina,
                id_espacio,
                cupo_maximo,
                dia_semana,
                hora_inicio,
                hora_fin
            )
        )

        conexion.commit()

        print("Actividad agregada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al agregar actividad:", e)
        conexion.rollback()

    finally:
        conexion.close()


def modificar_actividad():
    print("\n--- MODIFICAR ACTIVIDAD ---")

    try:
        id_actividad = int(input("Ingrese ID de la actividad a modificar: "))
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
            SELECT 
                nombre,
                id_disciplina,
                id_espacio,
                cupo_maximo,
                dia_semana,
                hora_inicio,
                hora_fin
            FROM actividades
            WHERE id_actividad = %s;
        """

        cursor.execute(consulta_busqueda, (id_actividad,))
        actividad = cursor.fetchone()

        if actividad is None:
            print("No existe una actividad con ese ID.")
            cursor.close()
            return

        print("\nDejá vacío el campo si no querés modificarlo.")

        nuevo_nombre = input(f"Nombre actual ({actividad[0]}): ").strip()

        listar_disciplinas_activas()
        nueva_disciplina = input(f"ID disciplina actual ({actividad[1]}): ").strip()

        listar_espacios_activos()
        nuevo_espacio = input(f"ID espacio actual ({actividad[2]}): ").strip()

        nuevo_cupo = input(f"Cupo máximo actual ({actividad[3]}): ").strip()
        nuevo_dia = input(f"Día actual ({actividad[4]}): ").strip()
        nueva_hora_inicio = input(f"Hora inicio actual ({actividad[5]}): ").strip()
        nueva_hora_fin = input(f"Hora fin actual ({actividad[6]}): ").strip()

        nombre = nuevo_nombre if nuevo_nombre != "" else actividad[0]
        dia_semana = nuevo_dia if nuevo_dia != "" else actividad[4]
        hora_inicio = nueva_hora_inicio if nueva_hora_inicio != "" else actividad[5]
        hora_fin = nueva_hora_fin if nueva_hora_fin != "" else actividad[6]

        if nueva_disciplina != "":
            try:
                id_disciplina = int(nueva_disciplina)
            except ValueError:
                print("El ID de disciplina debe ser numérico.")
                cursor.close()
                return
        else:
            id_disciplina = actividad[1]

        if nuevo_espacio != "":
            try:
                id_espacio = int(nuevo_espacio)
            except ValueError:
                print("El ID de espacio debe ser numérico.")
                cursor.close()
                return
        else:
            id_espacio = actividad[2]

        if nuevo_cupo != "":
            try:
                cupo_maximo = int(nuevo_cupo)
            except ValueError:
                print("El cupo máximo debe ser numérico.")
                cursor.close()
                return
        else:
            cupo_maximo = actividad[3]

        if nombre == "" or dia_semana == "" or str(hora_inicio) == "" or str(hora_fin) == "":
            print("Los campos obligatorios no pueden quedar vacíos.")
            cursor.close()
            return

        if cupo_maximo <= 0:
            print("El cupo máximo debe ser mayor a 0.")
            cursor.close()
            return

        consulta_disciplina = """
            SELECT id_disciplina
            FROM disciplinas
            WHERE id_disciplina = %s AND estado = 'activa';
        """

        cursor.execute(consulta_disciplina, (id_disciplina,))
        disciplina = cursor.fetchone()

        if disciplina is None:
            print("La disciplina seleccionada no existe o no está activa.")
            cursor.close()
            return

        consulta_espacio = """
            SELECT capacidad
            FROM espacios
            WHERE id_espacio = %s AND estado = 'activo';
        """

        cursor.execute(consulta_espacio, (id_espacio,))
        espacio = cursor.fetchone()

        if espacio is None:
            print("El espacio seleccionado no existe o no está activo.")
            cursor.close()
            return

        capacidad_espacio = espacio[0]

        if cupo_maximo > capacidad_espacio:
            print("El cupo máximo no puede superar la capacidad del espacio.")
            cursor.close()
            return

        consulta_update = """
            UPDATE actividades
            SET nombre = %s,
                id_disciplina = %s,
                id_espacio = %s,
                cupo_maximo = %s,
                dia_semana = %s,
                hora_inicio = %s,
                hora_fin = %s
            WHERE id_actividad = %s;
        """

        cursor.execute(
            consulta_update,
            (
                nombre,
                id_disciplina,
                id_espacio,
                cupo_maximo,
                dia_semana,
                hora_inicio,
                hora_fin,
                id_actividad
            )
        )

        conexion.commit()

        print("Actividad modificada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al modificar actividad:", e)
        conexion.rollback()

    finally:
        conexion.close()


def cambiar_estado_actividad():
    print("\n--- CAMBIAR ESTADO DE ACTIVIDAD ---")

    try:
        id_actividad = int(input("Ingrese ID de la actividad: "))
    except ValueError:
        print("El ID debe ser numérico.")
        return

    print("\nEstados disponibles:")
    print("1. abierta")
    print("2. cerrada")
    print("3. finalizada")
    print("4. cancelada")

    nuevo_estado = input("Ingrese nuevo estado: ").strip().lower()

    if not validar_estado_actividad(nuevo_estado):
        print("Estado inválido.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            UPDATE actividades
            SET estado = %s
            WHERE id_actividad = %s;
        """

        cursor.execute(consulta, (nuevo_estado, id_actividad))
        conexion.commit()

        if cursor.rowcount == 0:
            print("No existe una actividad con ese ID.")
        else:
            print("Estado de actividad actualizado correctamente.")

        cursor.close()

    except Error as e:
        print("Error al cambiar estado de actividad:", e)
        conexion.rollback()

    finally:
        conexion.close()


def menu_actividades():
    opcion = ""

    while opcion != "0":
        mostrar_menu_actividades()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_actividades()
        elif opcion == "2":
            buscar_actividad_por_id()
        elif opcion == "3":
            agregar_actividad()
        elif opcion == "4":
            modificar_actividad()
        elif opcion == "5":
            cambiar_estado_actividad()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")