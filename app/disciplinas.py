from conexion import obtener_conexion
from mysql.connector import Error


def mostrar_menu_disciplinas():
    print("\nGestion de disciplinas")
    print("1. Listar disciplinas")
    print("2. Buscar disciplina por ID")
    print("3. Agregar disciplina")
    print("4. Modificar disciplina")
    print("5. Dar de baja disciplina")
    print("0. Volver al menú principal")


def listar_disciplinas():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT id_disciplina, nombre, descripcion, estado
            FROM disciplinas
            ORDER BY nombre;
        """

        cursor.execute(consulta)
        disciplinas = cursor.fetchall()

        if len(disciplinas) == 0:
            print("\nNo hay disciplinas registradas.")
        else:
            print("\n Listado de disciplinas")
            for disciplina in disciplinas:
                print(f"ID: {disciplina[0]}")
                print(f"Nombre: {disciplina[1]}")
                print(f"Descripción: {disciplina[2]}")
                print(f"Estado: {disciplina[3]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al listar disciplinas:", e)

    finally:
        conexion.close()


def buscar_disciplina_por_id():
    try:
        id_disciplina = int(input("Ingrese ID de la disciplina: "))
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
            SELECT id_disciplina, nombre, descripcion, estado
            FROM disciplinas
            WHERE id_disciplina = %s;
        """

        cursor.execute(consulta, (id_disciplina,))
        disciplina = cursor.fetchone()

        if disciplina is None:
            print("\nNo se encontró una disciplina con ese ID.")
        else:
            print("\nDisciplina encontrada")
            print(f"ID: {disciplina[0]}")
            print(f"Nombre: {disciplina[1]}")
            print(f"Descripción: {disciplina[2]}")
            print(f"Estado: {disciplina[3]}")

        cursor.close()

    except Error as e:
        print("Error al buscar disciplina:", e)

    finally:
        conexion.close()


def agregar_disciplina():
    print("\nAgregar disciplina")

    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()

    if nombre == "":
        print("El nombre de la disciplina es obligatorio.")
        return

    if descripcion == "":
        descripcion = None

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO disciplinas (nombre,descripcion,estado)
            VALUES (%s, %s, 'activa');
        """

        cursor.execute(consulta, (nombre, descripcion))
        conexion.commit()

        print("Disciplina agregada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al agregar disciplina:", e)
        conexion.rollback()

    finally:
        conexion.close()


def modificar_disciplina():
    print("\nModificar disciplina")

    try:
        id_disciplina = int(input("Ingrese ID de la disciplina a modificar: "))
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
            SELECT nombre, descripcion
            FROM disciplinas
            WHERE id_disciplina = %s;
        """

        cursor.execute(consulta_busqueda, (id_disciplina,))
        disciplina = cursor.fetchone()

        if disciplina is None:
            print("No existe una disciplina con ese ID.")
            cursor.close()
            return

        print("\nDejá vacío el campo si no querés modificarlo.")

        nuevo_nombre = input(f"Nombre actual ({disciplina[0]}): ").strip()
        nueva_descripcion = input(f"Descripción actual ({disciplina[1]}): ").strip()

        nombre = nuevo_nombre if nuevo_nombre != "" else disciplina[0]
        descripcion = nueva_descripcion if nueva_descripcion != "" else disciplina[1]

        consulta_update = """
            UPDATE disciplinas
            SET nombre = %s,
                descripcion = %s
            WHERE id_disciplina = %s;
        """

        cursor.execute(consulta_update, (nombre, descripcion, id_disciplina))
        conexion.commit()

        print("Disciplina modificada correctamente.")

        cursor.close()

    except Error as e:
        print("Error al modificar disciplina:", e)
        conexion.rollback()

    finally:
        conexion.close()


def dar_baja_disciplina():
    print("\nDar disciplina de baja")

    try:
        id_disciplina = int(input("Ingrese ID de la disciplina: "))
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
            UPDATE disciplinas
            SET estado = 'inactiva'
            WHERE id_disciplina = %s;
        """

        cursor.execute(consulta, (id_disciplina,))
        conexion.commit()

        if cursor.rowcount == 0:
            print("No existe una disciplina con ese ID.")
        else:
            print("Disciplina dada de baja correctamente.")

        cursor.close()

    except Error as e:
        print("Error al dar de baja disciplina:", e)
        conexion.rollback()

    finally:
        conexion.close()


def menu_disciplinas():
    opcion = ""

    while opcion != "0":
        mostrar_menu_disciplinas()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_disciplinas()
        elif opcion == "2":
            buscar_disciplina_por_id()
        elif opcion == "3":
            agregar_disciplina()
        elif opcion == "4":
            modificar_disciplina()
        elif opcion == "5":
            dar_baja_disciplina()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")