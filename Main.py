import platform
import os
import time
import sqlite3 as sql
from Registro import Database
from Productos import TiendaVirtualAdmin
from Usuarios import TiendaVirtualUsuario

usuario = "Admin"
contrasena = "12345"

BASE_DATOS = "database.db"
TABLA = "Usuario"


def crear_nuevoUsuario(manejador: Database):
    manejador.create_table
    nombre =  input("Escriba su nombre: ")
    nombre_usuario = input("Escriba su nombre de usuario: ")
    correo =  input("Escriba su correo: ")
    contraseña = input("Escriba su contraseña: ")
    manejador.agregar(
        {
            "nombre": nombre,
            "nombre_usuario":  nombre_usuario,
            "correo":  correo,
            "contraseña": contraseña,
        }
    )

def login():
    continuar = True
    while continuar:
        nombre_usuario = input("Introduzca su nombre de usuario: ")
        contraseña = input("Introduzca su contraseña: ")
        con = sql.connect("database.db")
        cur = con.cursor()
        statement = f"SELECT * FROM Usuario WHERE nombre_usuario='{nombre_usuario}' AND contraseña ='{contraseña}';"
        cur.execute(statement)
        if not cur.fetchone():
            print("Error nombre usuario")
            time.sleep(3)
            os.system('cls')
        else:
            break

def opciones_admin():
    admin = TiendaVirtualAdmin("tienda_virtual.db")

    while True:
        print("\n1. Crear productos")
        print("2. Eliminar producto")
        print("3. Ocultar producto")
        print("4. Aplicar descuento")
        print("5. Establecer monto de reserva")
        print("6. Modificar precio")
        print("7. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            num_productos = int(input("Número de productos a crear: "))
            lista_productos = []
            for i in range(num_productos):
                nombre = input(f"Nombre del producto {i + 1}: ")
                precio_original = float(input(f"Precio original del producto {i + 1}: "))
                monto_reserva = float(input(f"monto de reserva para el producto {i + 1}: "))
                lista_productos.append((nombre, precio_original, monto_reserva))
            admin.crear_productos(lista_productos)

        elif opcion == "2":
            producto_id = int(input("ID del producto a eliminar: "))
            admin.eliminar_producto(producto_id)

        elif opcion == "3":
            producto_id = int(input("ID del producto a ocultar: "))
            admin.ocultar_producto(producto_id)

        elif opcion == "4":
            producto_id = int(input("ID del producto a aplicar descuento: "))
            descuento = float(input("Porcentaje de descuento: "))
            admin.aplicar_descuento(producto_id, descuento)

        elif opcion == "5":
            producto_id = int(input("ID del producto a establecer valor de reserva: "))
            monto_reserva = float(input("Nuevo monto de reserva: "))
            admin.establecer_monto_reserva(producto_id, monto_reserva)

        elif opcion == "6":
            producto_id = int(input("ID del producto a modificar: "))
            nuevo_precio = float(input("Nuevo precio: "))
            admin.modificar_precio(producto_id, nuevo_precio)

        elif opcion == "7":
            admin.cerrar_conexion()
            break

        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")


def Opciones_usuarios():
    admin = TiendaVirtualAdmin("tienda_virtual.db")
    usuario = TiendaVirtualUsuario("tienda_virtual.db")

    while True:
        print("\n1. Revisar productos")
        print("2. Hacer reservación")
        print("3. Generar pedido")
        print("4. Pago de pedido")
        print("5. Cancelar pedido")
        print("6. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            query = "SELECT id, nombre, precio_original, valor_reserva FROM productos WHERE habilitado = 1"
            admin.cursor.execute(query)
            productos = admin.cursor.fetchall()
            print("Productos disponibles:")
            for producto in productos:
                print(f"ID: {producto[0]}, Producto: {producto[1]}, Precio Original: {producto[2]}, Valor Reserva: {producto[3]}")
                
        elif opcion == "2":
            producto_id = int(input("ID del producto a reservar: "))
            monto = float(input("Monto mínimo para la reservación: "))
            usuario.hacer_reservacion(producto_id, monto)

        elif opcion == "3":
            usuario.mostrar_productos()
            productos_seleccionados = []   
            while True:
                producto_id = input("Ingrese el ID del producto que desea agregar al pedido (o 's' para salir): ")
                if producto_id.lower() == "s":
                    break
                try:
                    producto_id = int(producto_id)
            
                    query = "SELECT id, nombre, precio_original FROM productos WHERE habilitado = 1 AND id = ?"
                    usuario.cursor.execute(query, (producto_id,))
                    producto = usuario.cursor.fetchone()
                    if producto:
                        productos_seleccionados.append({
                            "id": producto[0],
                            "nombre": producto[1],
                            "precio_original": producto[2]
                        })
                        print(f"Producto '{producto[1]}' agregado al pedido.")
                    else:
                        print("Producto no válido o no habilitado.")
                except ValueError:
                    print("Ingrese un ID válido.")
    
                usuario.generar_pedido(productos_seleccionados)

          
        elif opcion == "4":
            usuario.mostrar_pedidos()
            pedido_id = int(input("ID del pedido a pagar: "))
            
            query_pedido = """
                SELECT id, direccion_entrega
                FROM pedidos
                WHERE id = ?
            """
            usuario.cursor.execute(query_pedido, (pedido_id,))
            pedido = usuario.cursor.fetchone()

            if pedido:
                print("\nDetalle del pedido a pagar:")
                print(f"ID del pedido: {pedido[0]}")
                print(f"Dirección de entrega: {pedido[1]}")

                usuario.pagar_pedido(pedido_id)  # Actualizado
            else:
                print("Pedido no encontrado.")


        elif opcion == "5":
            usuario.cancelar_pedido()

        elif opcion == "6":
            exit(0)

def main():
    continuar = True
    while continuar:
        print("1.- Login")
        print("2.- Registrarse")

        opcion = input("Seleccione la opcion: ")

        db = Database(BASE_DATOS, TABLA)


        match opcion:
            case "1":
                os.system('cls')
                print("1.- Usuario")
                print("2.- Administrador")

                opcion2 = input("Seleccione una opcion: ")
                match opcion2:
                    case "1":
                        os.system('cls')
                        login()
                        os.system('cls')
                        print("Que desea hacer ahora")

                        Opciones_usuarios()
                    
                    case "2":
                        for i in range(2):
                            user  = input("Introduzca el Usuario: ")
                            if user == usuario:
                                for i in range(2):
                                    password = input("Introduzca la contrasena: ")
                                    if password == contrasena:
                                        
                                        opciones_admin()
                                        
                                    else:
                                        print("Error de contrasena")
                            else:
                                print("Error de Usuario")
                
            case "2":
                os.system('cls')
                crear_nuevoUsuario(db)
                print("Por logearse ahora")
                time.sleep(3)
                os.system('cls')
            case _:
                exit(0)


# Ejecutar la funcion principal
main()