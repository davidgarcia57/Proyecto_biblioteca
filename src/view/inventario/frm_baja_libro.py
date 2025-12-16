import customtkinter as ctk
from tkinter import messagebox

class FrmBajaLibro(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.configure(fg_color="#F3E7D2") # Fondo Beige
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.crear_header()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10))
        
        btn_volver = ctk.CTkButton(
            header, 
            text="⬅ VOLVER AL MENÚ", 
            width=220, height=55,
            fg_color="#8D6E63", hover_color="#6D4C41",
            font=("Arial", 18, "bold"), 
            command=self.controller.volver_al_menu
        )
        btn_volver.pack(side="left")
        
        lbl_titulo = ctk.CTkLabel(
            header, 
            text="GESTIÓN DE BAJAS DE LIBROS", 
            font=("Georgia", 32, "bold"), 
            text_color="#5a3b2e"
        )
        lbl_titulo.pack(side="left", padx=40)

    def crear_panel_izquierdo(self):

        p_izq = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        p_izq.grid(row=1, column=0, sticky="nsew", padx=(30, 15), pady=20)
        
        ctk.CTkLabel(p_izq, text="Buscar Ejemplar", font=("Arial", 22, "bold"), text_color="#A7744A").pack(pady=(30, 10))

        self.entry_id = ctk.CTkEntry(
            p_izq, 
            placeholder_text="Escanee o escriba el ID...", 
            height=55, 
            font=("Arial", 20),
            justify="center"
        )
        self.entry_id.pack(fill="x", padx=40, pady=10)
        self.entry_id.bind("<Return>", self.buscar)

        # Botón Buscar
        ctk.CTkButton(
            p_izq, text="🔍 BUSCAR DATOS", height=50,
            fg_color="#A7744A", hover_color="#8c5e3c",
            font=("Arial", 16, "bold"),
            command=self.buscar
        ).pack(fill="x", padx=40, pady=10)

        ctk.CTkFrame(p_izq, height=2, fg_color="#Decdbb").pack(fill="x", padx=40, pady=20)

        self.lbl_info_titulo = ctk.CTkLabel(p_izq, text="Esperando búsqueda...", font=("Arial", 18, "bold"), text_color="gray")
        self.lbl_info_titulo.pack(pady=5)

        self.lbl_info_estado = ctk.CTkLabel(p_izq, text="", font=("Arial", 16))
        self.lbl_info_estado.pack(pady=5)

        self.btn_confirmar = ctk.CTkButton(
            p_izq, 
            text="🗑️ CONFIRMAR BAJA", 
            height=60,
            fg_color="#D32F2F", hover_color="#B71C1C",
            font=("Arial", 20, "bold"),
            state="disabled",
            command=self.confirmar
        )
        self.btn_confirmar.pack(side="bottom", fill="x", padx=40, pady=40)

    def crear_panel_derecho(self):
        p_der = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_color="#Decdbb", border_width=2)
        p_der.grid(row=1, column=1, sticky="nsew", padx=(15, 30), pady=20)
        
        container = ctk.CTkFrame(p_der, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20)

        ctk.CTkLabel(container, text="GUÍA RÁPIDA", font=("Arial", 26, "bold"), text_color="#A7744A").pack(pady=(0, 30))
        
        texto_instrucciones = (
            "PASO 1:\n"
            "Ingrese el ID del ejemplar o escanee\n"
            "el código de barras del libro.\n\n"
            "PASO 2:\n"
            "Verifique que el título y la ubicación\n"
            "coincidan con el libro físico.\n\n"
            "PASO 3:\n"
            "Si todo es correcto, presione el botón\n"
            "rojo para darlo de baja permanentemente."
        )
        
        ctk.CTkLabel(
            container, 
            text=texto_instrucciones, 
            font=("Arial", 20), 
            text_color="#333333",
            justify="center"
        ).pack(anchor="center")

        ctk.CTkLabel(container, text="📚 ❌ 🗑️", font=("Arial", 60)).pack(side="bottom", pady=40)

    def buscar(self, event=None):
        id_libro = self.entry_id.get()
        if not id_libro: return

        info = self.controller.obtener_info_ejemplar(id_libro)
        
        if info:
            # Mostramos datos bonitos
            self.lbl_info_titulo.configure(text=f"📖 {info['titulo']}", text_color="#333333")
            
            estado = info['estado']
            ubicacion = info['ubicacion']
            
            detalle = f"Ubicación: {ubicacion}  |  Estado: {estado}"
            self.lbl_info_estado.configure(text=detalle)
            
            # Lógica de activación de botón
            if estado == 'Disponible':
                self.btn_confirmar.configure(state="normal", text="🗑️ CONFIRMAR BAJA", fg_color="#D32F2F")
            elif estado == 'Prestado':
                self.btn_confirmar.configure(state="disabled", text="⚠️ LIBRO PRESTADO", fg_color="gray")
                self.lbl_info_estado.configure(text=f"{detalle}\n(Debe devolverse antes)", text_color="#D32F2F")
            elif estado == 'Baja':
                self.btn_confirmar.configure(state="disabled", text="⚠️ YA ESTÁ DE BAJA", fg_color="gray")
            else:
                self.btn_confirmar.configure(state="disabled", text=f"ESTADO: {estado}", fg_color="gray")
        else:
            self.lbl_info_titulo.configure(text="❌ Libro no encontrado", text_color="#D32F2F")
            self.lbl_info_estado.configure(text="Verifique el ID e intente de nuevo")
            self.btn_confirmar.configure(state="disabled", text="🗑️ CONFIRMAR BAJA", fg_color="#D32F2F")

    def confirmar(self):
        if messagebox.askyesno("Confirmar Baja", "¿Está TOTALMENTE SEGURO?\nEsta acción retirará el libro del inventario activo."):
            id_libro = self.entry_id.get()
            exito, msg = self.controller.procesar_baja(id_libro)
            
            if exito:
                messagebox.showinfo("Baja Exitosa", msg)
                self.entry_id.delete(0, 'end')
                self.lbl_info_titulo.configure(text="Esperando búsqueda...", text_color="gray")
                self.lbl_info_estado.configure(text="")
                self.btn_confirmar.configure(state="disabled")
            else:
                messagebox.showerror("Error", msg)