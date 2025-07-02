from modelo.conexion_bd import conectar

def login():  
    usuario = input ("Nombre de usuario: ")
    contraseña = input ("Contraseña: ")

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario=%s AND contraseña=%s", (usuario, contraseña))
    result = cursor.fetchone()

    if result:
        rol = result[0]
        print(f"Bienvenido {usuario}, ingresaste con el rol de {rol}")
        return rol
    else:
        print("Usuario o contraseña incorrectos")
        return None