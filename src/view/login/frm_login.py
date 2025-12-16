import customtkinter as ctk
import sys
from PIL import Image
import os
from src.utils import resource_path
class FrmLogin(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        # Fondo general gris
        self.configure(fg_color="#EBEBEB") 

        self.card = ctk.CTkFrame(
            self, 
            width=420,
            height=550,
            corner_radius=20, 
            fg_color="#F3E7D2" # Color Beige
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        try:
            ruta_logo = resource_path("resources/logo.png")
            
            if os.path.exists(ruta_logo):
                self.logo_img = ctk.CTkImage(
                    light_image=Image.open(ruta_logo), 
                    size=(120, 120)
                )
                self.lbl_logo = ctk.CTkLabel(self.card, image=self.logo_img, text="")
                self.lbl_logo.place(relx=0.5, y=40, anchor="n")
                ajuste_y = 110 
            else:
                print(f"⚠️ No se encontró el logo en: {ruta_logo}")
                ajuste_y = 0 
                
        except Exception as e:
            print(f"Error cargando logo: {e}")
            ajuste_y = 0

        self.lbl_titulo = ctk.CTkLabel(
            self.card, 
            text="BIBLIOTECA", 
            font=("Georgia", 36, "bold"),
            text_color="#5a3b2e"
        )
        self.lbl_titulo.place(relx=0.5, y=35 + ajuste_y, anchor="n")

        self.lbl_sub = ctk.CTkLabel(
            self.card, 
            text="Tu portal al conocimiento", 
            font=("Arial", 18),
            text_color="#7a5a44"
        )
        self.lbl_sub.place(relx=0.5, y=85 + ajuste_y if ajuste_y == 0 else 85, anchor="n") 
        # Nota: Ajusté la posición del subtítulo para que no se encime si no hay logo

        # --- INPUTS ---
        self.entry_user = ctk.CTkEntry(
            self.card, placeholder_text="Nombre de usuario", width=340, height=55,
            corner_radius=15, border_color="#A7744A", border_width=2,
            font=("Arial", 20), bg_color="#F3E7D2"
        )
        self.entry_user.place(relx=0.5, y=180, anchor="center")

        self.entry_pass = ctk.CTkEntry(
            self.card, placeholder_text="Contraseña", width=340, height=55, show="*",
            corner_radius=15, border_color="#A7744A", border_width=2,
            font=("Arial", 20), bg_color="#F3E7D2"
        )
        self.entry_pass.place(relx=0.5, y=260, anchor="center")

        # Mensaje de error
        self.lbl_error = ctk.CTkLabel(
            self.card, text="", text_color="#D32F2F", 
            font=("Arial", 16, "bold"), bg_color="#F3E7D2"
        )
        self.lbl_error.place(relx=0.5, y=310, anchor="center")

        # Botón Iniciar
        self.btn_login = ctk.CTkButton(
            self.card, text="INICIAR SESIÓN", width=280, height=60,
            corner_radius=15, fg_color="#A7744A", hover_color="#8c5e3c",
            font=("Arial", 20, "bold"), bg_color="#F3E7D2",
            command=self.evento_login
        )
        self.btn_login.place(relx=0.5, y=370, anchor="center")

        # Botón Salir
        self.btn_cerrar = ctk.CTkButton(
            self.card, text="SALIR DEL SISTEMA", width=200, height=45,
            corner_radius=15, fg_color="transparent", border_color="#A7744A", border_width=2,
            text_color="#A7744A", hover_color="#E8D6C0", font=("Arial", 16, "bold"),
            bg_color="#F3E7D2", command=self.cerrar_aplicacion
        )
        self.btn_cerrar.place(relx=0.5, y=490, anchor="center")

        self.entry_user.focus()
        self.entry_user.bind("<Return>", lambda e: self.evento_login())
        self.entry_pass.bind("<Return>", lambda e: self.evento_login())

    def evento_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
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