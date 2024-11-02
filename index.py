"""
Es una tienda de piezas electrónicas.

Andres Sebastian Toscano Martinez - 02230131068
Keiver Esneid Castellanos Julio - 02230131035

"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def conectar_db(consulta, parametros=None):
    conexion = sqlite3.connect("inventario_componentes.db")
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    if parametros:
        cursor.execute(consulta, parametros)
    else:
        cursor.execute(consulta)
    conexion.commit()
    resultado = [dict(fila) for fila in cursor.fetchall()]
    conexion.close()
    return resultado


class SistemaTienda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Gestión - ELECTROCrossFit")
        self.ventana.config(bg="#F0F4F8")
        ancho_ventana = 1600
        alto_ventana = 800
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.iniciar_interfaz()
        self.crear_tabla_productos()

    def crear_tabla_productos(self):
        consulta = """CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            especificaciones TEXT,
            precio REAL,
            cantidad INTEGER,
            categoria TEXT
        )"""
        conectar_db(consulta)

    def iniciar_interfaz(self):
        estilo = ttk.Style()
        estilo.configure("Custom.TEntry", padding=5)
        estilo.configure("Custom.TButton", padding=10)
        marco_principal = tk.Frame(self.ventana, bg="#F0F4F8", padx=20, pady=20)
        marco_principal.pack(fill="both", expand=True)
        marco_titulo = tk.Frame(marco_principal, bg="#F0F4F8")
        marco_titulo.pack(fill="x", pady=(0, 20))
        tk.Label(
            marco_titulo,
            text="ELECTROCrossFit - Sistema de Gestión",
            font=("Helvetica", 24, "bold"),
            bg="#F0F4F8",
            fg="#1A365D",
        ).pack()
        marco_contenido = tk.Frame(marco_principal, bg="#F0F4F8")
        marco_contenido.pack(fill="both", expand=True)
        self.crear_formulario(marco_contenido)
        self.crear_tabla(marco_contenido)

    def crear_formulario(self, padre):
        marco_form = tk.Frame(padre, bg="white", padx=30, pady=20)
        marco_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        marco_form.config(relief="ridge", bd=1)
        tk.Label(
            marco_form,
            text="Agregar Nuevo Componente",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#2C5282",
        ).pack(pady=(0, 20))
        campos = {
            "Modelo": {"tipo": str},
            "Nombre": {"tipo": str},
            "Especificaciones": {"tipo": str},
            "Precio": {"tipo": float},
            "Cantidad": {"tipo": int},
        }
        self.entradas = {}
        for nombre, config in campos.items():
            marco_campo = tk.Frame(marco_form, bg="white")
            marco_campo.pack(fill="x", pady=5)
            tk.Label(
                marco_campo,
                text=f"{nombre}:",
                font=("Helvetica", 12),
                bg="white",
                width=15,
                anchor="w",
            ).pack(side="left")
            entrada = ttk.Entry(marco_campo, style="Custom.TEntry", width=30)
            entrada.pack(side="left", padx=(10, 0))
            self.entradas[nombre] = {"widget": entrada, "tipo": config["tipo"]}
            if config["tipo"] in [int, float]:
                entrada.config(validate="key")
                if config["tipo"] == float:
                    entrada.config(
                        validatecommand=(padre.register(self.validar_decimal), "%P")
                    )
                else:
                    entrada.config(
                        validatecommand=(padre.register(self.validar_entero), "%P")
                    )
        marco_categoria = tk.Frame(marco_form, bg="white")
        marco_categoria.pack(fill="x", pady=5)
        tk.Label(
            marco_categoria,
            text="Categoría:",
            font=("Helvetica", 12),
            bg="white",
            width=15,
            anchor="w",
        ).pack(side="left")
        self.categorias = {
            "Microcontroladores": {"descripcion": "Arduino, ESP32, PIC, etc."},
            "Componentes Pasivos": {
                "descripcion": "Resistencias, capacitores, inductores"
            },
            "Componentes Activos": {"descripcion": "Transistores, CI, reguladores"},
            "Sensores": {"descripcion": "Temperatura, humedad, proximidad"},
            "Módulos": {"descripcion": "Bluetooth, WiFi, RF, displays"},
            "Herramientas": {"descripcion": "Cautín, multímetro, pinzas"},
            "Accesorios": {"descripcion": "Cables, protoboards, baterías"},
        }
        self.categoria_var = ttk.Combobox(
            marco_categoria,
            values=list(self.categorias.keys()),
            width=27,
            state="readonly",
        )
        self.categoria_var.pack(side="left", padx=(10, 0))
        marco_botones = tk.Frame(marco_form, bg="white")
        marco_botones.pack(fill="x", pady=20)
        ttk.Button(
            marco_botones,
            text="Agregar Componente",
            style="Custom.TButton",
            command=self.agregar_producto,
        ).pack(side="left", padx=5)
        ttk.Button(
            marco_botones,
            text="Limpiar Campos",
            style="Custom.TButton",
            command=self.limpiar_campos,
        ).pack(side="left", padx=5)

    def crear_tabla(self, padre):
        marco_tabla = tk.Frame(padre, bg="white", padx=30, pady=20)
        marco_tabla.pack(side="right", fill="both", expand=True, padx=(10, 0))
        marco_tabla.config(relief="ridge", bd=1)
        marco_filtros = tk.Frame(marco_tabla, bg="white")
        marco_filtros.pack(fill="x", pady=(0, 20))
        tk.Label(
            marco_filtros,
            text="Filtrar por categoría:",
            font=("Helvetica", 12),
            bg="white",
        ).pack(side="left", padx=(0, 10))
        self.filtro_categoria = ttk.Combobox(
            marco_filtros,
            values=["Todas"] + list(self.categorias.keys()),
            width=20,
            state="readonly",
        )
        self.filtro_categoria.set("Todas")
        self.filtro_categoria.pack(side="left", padx=(0, 20))
        self.filtro_categoria.bind(
            "<<ComboboxSelected>>", lambda e: self.filtrar_productos()
        )
        tk.Label(
            marco_filtros, text="Buscar:", font=("Helvetica", 12), bg="white"
        ).pack(side="left", padx=(0, 10))
        self.entrada_buscar = ttk.Entry(marco_filtros, style="Custom.TEntry", width=40)
        self.entrada_buscar.pack(side="left", padx=(0, 10))
        ttk.Button(
            marco_filtros,
            text="Buscar",
            style="Custom.TButton",
            command=self.buscar_producto,
        ).pack(side="left")
        columnas = {
            "ID": {"ancho": 50},
            "Modelo": {"ancho": 100},
            "Nombre": {"ancho": 200},
            "Especificaciones": {"ancho": 200},
            "Precio": {"ancho": 80},
            "Cantidad": {"ancho": 80},
            "Categoría": {"ancho": 150},
        }
        self.tabla = ttk.Treeview(
            marco_tabla, columns=list(columnas.keys()), show="headings", height=20
        )
        for col, config in columnas.items():
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=config["ancho"], anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=10)
        barra_desplazamiento = ttk.Scrollbar(
            marco_tabla, orient="vertical", command=self.tabla.yview
        )
        barra_desplazamiento.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)
        marco_acciones = tk.Frame(marco_tabla, bg="white")
        marco_acciones.pack(fill="x", pady=10)
        ttk.Button(
            marco_acciones,
            text="Eliminar Seleccionado",
            style="Custom.TButton",
            command=self.eliminar_producto,
        ).pack(side="left", padx=5)
        ttk.Button(
            marco_acciones,
            text="Actualizar Lista",
            style="Custom.TButton",
            command=self.actualizar_tabla,
        ).pack(side="left", padx=5)

    def validar_decimal(self, valor):
        if valor == "":
            return True
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def validar_entero(self, valor):
        if valor == "":
            return True
        return valor.isdigit()

    def agregar_producto(self):
        datos = {}
        for nombre, config in self.entradas.items():
            valor = config["widget"].get()
            if not valor:
                messagebox.showwarning(
                    "Advertencia", f"El campo {nombre} no puede estar vacío."
                )
                return
            try:
                datos[nombre] = config["tipo"](valor)
            except ValueError:
                messagebox.showwarning(
                    "Advertencia", f"El valor en {nombre} no es válido."
                )
                return
        categoria = self.categoria_var.get()
        if not categoria:
            messagebox.showwarning("Advertencia", "Debe seleccionar una categoría.")
            return
        datos["categoria"] = categoria
        consulta = "INSERT INTO productos (modelo, nombre, especificaciones, precio, cantidad, categoria) VALUES (?, ?, ?, ?, ?, ?)"
        conectar_db(
            consulta,
            (
                datos["Modelo"],
                datos["Nombre"],
                datos["Especificaciones"],
                datos["Precio"],
                datos["Cantidad"],
                datos["categoria"],
            ),
        )
        messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
        self.actualizar_tabla()
        self.limpiar_campos()

    def limpiar_campos(self):
        for config in self.entradas.values():
            config["widget"].delete(0, "end")
        self.categoria_var.set("")

    def eliminar_producto(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Seleccione un producto para eliminar."
            )
            return
        producto = self.tabla.item(seleccion)["values"]
        consulta = "DELETE FROM productos WHERE id = ?"
        conectar_db(consulta, (producto[0],))
        messagebox.showinfo("Éxito", "Producto eliminado.")
        self.actualizar_tabla()

    def filtrar_productos(self):
        categoria = self.filtro_categoria.get()
        texto_busqueda = self.entrada_buscar.get()
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        conexion = sqlite3.connect("inventario_componentes.db")
        cursor = conexion.cursor()
        if categoria == "Todas":
            if texto_busqueda:
                cursor.execute(
                    "SELECT * FROM productos WHERE nombre LIKE ?",
                    ("%" + texto_busqueda + "%",),
                )
            else:
                cursor.execute("SELECT * FROM productos")
        else:
            if texto_busqueda:
                cursor.execute(
                    "SELECT * FROM productos WHERE categoria = ? AND nombre LIKE ?",
                    (categoria, "%" + texto_busqueda + "%"),
                )
            else:
                cursor.execute(
                    "SELECT * FROM productos WHERE categoria = ?", (categoria,)
                )
        productos = cursor.fetchall()
        conexion.close()
        for producto in productos:
            self.tabla.insert("", "end", values=producto)

    def buscar_producto(self):
        self.filtrar_productos()

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        conexion = sqlite3.connect("inventario_componentes.db")
        cursor = conexion.cursor()
        categoria = self.filtro_categoria.get()
        if categoria == "Todas":
            cursor.execute("SELECT * FROM productos")
        else:
            cursor.execute("SELECT * FROM productos WHERE categoria = ?", (categoria,))
        productos = cursor.fetchall()
        conexion.close()
        for producto in productos:
            self.tabla.insert("", "end", values=producto)


if __name__ == "__main__":
    ventana = tk.Tk()
    sistema = SistemaTienda(ventana)
    ventana.mainloop()
