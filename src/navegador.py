from src.controller.login_controller import LoginController
from src.controller.catalogo_controller import CatalogoController
from src.controller.busqueda_controller import BusquedaController
from src.controller.prestamo_controller import PrestamoController
from src.view.circulacion.frm_menu import FrmMenuPrincipal

class Router:
    def __init__(self, app):
        self.app = app
        self.container = app.container

    def limpiar_contenedor(self):
        """Elimina la vista actual para mostrar una nueva."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_contenedor()
        # LoginController necesita 'app' para llamar a iniciar_sesion_exitoso
        controller = LoginController(self.container, self.app)
        controller.view.pack(fill="both", expand=True)

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        # Pasamos 'self' como controller para que el menú pueda navegar
        view = FrmMenuPrincipal(self.container, controller=self)
        view.pack(fill="both", expand=True)

    def mostrar_catalogo(self):
        self.limpiar_contenedor()
        controller = CatalogoController(
            self.container, 
            id_usuario_actual=self.app.usuario_actual.id_usuario, 
            on_close=self.mostrar_menu_principal # Callback al router
        )
        controller.view.pack(fill="both", expand=True)

    def mostrar_busqueda(self):
        self.limpiar_contenedor()
        controller = BusquedaController(
            self.container, 
            on_close=self.mostrar_menu_principal
        )
        controller.view.pack(fill="both", expand=True)

    def mostrar_prestamos(self):
        self.limpiar_contenedor()
        controller = PrestamoController(
            self.container, 
            usuario_sistema=self.app.usuario_actual, 
            on_close=self.mostrar_menu_principal
        )
        controller.view.pack(fill="both", expand=True)