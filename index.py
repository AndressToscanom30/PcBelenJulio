'''
Es una tienda de técnología
''' 
import sqlite3
import tkinter as tk

#Funciones CRUD

def create(nombre, precio, color, descripcion, stock):

    nombre = entrada_nombre.get()
    precio = entrada_precio.get()
    color = entrada_precio.get()


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
ventana.title("PcBelenJulio")
ventana.geometry("1200x700")

contenedor_crud = tk.Frame(ventana, width=1180, height=500, relief="groove", bd=2)
contenedor_crud.grid(row=0, column=0, padx=10, pady=10)

contenedor_crud.grid_propagate(False)

agregar = tk.Frame(contenedor_crud, bg='#4CAF50')
agregar.grid(row=0, column=0, padx=5, pady=5)

label_nombre = tk.Label(agregar, text="Nombre", bg='#4CAF50',fg='#FFFFFF', font=("Arial", 10, "bold"))
label_nombre.grid(row=0, column=0, padx=8, pady=10)
entrada_nombre = tk.Entry(agregar)
entrada_nombre.grid(row=0, column=1, padx=8, pady=10)

label_precio = tk.Label(agregar, text="Precio", bg='#4CAF50',fg='#FFFFFF', font=("Arial", 10, "bold"))
label_precio.grid(row=1, column=0, padx=8, pady=10)
entrada_precio = tk.Entry(agregar)
entrada_precio.grid(row=1, column=1, padx=8, pady=10)

label_color = tk.Label(agregar, text="Color", bg='#4CAF50',  fg='#FFFFFF', font=("Arial", 10, "bold"))
label_color.grid(row=2, column=0, padx=8, pady=10)
entrada_color = tk.Entry(agregar)
entrada_color.grid(row=2, column=1, padx=8, pady=10)

label_descripcion = tk.Label(agregar, text="Descripción", bg='#4CAF50', fg='#FFFFFF', font=("Arial", 10, "bold"))
label_descripcion.grid(row=3, column=0, padx=8, pady=10)
entrada_descripcion = tk.Entry(agregar)
entrada_descripcion.grid(row=3, column=1, padx=8, pady=10)

label_stock = tk.Label(agregar, text="Stock", bg='#4CAF50', fg='#FFFFFF', font=("Arial", 10, "bold"))
label_stock.grid(row=4, column=0, padx=8, pady=10)
entrada_stock = tk.Entry(agregar)
entrada_stock.grid(row=4, column=1, padx=8, pady=10)

agregar_button = tk.Button(agregar, text="Agregar", width=20)
agregar_button.grid(row=5, column=0, columnspan=2, pady=15, sticky="ns")

ventana.mainloop()