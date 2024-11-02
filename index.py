'''
Es una tienda de técnología
''' 
import sqlite3
import tkinter as tk

#Funciones CRUD

def create(nombre, precio, color, descripcion, stock):
    conexion = sqlite3.connect('PCBelenJulio.db')
    cursor = conexion.cursor()



    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre VARCHAR(100), 
        precio DECIMAL(10, 2), 
        color VARCHAR(50), 
        descripcion TEXT, 
        stock INTEGER CHECK (stock >= 0))
        ''')

    cursor.execute('''
        INSERT INTO productos(nombre, precio, color, descripcion, stock)
        VALUES(?, ?, ?, ?, ?)''', (nombre, precio, color, descripcion, stock)          
        )
    
    conexion.commit()
    conexion.close()

    print(f"Producto {nombre} agregado correctamente.")


def read():
    pass

def update():
    pass

def delete():
    pass


#GUI

ventana = tk.Tk()

print("Hello world")