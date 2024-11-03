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

USUARIOS = {
    "cliente" : "cliente123",
    "empleado" : "empleado123",
}

class SistemaTienda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Electrónica Mr.CrossFit - Sistema de Gestión")
        self.ventana.configure(bg=COLORES["fondo"])

        self.iniciar_sesion()

    def iniciar_sesion(self):
        self.limpiar_ventana()
        
        frame_login = tk.Frame(self.ventana, bg=COLORES["fondo"])
        frame_login.pack(padx=20, pady=20)

        tk.Label(
            frame_login,
            text="Iniciar Sesión",
            font=("Helvetica", 24, "bold"),
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(pady=20)

        tk.Label(frame_login, text="Usuario:", bg=COLORES["fondo"]).pack(pady=5)
        self.usuario_entry = ttk.Entry(frame_login)
        self.usuario_entry.pack(pady=5)

        tk.Label(frame_login, text="Contraseña:", bg=COLORES["fondo"]).pack(pady=5)
        self.contrasena_entry = ttk.Entry(frame_login, show="*")
        self.contrasena_entry.pack(pady=5)

        ttk.Button(frame_login, text="Iniciar Sesión", command=self.validar_usuario).pack(pady=10)

    def validar_usuario(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
            messagebox.showinfo("Éxito", f"Bienvenido {usuario}!")
            self.crear_db()
            self.crear_interfaz(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

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
                    categoria TEXT);
                """
            )

    def crear_interfaz(self, usuario):
        self.limpiar_ventana()

        self.frame_principal = tk.Frame(self.ventana, bg=COLORES["frame_principal"])
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Button(self.frame_principal, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=10)

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

    def cerrar_sesion(self):
        self.iniciar_sesion()

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
            self.entradas[campo] = {"widget": entrada, "tipo": config["tipo"]}

            if config["tipo"] in [int, float]:
                entrada.config(validate="key")
                if config["tipo"] is float:
                    entrada.config(
                        validatecommand=(container.register(self.validar_decimal), "%P")
                    )
                else:
                    entrada.config(
                        validatecommand=(container.register(self.validar_entero), "%P")
                    )

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
            entrada["widget"].delete(0, tk.END)
        self.categoria_var.set("")

    def guardar_producto(self):
        datos = {campo: entrada["widget"].get() for campo, entrada in self.entradas.items()}
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
        cantidad_seleccionados = len(seleccion)

        if cantidad_seleccionados == 0:
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")
            return
            
        mensaje = f"¿Está seguro de que desea eliminar {cantidad_seleccionados} producto(s)?"
        confirmacion = messagebox.askyesno("Confirmar Eliminación", mensaje)

        if confirmacion:
            for item in seleccion:
                id_producto = self.tabla.item(item)["values"][0]
                with conectar_db() as conn:
                    conn.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            
            self.actualizar_tabla()
            messagebox.showinfo("Producto Eliminado", "Los productos se han eliminado exitosamente.")
        else:
            messagebox.showinfo("Eliminación Cancelada", "La eliminación ha sido cancelada.")



ventana = tk.Tk()
app = SistemaTienda(ventana)
ventana.mainloop()