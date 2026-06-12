from conexion import obtener_conexion
from mysql.connector import Error


def mostrar_menu_espacios():
    print("\nGestion de espacios")
    print("1. Listar espacios")
    print("2. Buscar espacio por ID")
    print("3. Agregar espacio")
    print("4. Modificar espacio")
    print("5. Dar de baja espacio")
    print("0. Volver al menú principal")


def listar_espacios():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT id_espacio, nombre, ubicacion, capacidad, estado
            FROM espacios
            ORDER BY nombre;
        """

        cursor.execute(consulta)
        espacios = cursor.fetchall()

        if len(espacios) == 0:
            print("\nNo hay espacios registrados.")
        else:
            print("\n Listar espacios")
            for espacio in espacios:
                print(f"ID: {espacio[0]}")
                print(f"Nombre: {espacio[1]}")
                print(f"Ubicación: {espacio[2]}")
                print(f"Capacidad: {espacio[3]}")
                print(f"Estado: {espacio[4]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al listar espacios:", e)

    finally:
        conexion.close()


def buscar_espacio_por_id():
    try:
        id_espacio = int(input("Ingrese ID del espacio: "))
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
            SELECT id_espacio, nombre, ubicacion, capacidad, estado
            FROM espacios
            WHERE id_espacio = %s;
        """

        cursor.execute(consulta, (id_espacio,))
        espacio = cursor.fetchone()

        if espacio is None:
            print("\nNo se encontró un espacio con ese ID.")
        else:
            print("\n--- ESPACIO ENCONTRADO ---")
            print(f"ID: {espacio[0]}")
            print(f"Nombre: {espacio[1]}")
            print(f"Ubicación: {espacio[2]}")
            print(f"Capacidad: {espacio[3]}")
            print(f"Estado: {espacio[4]}")

        cursor.close()

    except Error as e:
        print("Error al buscar espacio:", e)

    finally:
        conexion.close()


def agregar_espacio():
    print("\n Agregar espacio")

    nombre = input("Nombre: ").strip()
    ubicacion = input("Ubicación: ").strip()

    try:
        capacidad = int(input("Capacidad: "))
    except ValueError:
        print("La capacidad debe ser numérica.")
        return

    if nombre == "":
        print("El nombre del espacio es obligatorio.")
        return

    if capacidad <= 0:
        print("La capacidad debe ser mayor a 0.")
        return

    if ubicacion == "":
        ubicacion = None

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO espacios (nombre,ubicacion,capacidad,estado)
            VALUES (%s, %s, %s, 'activo');
        """

        cursor.execute(consulta, (nombre, ubicacion, capacidad))
        conexion.commit()

        print("Espacio agregado correctamente.")

        cursor.close()

    except Error as e:
        print("Error al agregar espacio:", e)
        conexion.rollback()

    finally:
        conexion.close()


def modificar_espacio():
    print("\nModificar espacios")

    try:
        id_espacio = int(input("Ingrese ID del espacio a modificar: "))
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
            SELECT nombre, ubicacion, capacidad
            FROM espacios
            WHERE id_espacio = %s;
        """

        cursor.execute(consulta_busqueda, (id_espacio,))
        espacio = cursor.fetchone()

        if espacio is None:
            print("No existe un espacio con ese ID.")
            cursor.close()
            return

        print("\nDejá vacío el campo si no querés modificarlo.")

        nuevo_nombre = input(f"Nombre actual ({espacio[0]}): ").strip()
        nueva_ubicacion = input(f"Ubicación actual ({espacio[1]}): ").strip()
        nueva_capacidad = input(f"Capacidad actual ({espacio[2]}): ").strip()

        nombre = nuevo_nombre if nuevo_nombre != "" else espacio[0]
        ubicacion = nueva_ubicacion if nueva_ubicacion != "" else espacio[1]

        if nueva_capacidad != "":
            try:
                capacidad = int(nueva_capacidad)
            except ValueError:
                print("La capacidad debe ser numérica.")
                cursor.close()
                return
        else:
            capacidad = espacio[2]

        if nombre == "":
            print("El nombre no puede quedar vacío.")
            cursor.close()
            return

        if capacidad <= 0:
            print("La capacidad debe ser mayor a 0.")
            cursor.close()
            return

        consulta_update = """
            UPDATE espacios
            SET nombre = %s,
                ubicacion = %s,
                capacidad = %s
            WHERE id_espacio = %s;
        """

        cursor.execute(consulta_update, (nombre, ubicacion, capacidad, id_espacio))
        conexion.commit()

        print("Espacio modificado correctamente.")

        cursor.close()

    except Error as e:
        print("Error al modificar espacio:", e)
        conexion.rollback()

    finally:
        conexion.close()


def dar_baja_espacio():
    print("\nDar un espacio de baja")

    try:
        id_espacio = int(input("Ingrese ID del espacio: "))
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
            UPDATE espacios
            SET estado = 'inactivo'
            WHERE id_espacio = %s;
        """

        cursor.execute(consulta, (id_espacio,))
        conexion.commit()

        if cursor.rowcount == 0:
            print("No existe un espacio con ese ID.")
        else:
            print("Espacio dado de baja correctamente.")

        cursor.close()

    except Error as e:
        print("Error al dar de baja espacio:", e)
        conexion.rollback()

    finally:
        conexion.close()


def menu_espacios():
    opcion = ""

    while opcion != "0":
        mostrar_menu_espacios()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_espacios()
        elif opcion == "2":
            buscar_espacio_por_id()
        elif opcion == "3":
            agregar_espacio()
        elif opcion == "4":
            modificar_espacio()
        elif opcion == "5":
            dar_baja_espacio()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")