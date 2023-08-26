import sqlite3

class Database:
    def __init__(self, archivo: str, tabla: str):
        self.archivo = archivo
        self.table = tabla
    
    def create_table(self, campos: list):
        with sqlite3.connect(self.archivo) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {self.table}")
            params = ", ".join(campos)
            sql = f"CREATE TABLE {self.table} ({params})"
            cursor.execute(sql)
            conn.commit()

    def agregar(self, datos: dict):
        with sqlite3.connect(self.archivo) as conn:
            cursor = conn.cursor()
            fields = ", ".join(list(datos.keys()))
            comodines = ["?"] * len(
                datos
            )  # hace una lista de ? segun la cantidad de campos
            params = tuple(datos.values())
            sql = f"INSERT INTO {self.table} ({fields}) VALUES({','.join(comodines)})"
            cursor.execute(sql, params)
            conn.commit()
     