import customtkinter as ctk
import sys
from PIL import Image
import os
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
        ruta_logo = os.path.join("resources", "logo.png") 
        
        try:
            # 1. Cargamos la imagen y la guardamos en SELF (self.logo_img)
            # Si no usas 'self.', Python la borra de la memoria y se ve vacía.
            self.logo_img = ctk.CTkImage(
                light_image=Image.open(ruta_logo), 
                size=(120, 120) # Ajusta el tamaño a tu gusto
            )

            # 2. Creamos el label usando esa imagen guardada en self
            self.lbl_logo = ctk.CTkLabel(self.card, image=self.logo_img, text="")
            self.lbl_logo.place(relx=0.5, y=40, anchor="n") # Ajustamos posición
            
            # (Opcional) Si pones logo, baja un poco el título para que no se encimen:
            ajuste_y = 110 
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            ajuste_y = 0

        # Título Principal (Modifiqué 'y' para dar espacio al logo)
        self.lbl_titulo = ctk.CTkLabel(
            self.card, 
            text="BIBLIOTECA", 
            font=("Georgia", 36, "bold"),
            text_color="#5a3b2e"
        )
        # Si usaste el logo, cambia y=35 por y=(35 + ajuste_y) o un valor fijo como 160
        self.lbl_titulo.place(relx=0.5, y=35 + ajuste_y, anchor="n")

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