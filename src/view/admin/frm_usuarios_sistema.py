import customtkinter as ctk
from tkinter import ttk, messagebox
import os
from PIL import Image # Requiere: pip install pillow

class FrmUsuariosSistema(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # --- Configuración Principal ---
        self.configure(fg_color="#F3E7D2") # Beige
        self.grid_columnconfigure(0, weight=0) # Panel Formulario (Fijo)
        self.grid_columnconfigure(1, weight=1) # Panel Tabla (Expansible)
        self.grid_rowconfigure(1, weight=1)

        self.id_actual = None # Para controlar si editamos o creamos

        # --- HEADER ---
        self.crear_header()

        # --- PANEL IZQUIERDO: FORMULARIO ---
        self.crear_panel_formulario()

        # --- PANEL DERECHO: TABLA ---
        self.crear_panel_tabla()

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 10))
        
        ctk.CTkButton(header, text="⬅ Volver", width=90, height=35,
                      fg_color="#A7744A", hover_color="#8c5e3a", font=("Arial", 13, "bold"),
                      command=self.controller.volver_menu).pack(side="left")
        
        ctk.CTkLabel(header, text="Configuración de Usuarios", font=("Georgia", 26, "bold"), 
                     text_color="#5a3b2e").pack(side="left", padx=20)

    def crear_panel_formulario(self):
        # Contenedor del formulario
        self.p_form = ctk.CTkFrame(self, width=320, fg_color="white", corner_radius=20, border_width=1, border_color="#Decdbb")
        self.p_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.p_form.grid_propagate(False) 

        # --- AVATAR / LOGO ---
        frame_img = ctk.CTkFrame(self.p_form, fg_color="transparent")
        frame_img.pack(pady=(20, 10))

        try:
            image_path = "user_icon.png" 
            if os.path.exists(image_path):
                img_pil = Image.open(image_path)
                img_ctk = ctk.CTkImage(light_image=img_pil, size=(90, 90))
                ctk.CTkLabel(frame_img, image=img_ctk, text="").pack()
        except Exception:
            pass

        ctk.CTkLabel(self.p_form, text="Datos de Cuenta", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=(0, 10))

        # --- INPUTS ---
        self.entry_nombre = self.crear_input("Nombre Real (Personal)")
        self.entry_user = self.crear_input("Usuario (Login)")
        
        # Separador visual para contraseñas
        ctk.CTkFrame(self.p_form, height=1, fg_color="#E0E0E0").pack(fill="x", padx=30, pady=10)

        # Contraseñas con asteriscos (is_pass=True)
        self.entry_pass = self.crear_input("Nueva Contraseña", is_pass=True)
        self.entry_pass_conf = self.crear_input("Confirmar Contraseña", is_pass=True)
        
        # Rol y Estado
        ctk.CTkLabel(self.p_form, text="Rol y Permisos:", font=("Arial", 12, "bold"), text_color="gray", anchor="w").pack(fill="x", padx=25, pady=(10,0))
        self.combo_rol = ctk.CTkComboBox(self.p_form, values=["Bibliotecario", "Administrador"], height=35)
        self.combo_rol.pack(fill="x", padx=20, pady=5)
        
        self.chk_activo = ctk.CTkSwitch(self.p_form, text="Cuenta Activa", progress_color="#2E7D32")
        self.chk_activo.pack(pady=15)
        self.chk_activo.select()

        # --- BOTONES ---
        self.btn_guardar = ctk.CTkButton(self.p_form, text="Guardar Usuario", fg_color="#2E7D32", hover_color="#1e5222", 
                                         height=40, font=("Arial", 13, "bold"), command=self.evento_guardar)
        self.btn_guardar.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(self.p_form, text="Limpiar / Nuevo", fg_color="gray", hover_color="#555", 
                      height=30, command=self.limpiar_formulario).pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(self.p_form, text="Eliminar Usuario", fg_color="#D32F2F", hover_color="#9a2222", 
                      height=30, command=self.evento_eliminar).pack(pady=(15, 20), padx=20, fill="x")

    def crear_panel_tabla(self):
        p_tabla = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=1, border_color="#Decdbb")
        p_tabla.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(p_tabla, text="Lista de Usuarios Registrados", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)

        # Contenedor Tabla + Scrollbar
        frame_tree = ctk.CTkFrame(p_tabla, fg_color="transparent")
        frame_tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Estilos Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", rowheight=30, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#E8D6C0", foreground="#5a3b2e")
        style.map("Treeview", background=[("selected", "#A7744A")])

        # Tabla
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nombre", "Usuario", "Rol", "Estado"), show="headings", selectmode="browse")
        
        scrollbar = ctk.CTkScrollbar(frame_tree, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Cabeceras
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Usuario", text="Usuario (Login)")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=150)
        self.tree.column("Usuario", width=100)
        self.tree.column("Rol", width=100)
        self.tree.column("Estado", width=80, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def crear_input(self, ph, is_pass=False):
        ctk.CTkLabel(self.p_form, text=ph, anchor="w", font=("Arial", 11, "bold"), text_color="gray").pack(fill="x", padx=25, pady=(5,0))
        show_char = "*" if is_pass else ""
        e = ctk.CTkEntry(self.p_form, placeholder_text=ph, show=show_char, height=35, border_color="#A7744A")
        e.pack(fill="x", padx=20, pady=2)
        return e

    # --- LÓGICA / INTERACCIÓN ---

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def agregar_fila(self, *values):
        self.tree.insert("", "end", values=values)

    def limpiar_formulario(self):
        self.id_actual = None
        self.entry_nombre.delete(0, 'end')
        self.entry_user.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.entry_pass_conf.delete(0, 'end') 
        self.combo_rol.set("Bibliotecario")
        self.chk_activo.select()
        self.btn_guardar.configure(text="Guardar Usuario")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def evento_guardar(self):
        # Recolección de datos pura, sin validación de negocio
        datos = {
            "nombre": self.entry_nombre.get(),
            "usuario": self.entry_user.get(),
            "password": self.entry_pass.get(),
            "confirm_pass": self.entry_pass_conf.get(), # Enviamos confirmación al controlador
            "rol": self.combo_rol.get(),
            "activo": 1 if self.chk_activo.get() == 1 else 0
        }
        # Delegamos toda la responsabilidad al controlador
        self.controller.guardar_usuario(datos, self.id_actual)

    def evento_eliminar(self):
        if not self.id_actual:
            messagebox.showwarning("Aviso", "Seleccione un usuario de la tabla para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar Eliminación", "⚠️ ¿Seguro que desea eliminar este usuario?"):
            self.controller.eliminar_usuario(self.id_actual)

    def seleccionar_fila(self, event):
        item = self.tree.selection()
        if item:
            vals = self.tree.item(item, "values")
            self.limpiar_formulario()
            self.id_actual = vals[0]
            
            self.entry_nombre.insert(0, vals[1])
            self.entry_user.insert(0, vals[2])
            self.combo_rol.set(vals[3])
            
            estado = str(vals[4])
            if estado == "Activo" or estado == "1": 
                self.chk_activo.select()
            else: 
                self.chk_activo.deselect()

            self.btn_guardar.configure(text="Actualizar Usuario")