import customtkinter as ctk
from tkinter import messagebox
from datetime import date

class FrmPrestamos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F3E7D2") # Fondo Beige
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.crear_header()

        self.crear_panel_operacion(row=1, col=0)
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
        
        ctk.CTkLabel(header, text="MÓDULO DE PRÉSTAMOS", font=("Georgia", 32, "bold"), text_color="#5a3b2e").pack(side="left", padx=40)

    def crear_panel_operacion(self, row, col):
        p_op = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        p_op.grid(row=row, column=col, sticky="nsew", padx=(30, 15), pady=20)
        
        ctk.CTkLabel(p_op, text="1. Seleccionar Libro", font=("Arial", 20, "bold"), text_color="#A7744A").pack(pady=(20, 10))
        
        f_libro = ctk.CTkFrame(p_op, fg_color="#F9F5EB")
        f_libro.pack(fill="x", padx=20, pady=5)
        
        self.lbl_libro = ctk.CTkLabel(f_libro, text="Ningún libro seleccionado", font=("Arial", 16), text_color="gray")
        self.lbl_libro.pack(side="left", padx=20, pady=15)
        
        btn_bus_libro = ctk.CTkButton(
            f_libro, text="🔍 Buscar Libro", width=120, height=35,
            fg_color="#A7744A", hover_color="#8c5e3c",
            font=("Arial", 14, "bold"), 
            command=self.controller.abrir_busqueda_libros 
        )
        btn_bus_libro.pack(side="right", padx=10, pady=10)

        # Sección 2: Buscar Usuario
        ctk.CTkLabel(p_op, text="2. Seleccionar Lector", font=("Arial", 20, "bold"), text_color="#A7744A").pack(pady=(30, 10))
        
        f_user = ctk.CTkFrame(p_op, fg_color="#F9F5EB")
        f_user.pack(fill="x", padx=20, pady=5)
        
        self.lbl_usuario = ctk.CTkLabel(f_user, text="Ningún lector seleccionado", font=("Arial", 16), text_color="gray")
        self.lbl_usuario.pack(side="left", padx=20, pady=15)
        
        btn_bus_lec = ctk.CTkButton(
            f_user, text="🔍 Buscar Lector", width=120, height=35,
            fg_color="#A7744A", hover_color="#8c5e3c",
            font=("Arial", 14, "bold"), 
            command=self.controller.abrir_busqueda_lectores 
        )
        btn_bus_lec.pack(side="right", padx=10, pady=10)

        # Sección 3: Confirmar
        ctk.CTkFrame(p_op, height=2, fg_color="#Decdbb").pack(fill="x", padx=40, pady=40)
        
        ctk.CTkButton(p_op, text="✅ CONFIRMAR PRÉSTAMO", width=300, height=60,
                      fg_color="#2E7D32", hover_color="#1B5E20",
                      font=("Arial", 20, "bold"), command=self.controller.realizar_prestamo).pack(pady=10)

    def crear_panel_instrucciones(self, row, col):
        p_inst = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_color="#Decdbb", border_width=2)
        p_inst.grid(row=row, column=col, sticky="nsew", padx=(15, 30), pady=20)
        
        container = ctk.CTkFrame(p_inst, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20)
        
        ctk.CTkLabel(container, text="GUÍA RÁPIDA", font=("Arial", 26, "bold"), text_color="#A7744A").pack(pady=(0, 30))
        
        texto = (
            "PASO 1:\n"
            "Presione 'Buscar Libro' para abrir el catálogo.\n"
            "Haga doble clic sobre el libro deseado.\n\n"
            "PASO 2:\n"
            "Presione 'Buscar Lector' para ver la lista.\n"
            "Seleccione a la persona que se lleva el libro.\n\n"
            "PASO 3:\n"
            "Verifique que los datos sean correctos y\n"
            "presione el botón verde de Confirmar."
        )
        
        ctk.CTkLabel(container, text=texto, font=("Arial", 20), text_color="#333333", justify="center").pack(anchor="center")
        ctk.CTkLabel(container, text="📖 ➡️ 👤", font=("Arial", 60)).pack(side="bottom", pady=40)

    # Métodos de actualización de interfaz (llamados por el controller)
    def actualizar_libro(self, titulo):
        self.lbl_libro.configure(text=f"📖 {titulo}", text_color="#333333", font=("Arial", 16, "bold"))

    def actualizar_usuario(self, nombre):
        self.lbl_usuario.configure(text=f"👤 {nombre}", text_color="#333333", font=("Arial", 16, "bold"))