import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",    #Password generica para no comprometer repositorio
            database="gestion_actividades_deportivas"
        )

        if conexion.is_connected():
            return conexion

    except Error as e:
        print("Error al conectar con la base de datos:", e)
        return None