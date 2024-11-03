"""
Es una tienda de piezas electrónicas.

Andres Sebastian Toscano Martinez - 02230131068
Keiver Esneid Castellanos Julio - 02230131035

"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def conectar_db():
    return sqlite3.connect("inventario_componentes.db")


COLORES = {
    "fondo": "#E3F2FD",
    "frame_principal": "#FFFFFF",
    "boton_primario": "#1976D2",
    "boton_secundario": "#64B5F6",
    "texto": "#1A237E",
    "error": "#EF5350",
}

CAMPOS = {
    "modelo": {"label": "Modelo", "tipo": str, "required": True},
    "nombre": {"label": "Nombre", "tipo": str, "required": True},
    "especificaciones": {"label": "Especificaciones", "tipo": str, "required": True},
    "precio": {
        "label": "Precio",
        "tipo": float,
        "required": True,
        "validacion": lambda x: x.replace(".", "", 1).isdigit() if x else False,
    },
    "cantidad": {
        "label": "Cantidad",
        "tipo": int,
        "required": True,
        "validacion": lambda x: x.isdigit() if x else False,
    },
}

CATEGORIAS = {
    "microcontroladores": "Microcontroladores (Arduino, ESP32, PIC)",
    "pasivos": "Componentes Pasivos (R, C, L)",
    "activos": "Componentes Activos (Transistores, CI)",
    "sensores": "Sensores (Temp, Humedad)",
    "modulos": "Módulos (WiFi, Bluetooth)",
    "herramientas": "Herramientas",
    "accesorios": "Accesorios",
}


class SistemaTienda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Electrónica Mr.CrossFit - Sistema de Gestión")
        self.ventana.configure(bg=COLORES["fondo"])

        ancho, alto = 1200, 700
        x = (ventana.winfo_screenwidth() - ancho) // 2
        y = (ventana.winfo_screenheight() - alto) // 2
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.crear_db()
        self.crear_interfaz()

    def crear_db(self):
        with conectar_db() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modelo TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    especificaciones TEXT,
                    precio REAL,
                    cantidad INTEGER,
                    categoria TEXT
                )
            """
            )

    def crear_interfaz(self):
        self.frame_principal = tk.Frame(self.ventana, bg=COLORES["frame_principal"])
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            self.frame_principal,
            text="Electrónica Mr.CrossFit - Sistema de Inventario",
            font=("Helvetica", 24, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["texto"],
        ).pack(pady=20)

        container = tk.Frame(self.frame_principal, bg=COLORES["frame_principal"])
        container.pack(fill="both", expand=True)

        self.crear_formulario(container)
        self.crear_tabla(container)

    def crear_formulario(self, container):
        form_frame = tk.LabelFrame(
            container,
            text="Agregar Nuevo Producto",
            font=("Helvetica", 12, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["texto"],
        )
        form_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        self.entradas = {}
        for campo, config in CAMPOS.items():
            frame = tk.Frame(form_frame, bg=COLORES["frame_principal"])
            frame.pack(fill="x", padx=5, pady=5)

            tk.Label(
                frame,
                text=f"{config['label']}:",
                font=("Helvetica", 11),
                bg=COLORES["frame_principal"],
            ).pack(side="left")

            entrada = ttk.Entry(frame)
            entrada.pack(side="left", padx=5, fill="x", expand=True)
            self.entradas[campo] = entrada

        frame = tk.Frame(form_frame, bg=COLORES["frame_principal"])
        frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            frame,
            text="Categoría:",
            font=("Helvetica", 11),
            bg=COLORES["frame_principal"],
        ).pack(side="left")

        self.categoria_var = ttk.Combobox(
            frame, values=list(CATEGORIAS.values()), state="readonly"
        )
        self.categoria_var.pack(side="left", padx=5, fill="x", expand=True)

        frame_botones = tk.Frame(form_frame, bg=COLORES["frame_principal"])
        frame_botones.pack(fill="x", padx=5, pady=15)

        ttk.Button(frame_botones, text="Guardar", command=self.guardar_producto).pack(
            side="left", padx=5
        )
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_campos).pack(
            side="left", padx=5
        )

    def crear_tabla(self, container):
        tabla_frame = tk.LabelFrame(
            container,
            text="Inventario",
            font=("Helvetica", 12, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["texto"],
        )
        tabla_frame.pack(side="right", padx=10, pady=5, fill="both", expand=True)

        busqueda_frame = tk.Frame(tabla_frame, bg=COLORES["frame_principal"])
        busqueda_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            busqueda_frame, text="Filtrar por:", bg=COLORES["frame_principal"]
        ).pack(side="left", padx=(0, 5))

        self.filtro_cat = ttk.Combobox(
            busqueda_frame,
            values=["Todas"] + list(CATEGORIAS.values()),
            state="readonly",
            width=30,
        )
        self.filtro_cat.set("Todas")
        self.filtro_cat.pack(side="left", padx=5)
        self.filtro_cat.bind("<<ComboboxSelected>>", lambda e: self.actualizar_tabla())

        tk.Label(busqueda_frame, text="Buscar:", bg=COLORES["frame_principal"]).pack(
            side="left", padx=(20, 5)
        )

        self.busqueda_entrada = ttk.Entry(busqueda_frame, width=30)
        self.busqueda_entrada.pack(side="left", padx=5)

        ttk.Button(
            busqueda_frame, text="🔍 Buscar", command=self.actualizar_tabla
        ).pack(side="left", padx=5)

        columnas = (
            "ID",
            "Modelo",
            "Nombre",
            "Especificaciones",
            "Precio",
            "Cantidad",
            "Categoría",
        )
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)

        self.tabla.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(
            tabla_frame, orient="vertical", command=self.tabla.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        ttk.Button(
            tabla_frame, text="Eliminar Seleccionado", command=self.eliminar_producto
        ).pack(pady=5)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        categoria = self.filtro_cat.get()
        termino_busqueda = self.busqueda_entrada.get().strip().lower()

        with conectar_db() as conn:
            if categoria == "Todas":
                if termino_busqueda:
                    productos = conn.execute(
                        """
                        SELECT * FROM productos 
                        WHERE LOWER(nombre) LIKE ? OR LOWER(modelo) LIKE ?
                    """,
                        (f"%{termino_busqueda}%", f"%{termino_busqueda}%"),
                    ).fetchall()
                else:
                    productos = conn.execute("SELECT * FROM productos").fetchall()
            else:
                if termino_busqueda:
                    productos = conn.execute(
                        """
                        SELECT * FROM productos 
                        WHERE categoria = ? 
                        AND (LOWER(nombre) LIKE ? OR LOWER(modelo) LIKE ?)
                    """,
                        (categoria, f"%{termino_busqueda}%", f"%{termino_busqueda}%"),
                    ).fetchall()
                else:
                    productos = conn.execute(
                        "SELECT * FROM productos WHERE categoria = ?", (categoria,)
                    ).fetchall()

        if not productos:
            self.tabla.insert(
                "",
                "end",
                values=("No se encontraron productos", "", "", "", "", "", ""),
            )
        else:
            for producto in productos:
                self.tabla.insert("", "end", values=producto)

    def limpiar_campos(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.categoria_var.set("")

    def guardar_producto(self):
        datos = {campo: entrada.get() for campo, entrada in self.entradas.items()}
        datos["categoria"] = self.categoria_var.get()

        errores = []
        for campo, config in CAMPOS.items():
            if config["required"] and not datos[campo]:
                errores.append(f"El campo {config['label']} es obligatorio.")
            elif "validacion" in config and not config["validacion"](datos[campo]):
                errores.append(f"El valor de {config['label']} no es válido.")

        if errores:
            messagebox.showerror("Error de Validación", "\n".join(errores))
            return

        with conectar_db() as conn:
            conn.execute(
                """
                INSERT INTO productos (modelo, nombre, especificaciones, precio, cantidad, categoria)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    datos["modelo"],
                    datos["nombre"],
                    datos["especificaciones"],
                    float(datos["precio"]),
                    int(datos["cantidad"]),
                    datos["categoria"],
                ),
            )

        messagebox.showinfo(
            "Producto Guardado", "El producto se ha guardado con éxito."
        )
        self.limpiar_campos()
        self.actualizar_tabla()

    def eliminar_producto(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")
            return
        id_producto = self.tabla.item(seleccion[0])["values"][0]

        with conectar_db() as conn:
            conn.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        self.actualizar_tabla()
        messagebox.showinfo(
            "Producto Eliminado", "El producto se ha eliminado exitosamente."
        )


ventana = tk.Tk()
app = SistemaTienda(ventana)
ventana.mainloop()
