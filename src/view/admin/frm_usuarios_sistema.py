import customtkinter as ctk
from tkinter import ttk, messagebox

class FrmUsuariosSistema(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        #COnfig Principal
        self.configure(fg_color="#F3E7D2") # Beige de fondo
        
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(1, weight=1)

        self.id_actual = None 

        self.crear_header()

        # PANEL IZQUIERDO: FORMULARIO
        self.crear_panel_formulario()

        # PANEL DERECHO: TABLA
        self.crear_panel_tabla()

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 10))
        
        ctk.CTkButton(
            header, 
            text="⬅ Volver", 
            width=140, 
            height=50,
            fg_color="#A7744A", 
            hover_color="#8c5e3a", 
            font=("Arial", 16, "bold"),
            command=self.controller.volver_menu
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, 
            text="Configuración de Usuarios", 
            font=("Arial", 28, "bold"),
            text_color="#5a3b2e"
        ).pack(side="left", padx=20)

    def crear_panel_formulario(self):
        self.p_form = ctk.CTkScrollableFrame(
            self, 
            width=380,
            fg_color="white", 
            corner_radius=20, 
            border_width=2, 
            border_color="#Decdbb",
            label_text="Datos de Cuenta",
            label_font=("Arial", 18, "bold"),
            label_text_color="#A7744A"
        )
        self.p_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        self.entry_nombre = self.crear_input("Nombre Real (Personal)", pady_top=15) 
        self.entry_user = self.crear_input("Usuario (Login)")
        
        # Separador visual
        ctk.CTkFrame(self.p_form, height=2, fg_color="#E0E0E0").pack(fill="x", padx=30, pady=15)

        self.entry_pass = self.crear_input("Nueva Contraseña", is_pass=True)
        self.entry_pass_conf = self.crear_input("Confirmar Contraseña", is_pass=True)
        
        ctk.CTkLabel(self.p_form, text="Rol y Permisos:", font=("Arial", 14, "bold"), text_color="gray", anchor="w").pack(fill="x", padx=25, pady=(15,5))
        
        self.combo_rol = ctk.CTkComboBox(
            self.p_form, 
            values=["Bibliotecario", "Administrador"], 
            height=45,
            font=("Arial", 16),
            dropdown_font=("Arial", 16),
            border_color="#A7744A",
            border_width=2
        )
        self.combo_rol.pack(fill="x", padx=20, pady=5)
        
        # Cuenta activa
        self.chk_activo = ctk.CTkSwitch(
            self.p_form, 
            text="Cuenta Activa", 
            font=("Arial", 16, "bold"),
            progress_color="#2E7D32",
            switch_height=20,
            switch_width=40
        )
        self.chk_activo.pack(pady=20)
        self.chk_activo.select()

        # BOTONES DE ACCIÓN
        self.btn_guardar = ctk.CTkButton(
            self.p_form, 
            text="💾 Guardar Usuario", 
            fg_color="#2E7D32", 
            hover_color="#1e5222", 
            height=50,
            font=("Arial", 16, "bold"), 
            command=self.evento_guardar
        )
        self.btn_guardar.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            self.p_form, 
            text="Limpiar / Nuevo", 
            fg_color="gray", 
            hover_color="#555", 
            height=45, 
            font=("Arial", 14, "bold"),
            command=self.limpiar_formulario
        ).pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(
            self.p_form, 
            text="🗑️ Eliminar Usuario", 
            fg_color="#D32F2F", 
            hover_color="#9a2222", 
            height=45, 
            font=("Arial", 14, "bold"),
            command=self.evento_eliminar
        ).pack(pady=(20, 20), padx=20, fill="x")

    def crear_panel_tabla(self):
        p_tabla = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=2, border_color="#Decdbb")
        p_tabla.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(
            p_tabla, 
            text="Lista de Usuarios Registrados", 
            font=("Arial", 20, "bold"), 
            text_color="#A7744A"
        ).pack(pady=15)

        frame_tree = ctk.CTkFrame(p_tabla, fg_color="transparent")
        frame_tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        background="white", 
                        foreground="black",
                        rowheight=40,
                        font=("Arial", 14))
                        
        style.configure("Treeview.Heading", 
                        font=("Arial", 16, "bold"), 
                        background="#E8D6C0", 
                        foreground="#5a3b2e")
                        
        style.map("Treeview", background=[("selected", "#A7744A")])

        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nombre", "Usuario", "Rol", "Estado"), show="headings", selectmode="browse")
        
        scrollbar = ctk.CTkScrollbar(frame_tree, orientation="vertical", command=self.tree.yview, width=22)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200)
        self.tree.column("Usuario", width=120)
        self.tree.column("Rol", width=120)
        self.tree.column("Estado", width=100, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def crear_input(self, ph, is_pass=False, pady_top=10):
        ctk.CTkLabel(
            self.p_form, 
            text=ph, 
            anchor="w", 
            font=("Arial", 14, "bold"), 
            text_color="gray"
        ).pack(fill="x", padx=25, pady=(pady_top,0))
        
        show_char = "*" if is_pass else ""
        e = ctk.CTkEntry(
            self.p_form, 
            placeholder_text=ph, 
            show=show_char, 
            height=45,
            font=("Arial", 16),
            border_color="#A7744A",
            border_width=2
        )
        e.pack(fill="x", padx=20, pady=5)
        return e

    # Interaccion

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
        self.btn_guardar.configure(text="💾 Guardar Usuario", fg_color="#2E7D32")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def evento_guardar(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "usuario": self.entry_user.get(),
            "password": self.entry_pass.get(),
            "confirm_pass": self.entry_pass_conf.get(), 
            "rol": self.combo_rol.get(),
            "activo": 1 if self.chk_activo.get() == 1 else 0
        }
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

            self.btn_guardar.configure(text="🔄 Actualizar Usuario", fg_color="#A7744A")