import customtkinter as ctk
from src.controller.catalogo_controller import CatalogoController

# Configuración de CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca - Congreso de Durango")
        self.geometry("1024x760")

        # Iniciar el controlador de Catálogo
        # Le pasamos 'self' porque 'App' actúa como el contenedor principal
        self.controlador = CatalogoController(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()