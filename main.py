import customtkinter as ctk
from src.controller.loginController import LoginController
from src.controller.catalogo_controller import CatalogoController
# CAMBIO IMPORTANTE: Usar modo "light" para que combinen los colores beige/café
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Biblioteca - Congreso de Durango")
        self.geometry("1100x800")
        self.minsize(800, 600)

        # Contenedor principal donde pondremos las vistas (Login o Catalogo)
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # 1. Al arrancar, mostramos el Login
        self.mostrar_login()

    def limpiar_contenedor(self):
        # Elimina cualquier vista que esté actualmente en pantalla
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_contenedor()
        # Invocamos al controlador de Login
        self.login_controller = LoginController(self.container, self)
        self.login_controller.view.pack(fill="both", expand=True)

    def iniciar_sesion_exitoso(self, usuario_obj):
        """
        Este método es llamado por el LoginController cuando los datos son correctos.
        """
        self.usuario_actual = usuario_obj
        # Cambiamos la pantalla al Catálogo
        self.mostrar_catalogo()

    def mostrar_catalogo(self):
        self.limpiar_contenedor()
        # Invocamos al controlador del Catálogo, pasando el ID del usuario real
        self.catalogo_controller = CatalogoController(self.container, id_usuario_actual=self.usuario_actual.id_usuario)
        self.catalogo_controller.view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()