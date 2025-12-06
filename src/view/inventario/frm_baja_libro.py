import customtkinter as ctk
from tkinter import messagebox

class FrmBajaLibro(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Estilo
        self.configure(fg_color="#F3E7D2")
        self.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(header, text="⬅ Volver", width=80, fg_color="#A7744A", 
                      command=self.controller.volver_al_menu).pack(side="left")
        
        ctk.CTkLabel(header, text="Eliminar Libros", font=("Georgia", 24, "bold"), 
                     text_color="#5a3b2e").pack(side="left", padx=20)

        # Panel de Búsqueda
        panel = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        panel.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(panel, text="Ingrese el ID del Ejemplar:", font=("Arial", 14)).pack(pady=(20,5))
        
        self.entry_id = ctk.CTkEntry(panel, width=200, justify="center")
        self.entry_id.pack(pady=5)
        self.entry_id.bind("<Return>", self.buscar)

        ctk.CTkButton(panel, text="Buscar Libro", fg_color="#A7744A", command=self.buscar).pack(pady=15)

        # Panel de Datos (Oculto al inicio)
        self.lbl_datos = ctk.CTkLabel(panel, text="", font=("Arial", 16, "bold"), text_color="#5a3b2e")
        self.lbl_datos.pack(pady=10)

        self.btn_confirmar = ctk.CTkButton(
            panel, 
            text="CONFIRMAR", 
            fg_color="#D32F2F", hover_color="#B71C1C",
            state="disabled", command=self.confirmar
            )
        self.btn_confirmar.pack(pady=(0, 20))

    def buscar(self, event=None):
        id_libro = self.entry_id.get()
        if not id_libro: return

        info = self.controller.obtener_info_ejemplar(id_libro)
        if info:
            texto = f"Título: {info['titulo']}\nEstado: {info['estado']}\nUbicación: {info['ubicacion']}"
            self.lbl_datos.configure(text=texto)
            
            if info['estado'] == 'Disponible':
                self.btn_confirmar.configure(state="normal", text="CONFIRMAR BAJA")
            else:
                self.btn_confirmar.configure(state="disabled", text=f"NO SE PUEDE ({info['estado']})")
        else:
            self.lbl_datos.configure(text="Libro no encontrado")
            self.btn_confirmar.configure(state="disabled")

    def confirmar(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea dar de baja este libro?"):
            id_libro = self.entry_id.get()
            if self.controller.procesar_baja(id_libro):
                self.entry_id.delete(0, 'end')
                self.lbl_datos.configure(text="")
                self.btn_confirmar.configure(state="disabled")
    
    def mostrar_mensaje(self, msg, error):
        messagebox.showerror("Error", msg) if error else messagebox.showinfo("Éxito", msg)