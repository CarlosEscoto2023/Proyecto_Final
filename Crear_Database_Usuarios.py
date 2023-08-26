import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Usuario')
cur.execute('CREATE TABLE Usuario (Nombre TEXT NOT NULL, Nombre_Usuario TEXT NOT NULL, Correo TEXT NOT NULL, Contraseña TEXT NOT NULL)')
conn.close()