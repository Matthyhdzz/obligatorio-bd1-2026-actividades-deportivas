from estudiantes import menu_estudiantes
from disciplinas import menu_disciplinas
from espacios import menu_espacios
from actividades import menu_actividades
from inscripciones import menu_inscripciones
from asistencias import menu_asistencias
from reportes import menu_reportes


def mostrar_menu_principal():
    print("SISTEMA DE GESTIÓN")
    print("1. Gestión de estudiantes")
    print("2. Gestión de disciplinas deportivas")
    print("3. Gestión de espacios deportivos")
    print("4. Gestión de actividades deportivas")
    print("5. Gestión de inscripciones")
    print("6. Registro de asistencias")
    print("7. Reportes")
    print("0. Salir")


def ejecutar_opcion(opcion):
    if opcion == "1":
        menu_estudiantes()
    elif opcion == "2":
        menu_disciplinas()
    elif opcion == "3":
        menu_espacios()
    elif opcion == "4":
        menu_actividades()
    elif opcion == "5":
       menu_inscripciones()
    elif opcion == "6":
        menu_asistencias()
    elif opcion == "7":
        menu_reportes()
    elif opcion == "0":
        print("Saliendo")
    else:
        print("\nOpcion invalida")


def main():
    opcion = ""

    while opcion != "0":
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        ejecutar_opcion(opcion)


main()