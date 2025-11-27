import customtkinter as ctk
#Imports del controlador
from src.controller.busqueda_controller import BusquedaController
from src.controller.prestamo_controller import PrestamoController
from src.controller.login_controller import LoginController
from src.controller.catalogo_controller import CatalogoController
#Imports del view
from src.view.circulacion.frm_menu import FrmMenuPrincipal
from src.view.inventario.frm_buscar_libro import FmrBuscarLibro 

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
        self.usuario_actual = usuario_obj
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        self.menu_view = FrmMenuPrincipal(self.container, controller=self)
        self.menu_view.pack(fill="both", expand=True)

    def mostrar_catalogo(self):
        self.limpiar_contenedor()
        self.catalogo_controller = CatalogoController(
            self.container, 
            id_usuario_actual=self.usuario_actual.id_usuario, 
            on_close=self.mostrar_menu_principal
        )
        self.catalogo_controller.view.pack(fill="both", expand=True)
    
    def mostrar_busqueda(self):
        self.limpiar_contenedor()
        self.busqueda_controller = BusquedaController(
            self.container, 
            on_close=self.mostrar_menu_principal)
        self.busqueda_controller.view.pack(fill="both", expand=True)

    def mostrar_prestamos(self):
        self.limpiar_contenedor()
        self.prestamo_controller = PrestamoController(
            self.container, 
            usuario_sistema=self.usuario_actual, 
            on_close=self.mostrar_menu_principal
        )
        self.prestamo_controller.view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()