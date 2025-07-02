import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(host='localhost',user='root',password='',database='proyecto3')
        return conexion
    
    except mysql.connector.Error as err:
        print("Error al conectar {err}")
        return None
    