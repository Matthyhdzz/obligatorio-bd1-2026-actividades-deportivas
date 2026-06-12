from conexion import obtener_conexion
from mysql.connector import Error


def mostrar_menu_estudiantes():
    print("Gestión de estudiantes")
    print("1. Listar estudiantes")
    print("2. Buscar estudiante por documento")
    print("3. Agregar estudiante")
    print("4. Modificar estudiante")
    print("5. Dar de baja estudiante")
    print("0. Volver al menú principal")


def listar_estudiantes():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
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

        if len(estudiantes) == 0:
            print("\nNo hay estudiantes registrados.")
        else:
            print("\nListado de estudiantes")
            for estudiante in estudiantes:
                print(f"ID: {estudiante[0]}")
                print(f"Documento: {estudiante[1]}")
                print(f"Nombre: {estudiante[2]} {estudiante[3]}")
                print(f"Correo: {estudiante[4]}")
                print(f"Carrera: {estudiante[5]}")
                print(f"Facultad: {estudiante[6]}")
                print(f"Estado: {estudiante[7]}")
                print("-" * 40)

        cursor.close()

    except Error as e:
        print("Error al listar estudiantes:", e)

    finally:
        conexion.close()


def buscar_estudiante_por_documento():
    documento = input("Ingrese documento del estudiante: ").strip()

    if documento == "":
        print("El documento no puede estar vacío.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
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

        if estudiante is None:
            print("\nNo se encontró un estudiante con ese documento.")
        else:
            print("\nEncontrado")
            print(f"ID: {estudiante[0]}")
            print(f"Documento: {estudiante[1]}")
            print(f"Nombre: {estudiante[2]} {estudiante[3]}")
            print(f"Correo: {estudiante[4]}")
            print(f"Carrera: {estudiante[5]}")
            print(f"Facultad: {estudiante[6]}")
            print(f"Estado: {estudiante[7]}")

        cursor.close()

    except Error as e:
        print("Error al buscar estudiante:", e)

    finally:
        conexion.close()


def listar_carreras():
    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT c.id_carrera,c.nombre,f.nombre AS facultad
            FROM carreras c
            JOIN facultades f ON c.id_facultad = f.id_facultad
            WHERE c.estado = 'activa'
            ORDER BY f.nombre, c.nombre;
        """

        cursor.execute(consulta)
        carreras = cursor.fetchall()

        print("\nCarreras disponibles")
        for carrera in carreras:
            print(f"{carrera[0]}. {carrera[1]} - {carrera[2]}")

        cursor.close()

    except Error as e:
        print("Error al listar carreras:", e)

    finally:
        conexion.close()


def agregar_estudiante():
    print("\nAgregar estudiante")

    documento = input("Documento: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    correo = input("Correo electrónico: ").strip()

    listar_carreras()

    try:
        id_carrera = int(input("ID de carrera: "))
    except ValueError:
        print("El ID de carrera debe ser numérico.")
        return

    def documento_valido(documento):
        return documento.isdigit()

    def nombre_valido(nombre):
        return nombre.isalpha()

    def apellido_valido(apellido):
        return apellido.isalpha()

    if not documento_valido(documento):
        print("El documento tiene que ser numerico")
        return

    if not nombre_valido(nombre):
        print("El nombre tiene que ser numerico")
        return

    if not apellido_valido(apellido):
        print("El apellido tiene que ser numerico")
        return

    if documento == "" or nombre == "" or apellido == "" or correo == "":
        print("Todos los campos son obligatorios.")
        return

    if "@" not in correo:
        print("El correo electrónico no tiene un formato válido.")
        return

    conexion = obtener_conexion()

    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        consulta_carrera = """
            SELECT id_carrera
            FROM carreras
            WHERE id_carrera = %s AND estado = 'activa';
        """

        cursor.execute(consulta_carrera, (id_carrera,))
        carrera = cursor.fetchone()

        if carrera is None:
            print("La carrera seleccionada no existe o no está activa.")
            cursor.close()
            return

        consulta = """
            INSERT INTO estudiantes (documento,nombre,apellido,correo,id_carrera,estado)
            VALUES (%s, %s, %s, %s, %s, 'activo');
        """

        cursor.execute(consulta, (documento, nombre, apellido, correo, id_carrera))
        conexion.commit()

        print("Estudiante agregado correctamente.")

        cursor.close()

    except Error as e:
        print("Error al agregar estudiante:", e)
        conexion.rollback()

    finally:
        conexion.close()


def modificar_estudiante():
    print("\nModificar estudiante")

    try:
        id_estudiante = int(input("Ingrese ID del estudiante a modificar: "))
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
            SELECT documento, nombre, apellido, correo, id_carrera, estado
            FROM estudiantes
            WHERE id_estudiante = %s;
        """

        cursor.execute(consulta_busqueda, (id_estudiante,))
        estudiante = cursor.fetchone()

        if estudiante is None:
            print("No existe un estudiante con ese ID.")
            cursor.close()
            return

        print("\nSi no se quiere modificar, dejar vacio")

        nuevo_documento = input(f"Documento actual ({estudiante[0]}): ").strip()
        nuevo_nombre = input(f"Nombre actual ({estudiante[1]}): ").strip()
        nuevo_apellido = input(f"Apellido actual ({estudiante[2]}): ").strip()
        nuevo_correo = input(f"Correo actual ({estudiante[3]}): ").strip()

        listar_carreras()
        nueva_carrera = input(f"ID carrera actual ({estudiante[4]}): ").strip()

        documento = nuevo_documento if nuevo_documento != "" else estudiante[0]
        nombre = nuevo_nombre if nuevo_nombre != "" else estudiante[1]
        apellido = nuevo_apellido if nuevo_apellido != "" else estudiante[2]
        correo = nuevo_correo if nuevo_correo != "" else estudiante[3]

        if nueva_carrera != "":
            try:
                id_carrera = int(nueva_carrera)
            except ValueError:
                print("El ID de carrera debe ser numérico.")
                cursor.close()
                return
        else:
            id_carrera = estudiante[4]

        if "@" not in correo:
            print("El correo electrónico no tiene un formato válido.")
            cursor.close()
            return

        consulta_carrera = """
            SELECT id_carrera
            FROM carreras
            WHERE id_carrera = %s AND estado = 'activa';
        """

        cursor.execute(consulta_carrera, (id_carrera,))
        carrera = cursor.fetchone()

        if carrera is None:
            print("La carrera seleccionada no existe o no está activa.")
            cursor.close()
            return

        consulta_update = """
            UPDATE estudiantes
            SET documento = %s,
                nombre = %s,
                apellido = %s,
                correo = %s,
                id_carrera = %s
            WHERE id_estudiante = %s;
        """

        cursor.execute(
            consulta_update,
            (documento, nombre, apellido, correo, id_carrera, id_estudiante)
        )

        conexion.commit()

        print("Estudiante modificado correctamente.")

        cursor.close()

    except Error as e:
        print("Error al modificar estudiante:", e)
        conexion.rollback()

    finally:
        conexion.close()


def dar_baja_estudiante():
    print("\nDar de baja")

    try:
        id_estudiante = int(input("Ingrese ID del estudiante: "))
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
            UPDATE estudiantes
            SET estado = 'inactivo'
            WHERE id_estudiante = %s;
        """

        cursor.execute(consulta, (id_estudiante,))
        conexion.commit()

        if cursor.rowcount == 0:
            print("No existe un estudiante con ese ID.")
        else:
            print("Estudiante dado de baja correctamente.")

        cursor.close()

    except Error as e:
        print("Error al dar de baja estudiante:", e)
        conexion.rollback()

    finally:
        conexion.close()


def menu_estudiantes():
    opcion = ""

    while opcion != "0":
        mostrar_menu_estudiantes()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_estudiantes()
        elif opcion == "2":
            buscar_estudiante_por_documento()
        elif opcion == "3":
            agregar_estudiante()
        elif opcion == "4":
            modificar_estudiante()
        elif opcion == "5":
            dar_baja_estudiante()
        elif opcion == "0":
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida. Intente nuevamente.")