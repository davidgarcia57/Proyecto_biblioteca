import customtkinter as ctk
from tkinter import ttk, messagebox
import os
from PIL import Image # Requiere: pip install pillow

class FrmSolicitantes(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Configuración principal
        self.configure(fg_color="#F3E7D2") # Fondo Beige
        self.grid_columnconfigure(0, weight=0) # Panel Izquierdo (Fijo/Ancho contenido)
        self.grid_columnconfigure(1, weight=1) # Panel Derecho (Se expande con la tabla)
        self.grid_rowconfigure(1, weight=1)

        self.id_actual = None # Control de estado (Edición vs Nuevo)

        # --- HEADER ---
        self.crear_header()

        # --- PANEL IZQUIERDO: FORMULARIO ---
        self.crear_panel_formulario()

        # --- PANEL DERECHO: TABLA ---
        self.crear_panel_tabla()

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 10))
        
        ctk.CTkButton(
            header, text="⬅ Volver", width=90, height=35,
            fg_color="#A7744A", hover_color="#8c5e3a",
            font=("Arial", 13, "bold"),
            command=self.controller.volver_menu
        ).pack(side="left")
        
        ctk.CTkLabel(
            header, text="Gestión de Solicitantes", 
            font=("Georgia", 26, "bold"), text_color="#5a3b2e"
        ).pack(side="left", padx=20)

    def crear_panel_formulario(self):
        # Contenedor del formulario
        self.p_form = ctk.CTkFrame(self, width=320, fg_color="white", corner_radius=20, border_width=1, border_color="#Decdbb")
        self.p_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.p_form.grid_propagate(False) # Mantener ancho fijo si se desea, o quitar para auto-ajuste

        # --- IMAGEN / LOGO (Opcional) ---
        # Bloque try/except para evitar el espacio en blanco si falla
        frame_img = ctk.CTkFrame(self.p_form, fg_color="transparent")
        frame_img.pack(pady=(20, 10))
        
        try:
            # Puedes usar "logo_biblioteca.png" o una imagen de "usuario_default.png"
            image_path = "logo_biblioteca.png" 
            
            if os.path.exists(image_path):
                img_pil = Image.open(image_path)
                img_ctk = ctk.CTkImage(light_image=img_pil, size=(100, 100)) # Tamaño más pequeño para este panel
                
                lbl_img = ctk.CTkLabel(frame_img, image=img_ctk, text="")
                lbl_img.pack()
            # Si no existe, no hacemos nada y el pack no ocupa espacio
        except Exception:
            pass

        ctk.CTkLabel(self.p_form, text="Datos Personales", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=(0, 15))

        # Inputs
        self.entry_nombre = self.crear_input("Nombre Completo *")
        self.entry_telefono = self.crear_input("Teléfono")
        self.entry_email = self.crear_input("Correo Electrónico")
        self.entry_direccion = self.crear_input("Dirección")

        # Separador
        ctk.CTkFrame(self.p_form, height=2, fg_color="#E0E0E0").pack(fill="x", padx=30, pady=15)

        # Botones
        self.btn_guardar = ctk.CTkButton(self.p_form, text="Guardar Registro", fg_color="#2E7D32", hover_color="#1e5222", 
                                         height=40, font=("Arial", 13, "bold"), command=self.evento_guardar)
        self.btn_guardar.pack(pady=5, padx=20, fill="x")
        
        self.btn_limpiar = ctk.CTkButton(self.p_form, text="Limpiar / Nuevo", fg_color="gray", hover_color="#555", 
                                         height=35, command=self.limpiar_form)
        self.btn_limpiar.pack(pady=5, padx=20, fill="x")

        self.btn_eliminar = ctk.CTkButton(self.p_form, text="Eliminar Seleccionado", fg_color="#D32F2F", hover_color="#9a2222", 
                                          height=35, command=self.evento_eliminar)
        self.btn_eliminar.pack(pady=(20, 5), padx=20, fill="x")

        self.btn_imprimir = ctk.CTkButton(self.p_form, text="🖨️ Imprimir Lista PDF", fg_color="#5a3b2e", hover_color="#3e281f",
                                          height=35, command=self.imprimir_pdf)
        self.btn_imprimir.pack(pady=5, padx=20, fill="x")

    def crear_panel_tabla(self):
        p_tabla = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=1, border_color="#Decdbb")
        p_tabla.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        # Título tabla
        ctk.CTkLabel(p_tabla, text="Directorio de Solicitantes", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)

        # Contenedor para Treeview y Scrollbar
        frame_tree = ctk.CTkFrame(p_tabla, fg_color="transparent")
        frame_tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Estilos para la tabla (Treeview es nativo de tk, no ctk)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="white", 
                        foreground="black", 
                        fieldbackground="white", 
                        rowheight=30, 
                        font=("Arial", 11))
        style.configure("Treeview.Heading", 
                        font=("Arial", 11, "bold"), 
                        background="#E8D6C0", 
                        foreground="#5a3b2e")
        style.map("Treeview", background=[("selected", "#A7744A")])

        # Definición de columnas
        self.tree = ttk.Treeview(frame_tree, columns=("ID", "Nombre", "Tel", "Email"), show="headings", selectmode="browse")
        
        # Scrollbar vertical
        scrollbar = ctk.CTkScrollbar(frame_tree, orientation="vertical", command=self.tree.yview, fg_color="transparent")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Configurar cabeceras
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre Completo")
        self.tree.heading("Tel", text="Teléfono")
        self.tree.heading("Email", text="Correo Electrónico")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.column("Tel", width=100, anchor="center")
        self.tree.column("Email", width=180, anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def crear_input(self, placeholder):
        # Label pequeño arriba del entry
        ctk.CTkLabel(self.p_form, text=placeholder, anchor="w", font=("Arial", 11, "bold"), text_color="gray").pack(fill="x", padx=25, pady=(8,0))
        
        entry = ctk.CTkEntry(self.p_form, placeholder_text=placeholder, height=35, border_color="#A7744A")
        entry.pack(fill="x", padx=20, pady=(2,0))
        return entry

    # --- LÓGICA (Igual que antes) ---

    def limpiar_form(self):
        self.id_actual = None
        self.entry_nombre.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        self.btn_guardar.configure(text="Guardar Registro", fg_color="#2E7D32")
        self.tree.selection_remove(self.tree.selection()) # Deseleccionar tabla
        self.entry_nombre.focus()

    def evento_guardar(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "telefono": self.entry_telefono.get(),
            "email": self.entry_email.get(),
            "direccion": self.entry_direccion.get()
        }
        if not datos["nombre"]:
            messagebox.showwarning("Faltan datos", "El nombre es obligatorio")
            return

        self.controller.guardar_solicitante(datos, self.id_actual)
        self.limpiar_form() # Limpiar después de guardar

    def evento_eliminar(self):
        if self.id_actual:
            if messagebox.askyesno("Confirmar", f"¿Eliminar al solicitante ID {self.id_actual}?"):
                self.controller.eliminar_solicitante(self.id_actual)
                self.limpiar_form()
        else:
            messagebox.showwarning("Aviso", "Seleccione un solicitante de la lista para eliminar.")

    def seleccionar_fila(self, event):
        item = self.tree.selection()
        if item:
            vals = self.tree.item(item, "values")
            self.limpiar_form() # Limpia primero para borrar basura
            
            # Recuperar datos
            self.id_actual = vals[0]
            self.entry_nombre.insert(0, vals[1])
            self.entry_telefono.insert(0, vals[2])
            self.entry_email.insert(0, vals[3])
            
            # Nota: Si necesitas la dirección y no está en la tabla, deberás pedirla al controller
            # self.entry_direccion.insert(0, "...") 

            self.btn_guardar.configure(text="Actualizar Datos", fg_color="#A7744A") # Cambia color botón

    def imprimir_pdf(self):
        from src.controller.reportes_controller import ReportesController
        ReportesController().generar_reporte_solicitantes()