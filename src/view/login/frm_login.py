import customtkinter as ctk

class FrmLogin(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # Configuración del fondo principal (para que contraste con la tarjeta)
        self.configure(fg_color="#EBEBEB") 

        # --- TARJETA CENTRAL ---
        self.card = ctk.CTkFrame(
            self, 
            width=360, 
            height=400, # Más alto para mejor espaciado
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
        self.lbl_titulo.place(relx=0.5, y=20, anchor="n")

        self.lbl_sub = ctk.CTkLabel(
            self.card, 
            text="Tu portal al conocimiento", 
            font=("Georgia", 16), 
            text_color="#7a5a44" # Marrón claro
        )
        self.lbl_sub.place(relx=0.5, y=55, anchor="n")

        # Campo Usuario
        self.entry_user = ctk.CTkEntry(
            self.card,
            placeholder_text="Nombre de usuario",
            width=280,
            height=40,
            corner_radius=10,
            border_color="#A7744A"
        )
        self.entry_user.place(relx=0.5, y=110, anchor="center")

        # Campo Contraseña
        self.entry_pass = ctk.CTkEntry(
            self.card,
            placeholder_text="Contraseña",
            width=280,
            height=40,
            show="*",
            corner_radius=10,
            border_color="#A7744A"
        )
        self.entry_pass.place(relx=0.5, y=170, anchor="center")

        # Mensaje de error (Oculto por defecto)
        self.lbl_error = ctk.CTkLabel(
            self.card, 
            text="", 
            text_color="red", 
            font=("Arial", 14)
        )
        self.lbl_error.place(relx=0.5, y=210, anchor="center")

        # Botón (Con el color Bronce/Café)
        self.btn_login = ctk.CTkButton(
            self.card,
            text="INICIAR SESIÓN",
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#A7744A",
            hover_color="#8c5e3c", # Un tono más oscuro al pasar el mouse
            font=("Georgia", 14, "bold"),
            command=self.evento_login
        )
        self.btn_login.place(relx=0.5, y=250, anchor="center")

        # Botón para cerrar la aplicación (cierra la ventana principal)
        self.btn_cerrar = ctk.CTkButton(
            self.card,
            text="CERRAR",
            width=120,
            height=36,
            corner_radius=10,
            fg_color="#A7744A",
            hover_color="#8c5e3c",
            font=("Georgia", 14, "bold"),
            command=self.cerrar_aplicacion
        )
        self.btn_cerrar.place(relx=0.5, y=310, anchor="center")

        # Atajos y foco
        self.entry_user.focus()  # foco inicial en usuario
        # permitir Enter para iniciar sesión desde cualquiera de los entry
        self.entry_user.bind("<Return>", lambda e: self.evento_login())
        self.entry_pass.bind("<Return>", lambda e: self.evento_login())


    def evento_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        self.controller.validar_credenciales(user, password)

    def mostrar_error(self, mensaje):
        self.lbl_error.configure(text=mensaje)

    def cerrar_aplicacion(self):
        # cierra la ventana principal / aplicación completa
        toplevel = self.winfo_toplevel()
        try:
            toplevel.destroy()
        except Exception:
            # como alternativa segura, intentar salir del programa
            import sys
            sys.exit(0)
