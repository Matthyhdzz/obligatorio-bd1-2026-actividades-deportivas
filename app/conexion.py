import mysql.connector
from mysql.connector import Error
from conexion_admin import obtener_conexion


def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="adminpassword",
            database="gestion_actividades_deportivas"
        )

        if conexion.is_connected():
            return conexion

    except Error:
        print("Error al conectar con la base de datos:", Error)
        return None