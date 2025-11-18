import customtkinter as ctk

class FrmNuevoLibro(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller # Referencia al controlador para avisarle de eventos
        
        self.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text="Ficha de Ingreso - Libros", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)

        # Input: Título del Libro
        self.entry_titulo = ctk.CTkEntry(self, placeholder_text="Título del Libro", width=300)
        self.entry_titulo.pack(pady=5)

        # Input: ISBN
        self.entry_isbn = ctk.CTkEntry(self, placeholder_text="ISBN (020)", width=300)
        self.entry_isbn.pack(pady=5)

        # Input: Clasificación
        self.entry_clasif = ctk.CTkEntry(self, placeholder_text="Clasificación (050)", width=300)
        self.entry_clasif.pack(pady=5)
        
        # Input: ID Editorial (Por ahora manual, luego haremos un ComboBox)
        self.entry_editorial = ctk.CTkEntry(self, placeholder_text="ID Editorial (Número)", width=300)
        self.entry_editorial.pack(pady=5)

        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(self, text="Guardar Ficha", command=self.evento_guardar)
        self.btn_guardar.pack(pady=20)

    def evento_guardar(self):
        # La vista recolecta los datos y se los pasa al controlador
        datos = {
            "titulo": self.entry_titulo.get(),
            "isbn": self.entry_isbn.get(),
            "clasificacion": self.entry_clasif.get(),
            "editorial": self.entry_editorial.get()
        }
        self.controller.registrar_libro(datos)
    
    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "red" if es_error else "green"
        lbl_msg = ctk.CTkLabel(self, text=mensaje, text_color=color)
        lbl_msg.pack(pady=5)