import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def conectar_db():
    return sqlite3.connect("inventario_componentes.db")


COLORES = {
    "fondo": "#FFFFFF",           # Pure white background
    "frame_principal": "#F9F9F9", # Subtle off-white
    "primario": "#2D3436",        # Rich charcoal
    "secundario": "#636E72",      # Sophisticated gray
    "acento": "#B8860B",         # Deep gold
    "acento_claro": "#DAA520",   # Light gold
    "texto": "#2D3436",          # Matching text color
    "texto_suave": "#636E72",    # Soft text
    "borde": "#DFE6E9",          # Subtle border
    "error": "#B33939",          # Elegant red
    "exito": "#218C74",          # Forest green
    "hover": "#34495E",          # Hover state
    "disabled": "#B2BEC3",       # Disabled state
    "seleccion": "#F8F9FA",      # Selected state
    "input_bg": "#FFFFFF",       # Input background
    "sombra": "#00000010"        # Subtle shadow
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
    "cliente": "cliente123",
    "empleado": "empleado123",
}


class SistemaTienda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Electrónica Mr.CrossFit - Sistema de Gestión")
        self.ventana.configure(bg=COLORES["fondo"])
        window_width = 1200
        window_height = 700
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.ventana.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.iniciar_sesion()

    def iniciar_sesion(self):
        self.limpiar_ventana()
        self.ventana.geometry("1200x700")
        
        container = tk.Frame(self.ventana, bg=COLORES["fondo"])
        container.pack(fill="both", expand=True)
        
        left_panel = tk.Frame(container, bg=COLORES["primario"], width=600)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)
        
        brand_frame = tk.Frame(left_panel, bg=COLORES["primario"])
        brand_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            brand_frame,
            text="ELECTRÓNICA",
            font=("Helvetica", 42, "bold"),
            bg=COLORES["primario"],
            fg="white"
        ).pack()
        
        tk.Label(
            brand_frame,
            text="Mr.CrossFit",
            font=("Helvetica", 24),
            bg=COLORES["primario"],
            fg="white"
        ).pack()
        
        right_panel = tk.Frame(container, bg="white", width=600)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        login_frame = tk.Frame(right_panel, bg="white")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            login_frame,
            text="Bienvenido",
            font=("Helvetica", 28, "bold"),
            bg="white",
            fg=COLORES["texto"]
        ).pack(pady=(0,40))
        
        tk.Label(
            login_frame,
            text="Usuario",
            font=("Helvetica", 12),
            bg="white",
            fg=COLORES["texto"]
        ).pack(anchor="w")
        
        self.usuario_entry = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="#F8F9FA",
            relief="flat",
            width=30
        )
        self.usuario_entry.pack(ipady=8, pady=(5,20))
        
        tk.Label(
            login_frame,
            text="Contraseña",
            font=("Helvetica", 12),
            bg="white",
            fg=COLORES["texto"]
        ).pack(anchor="w")
        
        self.contrasena_entry = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="#F8F9FA",
            relief="flat",
            width=30,
            show="•"
        )
        self.contrasena_entry.pack(ipady=8, pady=5)
        
        login_btn = tk.Button(
            login_frame,
            text="Iniciar Sesión",
            font=("Helvetica", 12),
            bg=COLORES["primario"],
            fg="white",
            relief="flat",
            cursor="hand2",
            width=25,
            height=2,
            command=self.validar_usuario
        )
        login_btn.pack(pady=30)
        
        login_btn.bind("<Enter>", lambda e: login_btn.configure(bg=COLORES["secundario"]))
        login_btn.bind("<Leave>", lambda e: login_btn.configure(bg=COLORES["primario"]))
        self.ventana.bind('<Return>', lambda e: self.validar_usuario())

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
        self.frame_principal = tk.Frame(self.ventana, bg=COLORES["fondo"])
        self.frame_principal.pack(fill="both", expand=True)
        
        header = tk.Frame(self.frame_principal, bg=COLORES["primario"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        brand_frame = tk.Frame(header, bg=COLORES["primario"])
        brand_frame.pack(side="left", padx=30)
        
        tk.Label(
            brand_frame,
            text="ELECTRÓNICA",
            font=("Montserrat", 16, "bold"),
            bg=COLORES["primario"],
            fg=COLORES["acento"]
        ).pack(side="left")
        
        tk.Label(
            brand_frame,
            text="Mr.CrossFit",
            font=("Montserrat", 16),
            bg=COLORES["primario"],
            fg="white"
        ).pack(side="left", padx=(5,0))
        
        user_frame = tk.Frame(header, bg=COLORES["primario"])
        user_frame.pack(side="right", padx=30)
        
        tk.Label(
            user_frame,
            text=f"●  {usuario.title()}",
            font=("Helvetica", 12),
            bg=COLORES["primario"],
            fg=COLORES["acento"]
        ).pack(side="left", padx=(0,20))
        
        logout_btn = tk.Button(
            user_frame,
            text="Cerrar Sesión",
            font=("Helvetica", 10),
            bg=COLORES["primario"],
            fg="white",
            bd=0,
            activebackground=COLORES["secundario"],
            activeforeground="white",
            cursor="hand2",
            command=self.cerrar_sesion
        )
        logout_btn.pack(side="right")
        
        content = tk.Frame(self.frame_principal, bg=COLORES["fondo"])
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        if usuario == "empleado":
            forms_container = tk.Frame(content, bg=COLORES["fondo"], width=380)
            forms_container.pack(side="left", fill="y", padx=(0,30))
            forms_container.pack_propagate(False)
            
            self.crear_formulario(forms_container)
            self.crear_formulario_edicion(forms_container)
        
        table_container = tk.Frame(content, bg=COLORES["fondo"])
        table_container.pack(side="right", fill="both", expand=True)
        
        self.crear_tabla(table_container)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccion_tabla)
        
        style = ttk.Style()
        style.configure("Treeview",
            background="white",
            foreground=COLORES["texto"],
            fieldbackground="white",
            rowheight=35,
            font=("Helvetica", 10)
        )
        style.configure("Treeview.Heading",
            background="white",
            foreground=COLORES["primario"],  
            relief="flat",
            font=("Helvetica", 11, "bold")
        )
        style.map("Treeview.Heading",
            background=[('active', COLORES["borde"])], 
            foreground=[('active', COLORES["primario"])]
        )


    def crear_formulario_edicion(self, container):
        edit_frame = tk.LabelFrame(
            container,
            text="Editar Producto",
            font=("Helvetica", 12, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["texto"],
        )
        edit_frame.pack(side="top", padx=10, pady=5, fill="both")
        self.entradas_edicion = {}
        for campo, config in CAMPOS.items():
            frame = tk.Frame(edit_frame, bg=COLORES["frame_principal"])
            frame.pack(fill="x", padx=5, pady=5)

            tk.Label(
                frame,
                text=f"{config['label']}:",
                font=("Helvetica", 11),
                bg=COLORES["frame_principal"],
            ).pack(side="left")

            entrada = ttk.Entry(frame)
            entrada.pack(side="left", padx=5, fill="x", expand=True)
            entrada.configure(state='disabled')
            self.entradas_edicion[campo] = {"widget": entrada, "tipo": config["tipo"]}

        frame = tk.Frame(edit_frame, bg=COLORES["frame_principal"])
        frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            frame,
            text="Categoría:",
            font=("Helvetica", 11),
            bg=COLORES["frame_principal"],
        ).pack(side="left")

        self.categoria_edit_var = ttk.Combobox(
            frame, values=list(CATEGORIAS.values()), state='disabled'
        )
        self.categoria_edit_var.pack(side="left", padx=5, fill="x", expand=True)

        frame_botones = tk.Frame(edit_frame, bg=COLORES["frame_principal"])
        frame_botones.pack(fill="x", padx=5, pady=15)

        self.actualizar_btn = ttk.Button(frame_botones, text="Actualizar", 
                                       command=self.actualizar_producto, state='disabled')
        self.actualizar_btn.pack(side="left", padx=5)
        
        self.cancelar_btn = ttk.Button(frame_botones, text="Cancelar", 
                                     command=self.cancelar_edicion, state='disabled')
        self.cancelar_btn.pack(side="left", padx=5)

    def seleccion_tabla(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            self.habilitar_form_edicion()
        else:
            self.deshabilitar_form_edicion()

    def habilitar_form_edicion(self):
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].configure(state='normal')
        self.categoria_edit_var.configure(state='readonly')
        self.actualizar_btn.configure(state='normal')
        self.cancelar_btn.configure(state='normal')

    def deshabilitar_form_edicion(self):
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].configure(state='disabled')
        self.categoria_edit_var.configure(state='disabled')
        self.actualizar_btn.configure(state='disabled')
        self.cancelar_btn.configure(state='disabled')

    def cargar_producto_para_editar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto para editar")
            return
        
        item = self.tabla.item(seleccion[0])
        valores = item['values']
        
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].delete(0, tk.END)
        
        campos_ordenados = ["modelo", "nombre", "especificaciones", "precio", "cantidad"]
        for i, campo in enumerate(campos_ordenados):
            self.entradas_edicion[campo]["widget"].insert(0, valores[i+1])
        
        self.categoria_edit_var.set(valores[6])
        self.id_producto_actual = valores[0]

    def actualizar_producto(self):
        if not hasattr(self, 'id_producto_actual'):
            messagebox.showerror("Error", "No hay producto seleccionado para editar.")
            return

        datos = {campo: self.entradas_edicion[campo]["widget"].get() for campo in CAMPOS}
        datos["categoria"] = self.categoria_edit_var.get()

        if self.validar_datos(datos):
            with conectar_db() as conn:
                conn.execute(
                    """
                    UPDATE productos 
                    SET modelo=?, nombre=?, especificaciones=?, precio=?, cantidad=?, categoria=?
                    WHERE id=?
                    """,
                    (datos["modelo"], datos["nombre"], datos["especificaciones"], 
                     float(datos["precio"]), int(datos["cantidad"]), 
                     datos["categoria"], self.id_producto_actual)
                )
            messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
            self.cancelar_edicion()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos correctamente.")

    def eliminar_producto(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un producto para eliminar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            item = self.tabla.item(seleccion[0])
            id_producto = item['values'][0]
            
            with conectar_db() as conn:
                conn.execute("DELETE FROM productos WHERE id=?", (id_producto,))
            
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente")

    def cancelar_edicion(self):
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].delete(0, tk.END)
        self.categoria_edit_var.set("")
        if hasattr(self, 'id_producto_actual'):
            del self.id_producto_actual
        self.deshabilitar_form_edicion()

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
        form_frame.pack(side="top", padx=10, pady=5, fill="both")

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

        tk.Label(busqueda_frame, text="Buscar:", bg=COLORES["frame_principal"]).pack(side="left", padx=(5, 5))
        self.busqueda_entry = ttk.Entry(busqueda_frame)
        self.busqueda_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)
        self.busqueda_entry.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        botones_frame = tk.Frame(tabla_frame, bg=COLORES["frame_principal"])
        botones_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(botones_frame, text="Cargar para editar", command=self.cargar_producto_para_editar).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=5)

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=("ID", "Modelo", "Nombre", "Especificaciones", "Precio", "Cantidad", "Categoría"),
            show="headings",
            height=10,
        )
        self.tabla.pack(fill="both", expand=True)

        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)

        self.actualizar_tabla()

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

    def guardar_producto(self):
        datos = {campo: self.entradas[campo]["widget"].get() for campo in CAMPOS}
        datos["categoria"] = self.categoria_var.get()

        if self.validar_datos(datos):
            with conectar_db() as conn:
                conn.execute(
                    """
                    INSERT INTO productos (modelo, nombre, especificaciones, precio, cantidad, categoria)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (datos["modelo"], datos["nombre"], datos["especificaciones"], 
                     float(datos["precio"]), int(datos["cantidad"]), datos["categoria"])
                )
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos correctamente.")

    def limpiar_campos(self):
        for campo in CAMPOS:
            self.entradas[campo]["widget"].delete(0, tk.END)
        self.categoria_var.set("")

    def validar_datos(self, datos):
        for campo, config in CAMPOS.items():
            if config["required"] and not datos[campo]:
                return False
            if "validacion" in config and not config["validacion"](datos[campo]):
                return False
        return True

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        with conectar_db() as conn:
            query = "SELECT * FROM productos"
            filtros = []
            if self.filtro_cat.get() != "Todas":
                query += " WHERE categoria = ?"
                filtros.append(self.filtro_cat.get())

            if self.busqueda_entry.get():
                if 'WHERE' in query:
                    query += " AND (modelo LIKE ? OR nombre LIKE ? OR especificaciones LIKE ?)"
                else:
                    query += " WHERE (modelo LIKE ? OR nombre LIKE ? OR especificaciones LIKE ?)"
                filtros.extend(["%" + self.busqueda_entry.get() + "%"] * 3)

            cursor = conn.execute(query, filtros)
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=fila)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaTienda(root)
    root.mainloop()
