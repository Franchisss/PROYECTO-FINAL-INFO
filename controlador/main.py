from login import login
from menu import menu_imagenes, menu_senales

def main():
    rol = login()
    if rol == 'imagenes':
        menu_imagenes()
    elif rol == 'senales':
        menu_senales()

if __name__ == "__main__":
    main()
