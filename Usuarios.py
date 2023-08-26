import sqlite3
from Productos import TiendaVirtualAdmin

class TiendaVirtualUsuario:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos_en_pedidos (
                id INTEGER PRIMARY KEY,
                pedido_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
    
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY,
                direccion_entrega TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reservaciones (
                id_producto INTEGER,
                valor_reserva INTEGER
            )
        ''')
        
        self.conn.commit()

    def hacer_reservacion(self, id_producto, monto):
        query = "SELECT nombre, precio_original, valor_reserva FROM productos WHERE id = ?"
        self.cursor.execute(query, (id_producto,))
        producto = self.cursor.fetchone()

        if producto and monto >= producto[2]:
            query_reservar = "INSERT INTO Reservaciones (id_producto, valor_reserva) VALUES (?, ?)"
            self.cursor.execute(query_reservar, (id_producto, monto))
            self.conn.commit()
            print(f"Reservación exitosa para {producto[0]}.")
        else:
            print("No se pudo realizar la reservación. El monto no cumple con el mínimo requerido.")


    def generar_pedido(self, productos_seleccionados):
        total = sum(producto['precio_original'] for producto in productos_seleccionados)
        print("Detalle del pedido:")
        for producto in productos_seleccionados:
            print(f"Producto: {producto['nombre']}, _original_original: {producto['precio_original']}")
        print(f"Total a pagar: {total}")

        opcion_generar = input("¿Desea generar el pedido? (s/n): ")
        if opcion_generar.lower() == "s":
            self.cursor.execute("INSERT INTO pedidos (direccion_entrega) VALUES (?)", ("",))
            self.conn.commit()
            pedido_id = self.cursor.lastrowid
            for producto in productos_seleccionados:
                self.cursor.execute("INSERT INTO productos_en_pedidos (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)",
                                    (pedido_id, producto['id'], 1))
                self.conn.commit()
            print("Pedido generado exitosamente.")

    def pagar_pedido(self, pedido_id):
        query_pedido = """
             SELECT id, direccion_entrega
             FROM pedidos
             WHERE id = ?
         """
        self.cursor.execute(query_pedido, (pedido_id,))
        pedido = self.cursor.fetchone()

        if pedido:
            print("\nDetalle del pedido a pagar:")
            print(f"ID del pedido: {pedido[0]}")
            print(f"Dirección de entrega actual: {pedido[1]}")

            nueva_direccion_entrega = input("Ingrese la nueva dirección de entrega: ")

            query_productos_en_pedido = """
                SELECT productos_en_pedidos.id, productos.nombre, productos.precio_original, productos_en_pedidos.cantidad
                FROM productos_en_pedidos
                INNER JOIN productos ON productos.id = productos_en_pedidos.producto_id
                WHERE productos_en_pedidos.pedido_id = ?
            """
            self.cursor.execute(query_productos_en_pedido, (pedido_id,))
            productos_en_pedido = self.cursor.fetchall()

            total = 0
            print("\nProductos en el pedido:")
            for producto in productos_en_pedido:
                print(f"ID del producto en pedido: {producto[0]}, Producto: {producto[1]}, precio_original unitario: {producto[2]}, Cantidad: {producto[3]}")
                total += producto[2] * producto[3]

            print(f"Total a pagar: {total}")

            opcion_ver_pedido = input("\n¿Desea ver el detalle completo del pedido antes de proceder al pago? (s/n): ")
            if opcion_ver_pedido.lower() == "s":
                print("\nDetalle completo del pedido:")
                for producto in productos_en_pedido:
                    print(f"ID del producto en pedido: {producto[0]}, Producto: {producto[1]}, _original_original unitario: {producto[2]}, Cantidad: {producto[3]}")
                print(f"Total a pagar: {total}")

            opcion_pago = input("\nDesea proceder al pago? (s/n): ")
            if opcion_pago.lower() == "s":
                print("Procesando pago...")
                numero_tarjeta = input("Ingrese el número de tarjeta de crédito: ")
                fecha_vencimiento = input("Ingrese la fecha de vencimiento (MM/AA): ")
                cvv = input("Ingrese el CVV: ")
                if numero_tarjeta and fecha_vencimiento and cvv:
                    print("Tarjeta válida. Procesando pago...")
                    print("Pago realizado con éxito.")
                    fecha_entrega = "3 días después de la fecha de pago"
                    print(f"Pedido pagado exitosamente. Será entregado en la dirección: {nueva_direccion_entrega}, en {fecha_entrega}.")
                else:
                        print("Tarjeta inválida. Pago cancelado.")
            else:
                print("Pago cancelado.")
        else:
            print("Pedido no encontrado.")

    def cancelar_pedido(self):
        print("Pedido cancelado.")

    def mostrar_productos(self):
        query = "SELECT id, nombre, precio_original, valor_reserva FROM productos WHERE habilitado = 1"
        self.cursor.execute(query)
        productos = self.cursor.fetchall()
        print("Productos disponibles:")
        for producto in productos:
            print(f"ID: {producto[0]}, Producto: {producto[1]}, Precio Original: {producto[2]}, Precio Reserva: {producto[3]}")
            
    def mostrar_pedidos(self):
        query = "SELECT id FROM pedidos"
        self.cursor.execute(query)
        pedidos = self.cursor.fetchall()
        if pedidos:
            print("IDs de los pedidos realizados:")
            for pedido in pedidos:
                print(f"ID del pedido: {pedido[0]}")
        else:
            print("Aún no ha realizado ningún pedido.")

    def cerrar_conexion(self):
        self.conn.close()
        
if __name__ == "__main__":
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
            admin.cerrar_conexion()
            usuario.cerrar_conexion()
            break
