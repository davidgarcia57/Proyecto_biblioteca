import customtkinter as ctk
from src.navegador import Router

# Configuración de tema
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Biblioteca - Congreso de Durango")
        
        # En lugar de self.state("zoomed"), usamos un retraso de 0ms
        # para asegurar que la ventana ya existe antes de maximizarla.
        self.after(0, lambda: self.state("zoomed"))
        
        self.minsize(1024, 768)

        # Contenedor principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Estado de la aplicación
        self.usuario_actual = None

        # Inicializamos el Router pasándole 'self' (esta App)
        self.router = Router(self)

        # Iniciamos en el Login usando el router
        self.router.mostrar_login()

    def iniciar_sesion_exitoso(self, usuario_obj):
        """
        Método llamado por LoginController cuando el login es correcto.
        Actualiza el estado y usa el router para cambiar de pantalla.
        """
        self.usuario_actual = usuario_obj
        self.router.mostrar_menu_principal()

if __name__ == "__main__":
    app = App()
    app.mainloop()