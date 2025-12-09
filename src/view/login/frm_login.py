import customtkinter as ctk
import sys

class FrmLogin(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # Fondo general gris
        self.configure(fg_color="#EBEBEB") 

        # --- TARJETA CENTRAL (Más grande para que quepan los textos grandes) ---
        self.card = ctk.CTkFrame(
            self, 
            width=420,      # Aumentado de 360 a 420
            height=550,     # Aumentado de 400 a 550
            corner_radius=20, 
            fg_color="#F3E7D2" # Color Beige
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Título Principal
        self.lbl_titulo = ctk.CTkLabel(
            self.card, 
            text="BIBLIOTECA", 
            font=("Georgia", 36, "bold"), # Aumentado de 22 a 36px
            text_color="#5a3b2e"
        )
        self.lbl_titulo.place(relx=0.5, y=35, anchor="n")

        # Subtítulo
        self.lbl_sub = ctk.CTkLabel(
            self.card, 
            text="Tu portal al conocimiento", 
            font=("Arial", 18), # Arial 18px (más claro que Georgia 16)
            text_color="#7a5a44"
        )
        self.lbl_sub.place(relx=0.5, y=85, anchor="n")

        # --- INPUTS GIGANTES (Altura 55px y Letra 20px) ---
        
        self.entry_user = ctk.CTkEntry(
            self.card,
            placeholder_text="Nombre de usuario",
            width=340,              # Más ancho
            height=55,              # Altura fácil de apuntar
            corner_radius=15,
            border_color="#A7744A",
            border_width=2,         # Borde más visible
            font=("Arial", 20),     # Letra muy legible
            bg_color="#F3E7D2"      # <--- ESTO ARREGLA LOS BORDES FEOS
        )
        self.entry_user.place(relx=0.5, y=180, anchor="center")

        self.entry_pass = ctk.CTkEntry(
            self.card,
            placeholder_text="Contraseña",
            width=340,
            height=55,
            show="*",
            corner_radius=15,
            border_color="#A7744A",
            border_width=2,
            font=("Arial", 20),
            bg_color="#F3E7D2"      # <--- ESTO ARREGLA LOS BORDES FEOS
        )
        self.entry_pass.place(relx=0.5, y=260, anchor="center")

        # Mensaje de error
        self.lbl_error = ctk.CTkLabel(
            self.card, 
            text="", 
            text_color="#D32F2F", 
            font=("Arial", 16, "bold"), # Error más visible
            bg_color="#F3E7D2"          # Asegura fondo limpio
        )
        self.lbl_error.place(relx=0.5, y=310, anchor="center")

        # --- BOTÓN INICIAR (Sólido) ---
        self.btn_login = ctk.CTkButton(
            self.card,
            text="INICIAR SESIÓN",
            width=280,
            height=60,              # Botón masivo
            corner_radius=15,
            fg_color="#A7744A",
            hover_color="#8c5e3c",
            font=("Arial", 20, "bold"),
            bg_color="#F3E7D2",     # <--- ARREGLA BORDES "MORDIDOS"
            command=self.evento_login
        )
        self.btn_login.place(relx=0.5, y=370, anchor="center")

        # --- BOTÓN SALIR (Estilo contorno para diferenciar) ---
        # Este estilo ayuda a que no compita visualmente con el botón principal
        self.btn_cerrar = ctk.CTkButton(
            self.card,
            text="SALIR DEL SISTEMA", # Texto más descriptivo
            width=200,
            height=45,
            corner_radius=15,
            fg_color="transparent",   # Fondo transparente
            border_color="#A7744A",   # Solo borde
            border_width=2,
            text_color="#A7744A",
            hover_color="#E8D6C0",    # Un beige oscurito al pasar mouse
            font=("Arial", 16, "bold"),
            bg_color="#F3E7D2",       # <--- IMPRESCINDIBLE AQUÍ
            command=self.cerrar_aplicacion
        )
        self.btn_cerrar.place(relx=0.5, y=490, anchor="center")

        # Foco y Atajos
        self.entry_user.focus()
        self.entry_user.bind("<Return>", lambda e: self.evento_login())
        self.entry_pass.bind("<Return>", lambda e: self.evento_login())

    def evento_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        # Validación básica en vista para no molestar al controlador por vacíos
        if not user or not password:
            self.mostrar_error("⚠️ Ingrese sus datos")
            return
            
        if self.controller:
            self.controller.validar_credenciales(user, password)

    def mostrar_error(self, mensaje):
        self.lbl_error.configure(text=mensaje)

    def cerrar_aplicacion(self):
        toplevel = self.winfo_toplevel()
        try:
            toplevel.destroy()
        except Exception:
            sys.exit(0)