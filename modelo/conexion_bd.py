import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(host='localhost',user='root',password='',database='proyecto3')
        return conexion
    
    except mysql.connector.Error as err:
        print("Error al conectar {err}")
        return None
    
def insertar_senal_mat(nombre, llave, canales, intervalo, promedio):
    con = conectar()
    cursor = con.cursor()

    query = """
        INSERT INTO senales_mat (
            nombre_archivo, llave_seleccionada, canales, intervalo, promedio, fecha_subida
        ) VALUES (%s, %s, %s, %s, %s, NOW())
    """

    valores = (
        nombre,
        llave,
        str(canales),
        str(intervalo),
        str(promedio.tolist() if hasattr(promedio, "tolist") else promedio)
    )

    cursor.execute(query, valores)
    con.commit()
    cursor.close()
    con.close()

    