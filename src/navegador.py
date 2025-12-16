from src.controller.login_controller import LoginController
from src.controller.catalogo_controller import CatalogoController
from src.controller.busqueda_controller import BusquedaController
from src.controller.solicitante_controller import SolicitanteController
from src.controller.prestamo_controller import PrestamoController
from src.controller.usuario_system_controller import UsuarioSystemController
from src.controller.visitas_controller import VisitasController

# Importamos las vistas que no tienen un controlador complejo propio
# o que se usan como "sub-vistas" simples.
from src.view.circulacion.frm_menu import FrmMenuPrincipal
from src.view.inventario.frm_baja_libro import FrmBajaLibro
from src.view.reportes.frm_generar_reportes import FrmGenerarReportes
# FrmListaPrestamos ya no se importa aquí necesariamente si el controlador la maneja,
# pero no hace daño dejarla si se usa en algún tipo de chequeo.

class ControladorNavegacionSimple:
    """
    Controlador auxiliar para vistas simples que solo necesitan volver al menú.
    Ejemplo: FrmGenerarReportes.
    """
    def __init__(self, router):
        self.router = router

    def volver_menu(self):
        self.router.mostrar_menu_principal()

class Router:
    def __init__(self, app):
        self.app = app
        self.container = app.container

    def limpiar_contenedor(self):
        """Destruye el contenido actual para mostrar una nueva pantalla."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def cerrar_sesion(self):
        """Limpia el usuario actual y regresa al Login."""
        self.app.usuario_actual = None
        self.mostrar_login()

    # =========================================================================
    # RUTAS DE NAVEGACIÓN
    # =========================================================================

    def mostrar_login(self):
        self.limpiar_contenedor()
        controller = LoginController(self.container, self.app)
        # La vista se carga dentro del __init__ del controlador, aquí solo la mostramos
        controller.view.pack(fill="both", expand=True)

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        # El menú principal usa al propio Router como controlador para navegar
        view = FrmMenuPrincipal(self.container, controller=self)
        view.pack(fill="both", expand=True)

    def mostrar_catalogo(self):
        self.limpiar_contenedor()
        controller = CatalogoController(
            self.container, 
            id_usuario_actual=self.app.usuario_actual.id_usuario, 
            on_close=self.mostrar_menu_principal
        )
        controller.view.pack(fill="both", expand=True)

    def mostrar_busqueda(self):
        self.limpiar_contenedor()
        # BusquedaController maneja su propia lógica y popup
        controller = BusquedaController(
            self.container, 
            on_close=self.mostrar_menu_principal, 
            on_add_book=self.mostrar_catalogo
        )
        controller.view.pack(fill="both", expand=True)

    def mostrar_prestamos(self):
        self.limpiar_contenedor()
        controller = PrestamoController(
            self.container, 
            usuario_sistema=self.app.usuario_actual, 
            on_close=self.mostrar_menu_principal
        )
        # Por defecto, PrestamoController carga la vista de "Nuevo Préstamo"
        controller.view.pack(fill="both", expand=True)

    def mostrar_lista_prestamos(self):
        self.limpiar_contenedor()
        # Usamos el mismo controlador de Préstamos
        controller = PrestamoController(
            self.container, 
            usuario_sistema=self.app.usuario_actual, 
            on_close=self.mostrar_menu_principal
        )
        # IMPORTANTE: Llamamos al método especial que cambia la vista a la Lista
        controller.iniciar_lista_prestamos()
    
    def mostrar_solicitantes(self):
        self.limpiar_contenedor()
        controller = SolicitanteController(self.container, on_close=self.mostrar_menu_principal)
        controller.view.pack(fill="both", expand=True)

    def mostrar_baja_libros(self):
        self.limpiar_contenedor()
        # Reutilizamos CatalogoController para la lógica de baja (comparte modelos)
        controller = CatalogoController(
            self.container, 
            id_usuario_actual=self.app.usuario_actual.id_usuario, 
            on_close=self.mostrar_menu_principal
        )
        # Limpiamos la vista por defecto del controlador para poner la de Baja
        for widget in controller.view_container.winfo_children(): widget.destroy()
        
        # Inyectamos manualmente la vista de BajaLibro al controlador existente
        controller.view = FrmBajaLibro(self.container, controller)
        controller.view.pack(fill="both", expand=True)

    def mostrar_reportes_avanzados(self):
        self.limpiar_contenedor()
        # Usamos el controlador simple para esta vista estática
        ctrl_navegacion = ControladorNavegacionSimple(self)
        view = FrmGenerarReportes(self.container, ctrl_navegacion)
        view.pack(fill="both", expand=True)

    def mostrar_usuarios_sistema(self):
        self.limpiar_contenedor()
        
        # Obtenemos el ID del usuario que está logueado actualmente
        id_actual = self.app.usuario_actual.id_usuario
        
        # Se lo pasamos al controlador
        controller = UsuarioSystemController(
            self.container, 
            id_usuario_sesion=id_actual, # <--- NUEVO PARÁMETRO
            on_close=self.mostrar_menu_principal
        )
        controller.view.pack(fill="both", expand=True)

    def mostrar_registro_visitas(self):
        self.limpiar_contenedor()
        controller = VisitasController(self.container, on_close=self.mostrar_menu_principal)
        controller.view.pack(fill="both", expand=True)