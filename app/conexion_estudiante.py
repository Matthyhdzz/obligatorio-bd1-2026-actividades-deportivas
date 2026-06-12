import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="app_estudiante",
        password="estudiante123",
        database="gestion_actividades_deportivas"
    )