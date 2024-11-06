"""
PROGRAMA PARA LA GESTION DE UNA TIENDA DE PARTES ELECTRONICAS

- Andres Sebastian Toscano Martinez - 02230131068
- Keiver Esneid Castellanos Julio - 02230131035

CREDENCIALES**************************************************************************************
    Usuario: cliente, Contraseña: cliente123
    Usuario: empleado, Contraseña: empleado123
    
En este codigo se usa una libreria para poder generar las facturas
por un pdf, para instalarla ejecute el siguiente comando:
-pip install reportlab
Si por algun caso genera error al ejecutar, comentar o eliminar el metoddo generar_factura_pdf
y comentar o eliminar la linea 1001 a la 1007.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generar_factura_pdf(nombre_producto, descripcion, cantidad, precio_unitario, total):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nombre_archivo = f"Factura_{nombre_producto}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    ruta_pdf = os.path.join(os.getcwd(), nombre_archivo)
    
    pdf = canvas.Canvas(ruta_pdf, pagesize=A4)
    pdf.setTitle("Factura de Compra")
    
    pdf.setFillColorRGB(0.18, 0.20, 0.21)
    pdf.rect(0, 750, 595, 100, fill=True)
    
    pdf.setFillColorRGB(0.72, 0.53, 0.04)  
    pdf.setFont("Helvetica-Bold", 32)
    pdf.drawString(50, 785, "ELECTRÓNICA")
    
    pdf.setFillColorRGB(1, 1, 1)  
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, 815, "Mr.CrossFit")
    
    pdf.setStrokeColorRGB(0.72, 0.53, 0.04)
    pdf.setLineWidth(3)
    pdf.line(50, 770, 545, 770)
    
    pdf.setFillColorRGB(0.72, 0.53, 0.04)
    pdf.rect(395, 650, 150, 80, fill=True)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(405, 705, "FACTURA")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(405, 685, f"No. {datetime.now().strftime('%Y%m%d%H%M')}")
    pdf.drawString(405, 665, f"Fecha: {fecha_actual}")
    
    pdf.setFillColorRGB(0.18, 0.20, 0.21)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 680, "¡DETALLES DE TU COMPRA!")
    
    pdf.setStrokeColorRGB(0.72, 0.53, 0.04)
    pdf.setLineWidth(2)
    pdf.rect(45, 560, 505, 100, stroke=True)
    
    pdf.setFillColorRGB(0.18, 0.20, 0.21)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 630, "Producto:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(170, 630, nombre_producto)
    
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 600, "Descripción:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(170, 600, descripcion)
    
    y_pos = 520
    pdf.setFillColorRGB(0.72, 0.53, 0.04)
    pdf.rect(50, y_pos, 495, 25, fill=True)
    
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, y_pos+7, "CANTIDAD")
    pdf.drawString(200, y_pos+7, "PRECIO UNITARIO")
    pdf.drawString(400, y_pos+7, "TOTAL")
    
    pdf.setFillColorRGB(0.18, 0.20, 0.21)
    y_pos -= 30
    pdf.setFont("Helvetica", 11)
    pdf.drawString(75, y_pos, f"{cantidad} unidades")
    pdf.drawString(210, y_pos, f"${precio_unitario:,.2f}")
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(405, y_pos, f"${total:,.2f}")
    
    pdf.setFillColorRGB(0.72, 0.53, 0.04)
    pdf.rect(300, y_pos-60, 245, 40, fill=True)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(310, y_pos-40, f"TOTAL: ${total:,.2f}")
    
    pdf.setFillColorRGB(0.18, 0.20, 0.21)
    pdf.rect(0, 0, 595, 80, fill=True)
    
    pdf.setFillColorRGB(0.72, 0.53, 0.04)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(297, 55, "¡GRACIAS POR TU COMPRA!")
    
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(297, 35, "Electrónica Mr.CrossFit - ¡La Tecnología que mueve el alma!")
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(297, 15, "Contáctanos: electronica@mrcrossfit.com | Tel: +57 317 855 1756")
    
    pdf.setStrokeColorRGB(0.72, 0.53, 0.04)
    pdf.setLineWidth(3)
    for i in range(3):
        pdf.line(50 + i*200, 90, 150 + i*200, 90)
    
    pdf.save()

def validar_texto(char):
    return char.isalpha() or char.isspace() or char == "-" or char.isdigit()


def validar_numerico(char):
    return char.isdigit()


def validar_flotante(char):
    return char.isdigit() or char == "." or char == ""


def conectar_base_datos():
    try:
        return sqlite3.connect("inventario_componentes.db")
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"Error al conectar: {str(e)}")
        return None


COLORES = {
    "fondo": "#FFFFFF",
    "frame_principal": "#F9F9F9",
    "primario": "#2D3436",
    "secundario": "#636E72",
    "acento": "#B8860B",
    "acento_claro": "#DAA520",
    "texto": "#2D3436",
    "texto_suave": "#636E72",
    "borde": "#DFE6E9",
    "error": "#B33939",
    "exito": "#218C74",
    "hover": "#34495E",
    "disabled": "#B2BEC3",
    "seleccion": "#F8F9FA",
    "input_bg": "#FFFFFF",
    "sombra": "#00000010",
}

CAMPOS = {
    "modelo": {
        "label": "Modelo",
        "tipo": str,
        "required": True,
        "validate": validar_texto,
    },
    "nombre": {
        "label": "Nombre",
        "tipo": str,
        "required": True,
        "validate": validar_texto,
    },
    "especificaciones": {
        "label": "Especificaciones",
        "tipo": str,
        "required": True,
        "validate": validar_texto,
    },
    "precio": {
        "label": "Precio",
        "tipo": float,
        "required": True,
        "validate": validar_flotante,
        "validacion": lambda x: x.replace(".", "", 1).isdigit() if x else False,
    },
    "cantidad": {
        "label": "Cantidad",
        "tipo": int,
        "required": True,
        "validate": validar_numerico,
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
        self.rol_usuario = None
        window_width = 1200
        window_height = 700
        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.ventana.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
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
            fg="white",
        ).pack()

        tk.Label(
            brand_frame,
            text="Mr.CrossFit",
            font=("Helvetica", 24),
            bg=COLORES["primario"],
            fg="white",
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
            fg=COLORES["texto"],
        ).pack(pady=(0, 40))

        tk.Label(
            login_frame,
            text="Usuario",
            font=("Helvetica", 12),
            bg="white",
            fg=COLORES["texto"],
        ).pack(anchor="w")

        self.usuario_entry = tk.Entry(
            login_frame, font=("Helvetica", 12), bg="#F8F9FA", relief="flat", width=30
        )
        self.usuario_entry.pack(ipady=8, pady=(5, 20))

        tk.Label(
            login_frame,
            text="Contraseña",
            font=("Helvetica", 12),
            bg="white",
            fg=COLORES["texto"],
        ).pack(anchor="w")

        self.contrasena_entry = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="#F8F9FA",
            relief="flat",
            width=30,
            show="•",
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
            command=self.validar_usuario,
        )
        login_btn.pack(pady=30)

        login_btn.bind(
            "<Enter>", lambda e: login_btn.configure(bg=COLORES["secundario"])
        )
        login_btn.bind("<Leave>", lambda e: login_btn.configure(bg=COLORES["primario"]))
        self.ventana.bind("<Return>", lambda e: self.validar_usuario())

    def validar_usuario(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
            self.rol_usuario = usuario
            messagebox.showinfo("Éxito", f"Bienvenido {usuario}!")
            self.crear_base_datos()
            self.crear_interfaz(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def crear_base_datos(self):
        with conectar_base_datos() as conn:
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
            fg=COLORES["acento"],
        ).pack(side="left")

        tk.Label(
            brand_frame,
            text="Mr.CrossFit",
            font=("Montserrat", 16),
            bg=COLORES["primario"],
            fg="white",
        ).pack(side="left", padx=(5, 0))

        user_frame = tk.Frame(header, bg=COLORES["primario"])
        user_frame.pack(side="right", padx=30)

        tk.Label(
            user_frame,
            text=f"●  {usuario.title()}",
            font=("Helvetica", 12),
            bg=COLORES["primario"],
            fg=COLORES["acento"],
        ).pack(side="left", padx=(0, 20))

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
            command=self.cerrar_sesion,
        )
        logout_btn.pack(side="right")

        content = tk.Frame(self.frame_principal, bg=COLORES["fondo"])
        content.pack(fill="both", expand=True, padx=30, pady=30)

        if usuario == "empleado":
            forms_container = tk.Frame(content, bg=COLORES["fondo"], width=380)
            forms_container.pack(side="left", fill="y", padx=(0, 30))
            forms_container.pack_propagate(False)

            self.crear_formulario(forms_container)
            self.crear_formulario_edicion(forms_container)
        else:
            purchase_container = tk.Frame(content, bg=COLORES["fondo"], width=380)
            purchase_container.pack(side="left", fill="y", padx=(0, 30))
            purchase_container.pack_propagate(False)

            self.crear_interfaz_compra(purchase_container)

        table_container = tk.Frame(content, bg=COLORES["fondo"])
        table_container.pack(side="right", fill="both", expand=True)

        self.crear_tabla(table_container)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_elemento_tabla)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="white",
            foreground=COLORES["texto"],
            fieldbackground="white",
            rowheight=35,
            font=("Helvetica", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="white",
            foreground=COLORES["primario"],
            relief="flat",
            font=("Helvetica", 11, "bold"),
        )
        style.map(
            "Treeview.Heading",
            background=[("active", COLORES["borde"])],
            foreground=[("active", COLORES["primario"])],
        )

    def actualizar_detalles_producto(self, event=None):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            
            self.detalles_labels["modelo"].config(text=valores[1])
            self.detalles_labels["nombre"].config(text=valores[2])
            self.detalles_labels["precio"].config(text=f"${float(valores[4]):,.2f}")
            self.detalles_labels["cantidad"].config(text=f"{valores[5]} unidades")

    def actualizar_total(self, event=None):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            precio = float(valores[4])

            cantidad = self.cantidad_compra.get()
            if cantidad and cantidad.isdigit():
                total = precio * int(cantidad)
                self.total_label.configure(text=f"Total: ${total:.2f}")
            else:
                self.total_label.configure(text="Total: $0.00")

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
            entrada.configure(state="disabled")
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
            frame, values=list(CATEGORIAS.values()), state="disabled"
        )
        self.categoria_edit_var.pack(side="left", padx=5, fill="x", expand=True)

        frame_botones = tk.Frame(edit_frame, bg=COLORES["frame_principal"])
        frame_botones.pack(fill="x", padx=5, pady=15)

        self.actualizar_btn = ttk.Button(
            frame_botones,
            text="Actualizar",
            command=self.actualizar_producto,
            state="disabled",
        )
        self.actualizar_btn.pack(side="left", padx=5)

        self.cancelar_btn = ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.cancelar_edicion,
            state="disabled",
        )
        self.cancelar_btn.pack(side="left", padx=5)

    def seleccionar_elemento_tabla(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            
            if self.rol_usuario == "cliente":
                self.actualizar_detalles_producto(event)
            elif self.rol_usuario == "empleado":
                self.habilitar_formulario_edicion()

    def habilitar_formulario_edicion(self):
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].configure(state="normal")
        self.categoria_edit_var.configure(state="readonly")
        self.actualizar_btn.configure(state="normal")
        self.cancelar_btn.configure(state="normal")

    def deshabilitar_formulario_edicion(self):
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].configure(state="disabled")
        self.categoria_edit_var.configure(state="disabled")
        self.actualizar_btn.configure(state="disabled")
        self.cancelar_btn.configure(state="disabled")

    def cargar_producto_edicion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Por favor seleccione un producto para editar"
            )
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].delete(0, tk.END)

        campos_ordenados = [
            "modelo",
            "nombre",
            "especificaciones",
            "precio",
            "cantidad",
        ]
        for i, campo in enumerate(campos_ordenados):
            self.entradas_edicion[campo]["widget"].insert(0, valores[i + 1])

        self.categoria_edit_var.set(valores[6])
        self.id_producto_actual = valores[0]

    def actualizar_producto(self):
        if not hasattr(self, "id_producto_actual"):
            messagebox.showerror("Error", "No hay producto seleccionado para editar.")
            return

        datos = {
            campo: self.entradas_edicion[campo]["widget"].get() for campo in CAMPOS
        }
        datos["categoria"] = self.categoria_edit_var.get()

        if self.validar_datos(datos):
            with conectar_base_datos() as conn:
                conn.execute(
                    """
                    UPDATE productos
                    SET modelo=?, nombre=?, especificaciones=?, precio=?, cantidad=?, categoria=?
                    WHERE id=?
                    """,
                    (
                        datos["modelo"],
                        datos["nombre"],
                        datos["especificaciones"],
                        float(datos["precio"]),
                        int(datos["cantidad"]),
                        datos["categoria"],
                        self.id_producto_actual,
                    ),
                )
            messagebox.showinfo("Éxito", "Producto actualizado exitosamente.")
            self.cancelar_edicion()
            self.actualizar_tabla()
        else:
            messagebox.showerror(
                "Error", "Por favor, complete todos los campos correctamente."
            )

    def eliminar_producto(self):
        if self.rol_usuario != "empleado":
            messagebox.showwarning(
                "Acceso Denegado", "No tiene permisos para eliminar productos"
            )
            return

        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia", "Por favor seleccione un producto para eliminar"
            )
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            item = self.tabla.item(seleccion[0])
            id_producto = item["values"][0]

            with conectar_base_datos() as conn:
                conn.execute("DELETE FROM productos WHERE id=?", (id_producto,))

            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Producto eliminado exitosamente")

    def cancelar_edicion(self):
        for campo in self.entradas_edicion:
            self.entradas_edicion[campo]["widget"].delete(0, tk.END)
        self.categoria_edit_var.set("")
        if hasattr(self, "id_producto_actual"):
            del self.id_producto_actual
        self.deshabilitar_formulario_edicion()

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

            vcmd = (self.ventana.register(config["validate"]), "%S")
            entrada = ttk.Entry(frame, validate="key", validatecommand=vcmd)
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

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=(
                "ID",
                "Modelo",
                "Nombre",
                "Especificaciones",
                "Precio",
                "Cantidad",
                "Categoría",
            ),
            show="headings",
            height=10,
        )

        self.tabla.column("ID", width=50)
        self.tabla.column("Modelo", width=120)
        self.tabla.column("Nombre", width=150)
        self.tabla.column("Especificaciones", width=200)
        self.tabla.column("Precio", width=80)
        self.tabla.column("Cantidad", width=80)
        self.tabla.column("Categoría", width=180)

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Especificaciones", text="Especificaciones")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Categoría", text="Categoría")

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
            side="left", padx=(5, 5)
        )
        self.busqueda_entry = ttk.Entry(busqueda_frame)
        self.busqueda_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)
        self.busqueda_entry.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        botones_frame = tk.Frame(tabla_frame, bg=COLORES["frame_principal"])
        botones_frame.pack(fill="x", padx=5, pady=5)

        if self.rol_usuario == "empleado":
            ttk.Button(
                botones_frame,
                text="Cargar para editar",
                command=self.cargar_producto_edicion,
            ).pack(side="left", padx=5)
            ttk.Button(
                botones_frame, text="Eliminar", command=self.eliminar_producto
            ).pack(side="left", padx=5)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.actualizar_detalles_producto)

        if self.rol_usuario == "cliente":
            self.cantidad_compra.bind("<KeyRelease>", self.actualizar_total)

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
            with conectar_base_datos() as conn:
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
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            self.limpiar_campos()
            self.actualizar_tabla()
        else:
            messagebox.showerror(
                "Error", "Por favor, complete todos los campos correctamente."
            )

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

        with conectar_base_datos() as conn:
            query = "SELECT * FROM productos"
            filtros = []

            if self.filtro_cat.get() != "Todas":
                query += " WHERE categoria = ?"
                filtros.append(self.filtro_cat.get())

            if self.busqueda_entry.get():
                if "WHERE" in query:
                    query += " AND (modelo LIKE ? OR nombre LIKE ? OR especificaciones LIKE ?)"
                else:
                    query += " WHERE (modelo LIKE ? OR nombre LIKE ? OR especificaciones LIKE ?)"
                filtros.extend(["%" + self.busqueda_entry.get() + "%"] * 3)

            cursor = conn.execute(query, filtros)
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=fila)

    def crear_interfaz_compra(self, container):
        detalles_frame = tk.LabelFrame(
            container,
            text="Detalles del Producto",
            font=("Helvetica", 14, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["texto"],
            padx=15,
            pady=15
        )
        detalles_frame.pack(side="top", padx=10, pady=5, fill="x")

        self.detalles_labels = {}
        for campo in ["modelo", "nombre", "precio", "cantidad"]:
            frame = tk.Frame(detalles_frame, bg=COLORES["frame_principal"])
            frame.pack(fill="x", padx=5, pady=8)
            
            tk.Label(
                frame,
                text=f"{CAMPOS[campo]['label']}:",
                font=("Helvetica", 12, "bold"),
                bg=COLORES["frame_principal"],
                fg=COLORES["primario"]
            ).pack(side="left")
            
            label = tk.Label(
                frame,
                text="---",
                font=("Helvetica", 12),
                bg=COLORES["frame_principal"],
                fg=COLORES["texto_suave"],
                width=25,
                anchor="w"
            )
            label.pack(side="left", padx=10)
            self.detalles_labels[campo] = label

        factura_frame = tk.LabelFrame(
            container,
            text="Facturación",
            font=("Helvetica", 14, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["texto"],
            padx=15,
            pady=15
        )
        factura_frame.pack(side="top", padx=10, pady=15, fill="x")

        frame = tk.Frame(factura_frame, bg=COLORES["frame_principal"])
        frame.pack(fill="x", pady=10)
        
        tk.Label(
            frame,
            text="Cantidad a comprar:",
            font=("Helvetica", 12, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["primario"]
        ).pack(side="left")
        
        vcmd = (self.ventana.register(validar_numerico), '%S')
        self.cantidad_compra = ttk.Entry(
            frame, 
            validate="key", 
            validatecommand=vcmd,
            width=15
        )
        self.cantidad_compra.pack(side="left", padx=10)

        self.total_label = tk.Label(
            factura_frame,
            text="Total: $0.00",
            font=("Helvetica", 16, "bold"),
            bg=COLORES["frame_principal"],
            fg=COLORES["acento"]
        )
        self.total_label.pack(pady=15)

        comprar_btn = tk.Button(
            factura_frame,
            text="Realizar Compra",
            font=("Helvetica", 12, "bold"),
            bg=COLORES["primario"],
            fg="white",
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=self.procesar_compra
        )
        comprar_btn.pack(pady=5)
        
        comprar_btn.bind("<Enter>", lambda e: comprar_btn.configure(bg=COLORES["secundario"]))
        comprar_btn.bind("<Leave>", lambda e: comprar_btn.configure(bg=COLORES["primario"]))

    def procesar_compra(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para comprar")
            return

        cantidad = self.cantidad_compra.get()
        if not cantidad:
            messagebox.showwarning("Advertencia", "Ingrese la cantidad a comprar")
            return

        cantidad = int(cantidad)
        item = self.tabla.item(seleccion[0])
        valores = item["values"]
        stock = int(valores[5])
        precio = float(valores[4])

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return

        if cantidad > stock:
            messagebox.showerror("Error", "No hay suficiente stock disponible")
            return

        total = cantidad * precio
        if messagebox.askyesno(
            "Confirmar Compra",
            f"Total a pagar: ${total:.2f}\n¿Desea confirmar la compra?",
        ):
            with conectar_base_datos() as conn:
                conn.execute(
                    "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?",
                    (cantidad, valores[0]),
                )
            messagebox.showinfo("Éxito", "¡Compra realizada con éxito!")
            self.cantidad_compra.delete(0, tk.END)
            self.actualizar_tabla()

            generar_factura_pdf(
                nombre_producto=valores[1],   
                descripcion=valores[2],       
                cantidad=cantidad,
                precio_unitario=precio,
                total=total
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaTienda(root)
    root.mainloop()