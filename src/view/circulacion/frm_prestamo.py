import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

class FrmPrestamos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2")

        # 1. Configuración del Grid Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # 2. Header (Fila 0)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        self.btn_volver = ctk.CTkButton(self.header, text="⬅ Volver", width=80, fg_color="#A7744A", command=self.controller.volver_menu)
        self.btn_volver.pack(side="left")
        
        ctk.CTkLabel(self.header, text="Gestión de Préstamos", font=("Georgia", 24, "bold"), text_color="#5a3b2e").pack(side="left", padx=20)

        # 3. Formulario (Fila 1, Col 0) - ¡CREAR ESTO PRIMERO!
        self.frm_form = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.frm_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(self.frm_form, text="Nuevo Préstamo", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)

        # --- AHORA SÍ AGREGAMOS LOS WIDGETS ---
        
        # ID LIBRO
        ctk.CTkLabel(self.frm_form, text="ID Ejemplar (Libro):").pack(pady=(10,0), padx=20, anchor="w")
        
        # Frame para input y botón de búsqueda
        frm_input_libro = ctk.CTkFrame(self.frm_form, fg_color="transparent")
        frm_input_libro.pack(fill="x", padx=20, pady=5)
        
        self.txt_id_libro = ctk.CTkEntry(frm_input_libro, placeholder_text="Escanea código o escribe ID")
        self.txt_id_libro.pack(side="left", fill="x", expand=True)
        self.txt_id_libro.bind("<Return>", lambda e: self.buscar_libro())
        
        self.btn_buscar_libro = ctk.CTkButton(
            frm_input_libro, 
            text="🔍", 
            width=40, 
            command=self.controller.abrir_popup_libros 
        )
        self.btn_buscar_libro.pack(side="left", padx=(5,0))

        self.lbl_info_libro = ctk.CTkLabel(self.frm_form, text="[Esperando libro...]", text_color="gray", wraplength=250)
        self.lbl_info_libro.pack(pady=5)

        # ID PRESTATARIO
        ctk.CTkLabel(self.frm_form, text="ID Solicitante:").pack(pady=(15,0), padx=20, anchor="w")
        self.txt_id_usuario = ctk.CTkEntry(self.frm_form, placeholder_text="ID del lector")
        self.txt_id_usuario.pack(fill="x", padx=20, pady=5)
        self.txt_id_usuario.bind("<Return>", lambda e: self.buscar_solicitante())

        self.lbl_info_usuario = ctk.CTkLabel(self.frm_form, text="[Esperando solicitante...]", text_color="gray")
        self.lbl_info_usuario.pack(pady=5)

        # DÍAS DE PRÉSTAMO
        ctk.CTkLabel(self.frm_form, text="Días de préstamo:").pack(pady=(15,0), padx=20, anchor="w")
        self.combo_dias = ctk.CTkComboBox(self.frm_form, values=["3", "5", "7", "15"], state="readonly")
        self.combo_dias.set("3")
        self.combo_dias.pack(fill="x", padx=20, pady=5)

        # BOTÓN ACCIÓN
        self.btn_prestar = ctk.CTkButton(self.frm_form, text="REALIZAR PRÉSTAMO", fg_color="#2E7D32", height=40, font=("Arial", 14, "bold"), command=self.evento_prestar)
        self.btn_prestar.pack(pady=30, padx=20, fill="x")

        # 4. Panel Derecho (Fila 1, Col 1)
        self.frm_lista = ctk.CTkFrame(self, fg_color="white")
        self.frm_lista.grid(row=1, column=1, sticky="nsew", padx=(0,20), pady=20)
        
        ctk.CTkLabel(self.frm_lista, text="Instrucciones:", font=("Arial", 14, "bold")).pack(pady=20)
        msg = ("1. Ingrese el ID del Ejemplar y presione ENTER para verificar disponibilidad.\n\n"
               "2. Ingrese el ID del Solicitante y presione ENTER para verificar registro.\n\n"
               "3. Seleccione los días y haga clic en Realizar Préstamo.")
        ctk.CTkLabel(self.frm_lista, text=msg, justify="left", wraplength=400).pack(padx=20)

    # --- MÉTODOS DE LA CLASE ---
    def buscar_libro(self):
        id_libro = self.txt_id_libro.get()
        if id_libro:
            self.controller.verificar_libro(id_libro)

    def buscar_solicitante(self):
        id_sol = self.txt_id_usuario.get()
        if id_sol:
            self.controller.verificar_solicitante(id_sol)

    def evento_prestar(self):
        self.controller.registrar_prestamo(
            self.txt_id_libro.get(),
            self.txt_id_usuario.get(),
            self.combo_dias.get()
        )
        
    def mostrar_mensaje(self, msg, error=False):
        # Usamos messagebox para feedback claro
        if error:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Información", msg)
        
    def actualizar_info_libro(self, texto, disponible=True):
        self.lbl_info_libro.configure(text=texto, text_color="green" if disponible else "red")
        
    def actualizar_info_usuario(self, texto, valido=True):
        self.lbl_info_usuario.configure(text=texto, text_color="green" if valido else "red")

    #Préstamos Activos e Inactivos
    

