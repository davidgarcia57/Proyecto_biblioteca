import customtkinter as ctk
from src.controller.loginController import LoginController
from src.controller.catalogo_controller import CatalogoController
from src.view.circulacion.frm_menu import FrmMenuPrincipal
from src.view.inventario.frm_buscar_libro import FmrBuscarLibro
from src.controller.busqueda_controller import BusquedaController

# Configuración de tema
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Biblioteca - Congreso de Durango")
        self.state("zoomed")
        self.minsize(1024, 768)

        # Contenedor principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Iniciamos en el Login
        self.mostrar_login()

    def limpiar_contenedor(self):
        """Elimina la vista actual para mostrar una nueva."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_contenedor()
        self.login_controller = LoginController(self.container, self)
        self.login_controller.view.pack(fill="both", expand=True)

    def iniciar_sesion_exitoso(self, usuario_obj):
        """Método llamado desde el Login cuando las credenciales son correctas."""
        self.usuario_actual = usuario_obj
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        # Pasamos 'self' como controlador para que el menú pueda llamar a mostrar_catalogo
        self.menu_view = FrmMenuPrincipal(self.container, controller=self)
        self.menu_view.pack(fill="both", expand=True)

    def mostrar_catalogo(self):
        self.limpiar_contenedor()
        # Pasamos 'app_main=self' para que el catálogo pueda volver al menú con el botón 'Atrás'
        self.catalogo_controller = CatalogoController(
            self.container, 
            id_usuario_actual=self.usuario_actual.id_usuario, 
            on_close=self.mostrar_menu_principal
        )
        self.catalogo_controller.view.pack(fill="both", expand=True)
    
    def mostrar_busqueda(self):
        self.limpiar_contenedor()
        # Pasamos 'self' como controlador para que el menú pueda llamar a mostrar_busqueda
        self.busqueda_controller = BusquedaController(
            self.container, 
            on_close=self.mostrar_menu_principal)
        self.busqueda_controller.view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()