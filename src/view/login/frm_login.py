import customtkinter as ctk

class FrmLogin(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Configuración del fondo principal (para que contraste con la tarjeta)
        self.configure(fg_color="#EBEBEB") 

        # --- TARJETA CENTRAL ---
        self.card = ctk.CTkFrame(
            self, 
            width=350, 
            height=350, # Un poco más alto para que quepan los mensajes de error
            corner_radius=20, 
            fg_color="#F3E7D2" # Color Beige
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Títulos
        self.lbl_titulo = ctk.CTkLabel(
            self.card, 
            text="BIBLIOTECA", 
            font=("Georgia", 22, "bold"), 
            text_color="#5a3b2e" # Marrón oscuro
        )
        self.lbl_titulo.place(relx=0.5, y=30, anchor="n")

        self.lbl_sub = ctk.CTkLabel(
            self.card, 
            text="Tu portal al conocimiento", 
            font=("Georgia", 14), 
            text_color="#7a5a44" # Marrón claro
        )
        self.lbl_sub.place(relx=0.5, y=65, anchor="n")

        # Campo Usuario
        self.entry_user = ctk.CTkEntry(
            self.card,
            placeholder_text="Nombre de usuario",
            width=250,
            height=40,
            corner_radius=10,
            border_color="#A7744A"
        )
        self.entry_user.place(relx=0.5, y=120, anchor="center")

        # Campo Contraseña
        self.entry_pass = ctk.CTkEntry(
            self.card,
            placeholder_text="Contraseña",
            width=250,
            height=40,
            show="*",
            corner_radius=10,
            border_color="#A7744A"
        )
        self.entry_pass.place(relx=0.5, y=170, anchor="center")

        # Botón (Con el color Bronce/Café)
        self.btn_login = ctk.CTkButton(
            self.card,
            text="INICIAR SESIÓN",
            width=180,
            height=40,
            corner_radius=10,
            fg_color="#A7744A",
            hover_color="#8c5e3c", # Un tono más oscuro al pasar el mouse
            font=("Georgia", 14, "bold"),
            command=self.evento_login
        )
        self.btn_login.place(relx=0.5, y=230, anchor="center")

        # Mensaje de error (Oculto por defecto)
        self.lbl_error = ctk.CTkLabel(
            self.card, 
            text="", 
            text_color="red", 
            font=("Arial", 12)
        )
        self.lbl_error.place(relx=0.5, y=270, anchor="center")

        # Links decorativos
        self.link1 = ctk.CTkLabel(self.card, text="¿Olvidaste tu contraseña?", text_color="#5a3b2e", font=("Arial", 11), cursor="hand2")
        self.link1.place(relx=0.5, y=300, anchor="center")

    def evento_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        self.controller.validar_credenciales(user, password)

    def mostrar_error(self, mensaje):
        self.lbl_error.configure(text=mensaje)