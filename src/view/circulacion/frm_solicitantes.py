import customtkinter as ctk
from tkinter import ttk, messagebox

class FrmSolicitantes(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F3E7D2")
        self.grid_columnconfigure(1, weight=1) # Panel derecho se expande
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(self.header, text="⬅ Volver", width=80, fg_color="#A7744A", command=self.controller.volver_menu).pack(side="left")
        ctk.CTkLabel(self.header, text="Gestión de Solicitantes", font=("Georgia", 24, "bold"), text_color="#5a3b2e").pack(side="left", padx=20)

        # --- PANEL IZQUIERDO (Formulario) ---
        self.frm_form = ctk.CTkFrame(self, width=300, fg_color="white", corner_radius=10)
        self.frm_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frm_form.pack_propagate(False) # Forzar ancho fijo

        ctk.CTkLabel(self.frm_form, text="Datos del Solicitante", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)

        self.id_actual = None # Para saber si estamos editando

        self.entry_nombre = self.crear_input("Nombre Completo *")
        self.entry_telefono = self.crear_input("Teléfono")
        self.entry_email = self.crear_input("Correo Electrónico")
        self.entry_direccion = self.crear_input("Dirección")

        # Botones de Acción
        self.btn_guardar = ctk.CTkButton(self.frm_form, text="Guardar", fg_color="#2E7D32", command=self.evento_guardar)
        self.btn_guardar.pack(pady=10, padx=20, fill="x")
        
        self.btn_limpiar = ctk.CTkButton(self.frm_form, text="Nuevo / Limpiar", fg_color="gray", command=self.limpiar_form)
        self.btn_limpiar.pack(pady=5, padx=20, fill="x")

        self.btn_eliminar = ctk.CTkButton(self.frm_form, text="Eliminar Seleccionado", fg_color="#D32F2F", command=self.evento_eliminar)
        self.btn_eliminar.pack(pady=20, padx=20, fill="x")

        self.btn_imprimir = ctk.CTkButton(self.frm_form, text="🖨️ Imprimir PDF",fg_color="#5a3b2e", command=self.imprimir_pdf)
        self.btn_imprimir.pack(pady=20, padx=20, fill="x")

        # --- PANEL DERECHO (Tabla) ---
        self.frm_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_tabla.grid(row=1, column=1, sticky="nsew", padx=(0,20), pady=20)

        # Configurar Treeview (Tabla)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        self.tree = ttk.Treeview(self.frm_tabla, columns=("ID", "Nombre", "Tel", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre Completo")
        self.tree.heading("Tel", text="Teléfono")
        self.tree.heading("Email", text="Email")
        
        self.tree.column("ID", width=40)
        self.tree.column("Nombre", width=200)
        self.tree.column("Tel", width=100)
        self.tree.column("Email", width=150)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def crear_input(self, placeholder):
        ctk.CTkLabel(self.frm_form, text=placeholder, anchor="w").pack(fill="x", padx=20, pady=(10,0))
        entry = ctk.CTkEntry(self.frm_form, placeholder_text=placeholder)
        entry.pack(fill="x", padx=20, pady=(2,0))
        return entry

    def limpiar_form(self):
        self.id_actual = None
        self.entry_nombre.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        self.btn_guardar.configure(text="Guardar Nuevo")

    def evento_guardar(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "telefono": self.entry_telefono.get(),
            "email": self.entry_email.get(),
            "direccion": self.entry_direccion.get()
        }
        self.controller.guardar_solicitante(datos, self.id_actual)

    def evento_eliminar(self):
        if self.id_actual:
            if messagebox.askyesno("Confirmar", "¿Eliminar a este solicitante?"):
                self.controller.eliminar_solicitante(self.id_actual)
        else:
            messagebox.showwarning("Aviso", "Seleccione un solicitante de la lista")

    def seleccionar_fila(self, event):
        item = self.tree.selection()
        if item:
            vals = self.tree.item(item, "values")
            self.limpiar_form()
            self.id_actual = vals[0]
            self.entry_nombre.insert(0, vals[1])
            self.entry_telefono.insert(0, vals[2])
            self.entry_email.insert(0, vals[3])
            # La dirección no está en las columnas visibles, pero el controller podría traerla completa si quisieras
            self.btn_guardar.configure(text="Actualizar Datos")
    
    def imprimir_pdf(self):
        from src.controller.reportes_controller import ReportesController
        ReportesController().generar_reporte_solicitantes()