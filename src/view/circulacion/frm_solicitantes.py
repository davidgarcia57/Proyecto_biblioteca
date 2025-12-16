import customtkinter as ctk
from tkinter import ttk, messagebox

class FrmSolicitantes(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F3E7D2")
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.crear_header()
        self.crear_panel_gestion(row=1, col=0)
        self.crear_panel_instrucciones(row=1, col=1)

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10))
        
        btn_volver = ctk.CTkButton(
            header, text="⬅ VOLVER AL MENÚ", width=220, height=55,
            fg_color="#8D6E63", hover_color="#6D4C41",
            font=("Arial", 18, "bold"), command=self.controller.volver_menu
        )
        btn_volver.pack(side="left")
        
        ctk.CTkLabel(header, text="DIRECTORIO DE LECTORES", font=("Georgia", 32, "bold"), text_color="#5a3b2e").pack(side="left", padx=40)

    def crear_panel_gestion(self, row, col):
        p_gest = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        p_gest.grid(row=row, column=col, sticky="nsew", padx=(30, 15), pady=20)
        
        # Formulario
        f_form = ctk.CTkFrame(p_gest, fg_color="transparent")
        f_form.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(f_form, text="Nuevo / Editar Lector", font=("Arial", 18, "bold"), text_color="#A7744A").pack(anchor="w", pady=(0, 10))
        
        self.entry_nombre = ctk.CTkEntry(f_form, placeholder_text="Nombre Completo", height=45, font=("Arial", 14))
        self.entry_nombre.pack(fill="x", pady=5)
        
        self.entry_telefono = ctk.CTkEntry(f_form, placeholder_text="Teléfono", height=45, font=("Arial", 14))
        self.entry_telefono.pack(fill="x", pady=5)
        
        self.entry_email = ctk.CTkEntry(f_form, placeholder_text="Correo Electrónico", height=45, font=("Arial", 14))
        self.entry_email.pack(fill="x", pady=5)
        
        self.entry_direccion = ctk.CTkEntry(f_form, placeholder_text="Dirección", height=45, font=("Arial", 14))
        self.entry_direccion.pack(fill="x", pady=5)
        
        # --- BOTONES DE ACCIÓN ---
        f_btns = ctk.CTkFrame(f_form, fg_color="transparent")
        f_btns.pack(fill="x", pady=15)
        
        ctk.CTkButton(f_btns, text="LIMPIAR", width=100, height=40, fg_color="gray", 
                      command=self.limpiar_form).pack(side="left", padx=5)

        self.btn_eliminar = ctk.CTkButton(
            f_btns, 
            text="🗑️ ELIMINAR", 
            width=100, height=40, 
            fg_color="#D32F2F", hover_color="#B71C1C",
            state="disabled", # Desactivado por defecto
            command=self.eliminar_lector
        )
        self.btn_eliminar.pack(side="left", padx=5)

        # Botón Guardar (Verde)
        ctk.CTkButton(f_btns, text="💾 GUARDAR LECTOR", width=200, height=40, fg_color="#2E7D32", 
                      font=("Arial", 14, "bold"), command=self.guardar_lector).pack(side="right", padx=5)

        # Tabla
        f_tabla = ctk.CTkFrame(p_gest, fg_color="transparent")
        f_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        cols = ("id", "nombre", "telefono", "email")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID"); self.tree.column("id", width=40)
        self.tree.heading("nombre", text="Nombre"); self.tree.column("nombre", width=150)
        self.tree.heading("telefono", text="Teléfono"); self.tree.column("telefono", width=100)
        self.tree.heading("email", text="Email"); self.tree.column("email", width=150)
        
        sb = ctk.CTkScrollbar(f_tabla, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self.cargar_para_editar)

    def crear_panel_instrucciones(self, row, col):
        p_inst = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_color="#Decdbb", border_width=2)
        p_inst.grid(row=row, column=col, sticky="nsew", padx=(15, 30), pady=20)
        
        container = ctk.CTkFrame(p_inst, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20)
        
        ctk.CTkLabel(container, text="ADMINISTRACIÓN", font=("Arial", 26, "bold"), text_color="#A7744A").pack(pady=(0, 30))
        
        texto = (
            "REGISTRAR:\n"
            "Llene los campos y presione Guardar.\n\n"
            "EDITAR / ELIMINAR:\n"
            "Haga DOBLE CLIC en un usuario de la lista.\n"
            "El botón 'Eliminar' se activará en rojo.\n\n"
            "IMPORTANTE:\n"
            "No podrá eliminar lectores que tengan\n"
            "libros sin devolver."
        )
        
        ctk.CTkLabel(container, text=texto, font=("Arial", 20), text_color="#333333", justify="center").pack(anchor="center")
        ctk.CTkLabel(container, text="👥", font=("Arial", 100)).pack(side="bottom", pady=40)

    # --- FUNCIONALIDAD ---

    def guardar_lector(self):
        data = {
            "nombre": self.entry_nombre.get(),
            "telefono": self.entry_telefono.get(),
            "email": self.entry_email.get(),
            "direccion": self.entry_direccion.get()
        }
        if hasattr(self, 'id_editar') and self.id_editar:
            data['id'] = self.id_editar
            self.controller.actualizar_solicitante(data)
        else:
            self.controller.agregar_solicitante(data)
        
        self.limpiar_form()

    def eliminar_lector(self):
        # Preguntamos antes de borrar
        if hasattr(self, 'id_editar') and self.id_editar:
            confirmar = messagebox.askyesno("Eliminar Lector", "¿Está seguro que desea eliminar a este lector?\nEsta acción no se puede deshacer.")
            if confirmar:
                self.controller.eliminar_solicitante(self.id_editar)
                self.limpiar_form() # Limpiamos para desactivar el botón

    def cargar_para_editar(self, event):
        item = self.tree.selection()
        if item:
            vals = self.tree.item(item)['values']
            self.id_editar = vals[0]
            
            self.entry_nombre.delete(0, 'end'); self.entry_nombre.insert(0, vals[1])
            self.entry_telefono.delete(0, 'end'); self.entry_telefono.insert(0, str(vals[2]))
            self.entry_email.delete(0, 'end'); self.entry_email.insert(0, vals[3])
            
            # ACTIVAMOS EL BOTÓN DE ELIMINAR
            self.btn_eliminar.configure(state="normal")

    def limpiar_form(self):
        self.id_editar = None
        self.entry_nombre.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        
        # DESACTIVAMOS EL BOTÓN DE ELIMINAR (Por seguridad)
        if hasattr(self, 'btn_eliminar'):
            self.btn_eliminar.configure(state="disabled")

    def actualizar_tabla(self, lista_objetos):
        self.tree.delete(*self.tree.get_children())
        for obj in lista_objetos:
            valores = (obj.id_prestatario, obj.nombre_completo, obj.telefono, obj.email)
            self.tree.insert("", "end", values=valores)