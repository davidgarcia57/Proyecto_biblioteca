import customtkinter as ctk
from tkinter import ttk, messagebox

class FrmUsuariosSistema(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2") # Beige
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(header, text="⬅ Volver", width=80, fg_color="#A7744A", 
                      command=self.controller.volver_menu).pack(side="left")
        
        ctk.CTkLabel(header, text="Configuración del Sistema", font=("Georgia", 24, "bold"), 
                     text_color="#5a3b2e").pack(side="left", padx=20)

        # --- PANEL IZQUIERDO (Formulario) ---
        self.frm_form = ctk.CTkFrame(self, width=320, fg_color="white", corner_radius=10)
        self.frm_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frm_form.pack_propagate(False) # Evita que se encoja

        ctk.CTkLabel(self.frm_form, text="Gestión de Usuarios", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)
        
        self.id_actual = None
        
        self.entry_nombre = self.crear_input("Nombre Real")
        self.entry_user = self.crear_input("Usuario (Login)")
        self.entry_pass = self.crear_input("Contraseña (Dejar vacío si no cambia)")
        
        ctk.CTkLabel(self.frm_form, text="Rol Asignado:", anchor="w").pack(fill="x", padx=20, pady=(10,0))
        self.combo_rol = ctk.CTkComboBox(self.frm_form, values=["Bibliotecario", "Admin"])
        self.combo_rol.pack(fill="x", padx=20, pady=5)
        
        self.chk_activo = ctk.CTkCheckBox(self.frm_form, text="Cuenta Activa")
        self.chk_activo.pack(pady=15)
        self.chk_activo.select()

        # Botones de Acción
        ctk.CTkButton(self.frm_form, text="Guardar / Actualizar", fg_color="#2E7D32", height=40,
                      command=self.evento_guardar).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(self.frm_form, text="Limpiar Formulario", fg_color="gray", 
                      command=self.limpiar_formulario).pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(self.frm_form, text="Eliminar Usuario", fg_color="#D32F2F", hover_color="#B71C1C",
                      command=self.evento_eliminar).pack(pady=20, padx=20, fill="x")

        # --- PANEL DERECHO (Tabla) ---
        self.frm_tabla = ctk.CTkFrame(self, fg_color="white")
        self.frm_tabla.grid(row=1, column=1, sticky="nsew", padx=(0,20), pady=20)
        
        self.tree = ttk.Treeview(self.frm_tabla, columns=("ID", "Nombre", "Usuario", "Rol", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=150)
        self.tree.column("Usuario", width=100)
        self.tree.column("Rol", width=100)
        self.tree.column("Estado", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def crear_input(self, ph):
        ctk.CTkLabel(self.frm_form, text=ph, anchor="w").pack(fill="x", padx=20, pady=(5,0))
        e = ctk.CTkEntry(self.frm_form, placeholder_text=ph)
        e.pack(fill="x", padx=20, pady=2)
        return e

    def limpiar_tabla(self):
        for i in self.tree.get_children(): self.tree.delete(i)

    def agregar_fila(self, *args):
        self.tree.insert("", "end", values=args)

    def limpiar_formulario(self):
        self.id_actual = None
        self.entry_nombre.delete(0, 'end')
        self.entry_user.delete(0, 'end')
        self.entry_pass.delete(0, 'end')
        self.combo_rol.set("Bibliotecario")
        self.chk_activo.select()

    def evento_guardar(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "usuario": self.entry_user.get(),
            "password": self.entry_pass.get(),
            "rol": self.combo_rol.get(),
            "activo": self.chk_activo.get()
        }
        self.controller.guardar_usuario(datos, self.id_actual)

    def evento_eliminar(self):
        if not self.id_actual:
            messagebox.showwarning("Aviso", "Seleccione un usuario de la tabla para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este usuario permanentemente?"):
            # OJO: Este método lo agregaremos al controlador en el siguiente paso
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
            
            # Ajustar checkbox
            if vals[4] == "Activo": 
                self.chk_activo.select()
            else: 
                self.chk_activo.deselect()