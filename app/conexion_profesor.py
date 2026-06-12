import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="app_profesor",
        password="profesor123",
        database="gestion_actividades_deportivas"
    )