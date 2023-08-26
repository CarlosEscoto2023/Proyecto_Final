import sqlite3

class TiendaVirtualAdmin:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                precio_original REAL,
                precio_actual REAL,
                habilitado INTEGER,
                valor_reserva REAL
            )
        ''')
        self.conn.commit()

    def crear_productos(self, lista_productos):
        query = "INSERT INTO productos (nombre, precio_original, precio_actual, habilitado, valor_reserva) VALUES (?, ?, ?, 1, ?)"
        values = [(nombre, precio_original, precio_original, valor_reserva) for nombre, precio_original, valor_reserva in lista_productos]
        self.cursor.executemany(query, values)
        self.conn.commit()
        print("Productos creados exitosamente. ")

    def eliminar_producto(self, producto_id):
        query = "DELETE FROM productos WHERE id = ?"
        values = (producto_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("Producto eliminado exitosamente.")

    def ocultar_producto(self, producto_id):
        query = "UPDATE productos SET habilitado = 0 WHERE id = ?"
        values = (producto_id,)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("Producto ocultado exitosamente.")

    def aplicar_descuento(self, producto_id, descuento):
        query = "UPDATE productos SET precio_actual = precio_original * (1 - ? / 100) WHERE id = ?"
        values = (descuento, producto_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("Descuento aplicado exitosamente.")

    def establecer_monto_reserva(self, producto_id, valor_reserva):
        query = "UPDATE productos SET valor_reserva = ? WHERE id = ?"
        values = (valor_reserva, producto_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("monto de reserva establecido exitosamente.")

    def modificar_precio(self, producto_id, nuevo_precio):
        query = "UPDATE productos SET precio_actual = ? WHERE id = ?"          
        values = (nuevo_precio, producto_id)
        self.cursor.execute(query, values)
        self.conn.commit()
        print("Precio modificado exitosamente.")

    def cerrar_conexion(self):
        self.conn.close()

if __name__ == "__main__":
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


