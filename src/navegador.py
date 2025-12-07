import tkinter as tk # Importamos tkinter para el Menú Nativo
from src.controller.login_controller import LoginController
from src.controller.catalogo_controller import CatalogoController
from src.controller.busqueda_controller import BusquedaController
from src.controller.solicitante_controller import SolicitanteController
from src.controller.prestamo_controller import PrestamoController
from src.controller.usuario_system_controller import UsuarioSystemController
from src.controller.visitas_controller import VisitasController

# Vistas simples
from src.view.circulacion.frm_menu import FrmMenuPrincipal
from src.view.inventario.frm_baja_libro import FrmBajaLibro
from src.view.reportes.frm_generar_reportes import FrmGenerarReportes
from src.view.circulacion.frm_lista_prestamos import FrmListaPrestamos

class ControladorNavegacionSimple:
    def __init__(self, router):
        self.router = router
    def volver_menu(self):
        self.router.mostrar_menu_principal()

class Router:
    def __init__(self, app):
        self.app = app
        self.container = app.container

    def limpiar_contenedor(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- LÓGICA DE LA BARRA DE MENÚ (NUEVO AQUÍ) ---
    def configurar_menu_superior(self):
        """Construye y asigna la barra de menú nativa a la ventana principal"""
        barra_menu = tk.Menu(self.app)

        # 1. MENÚ ARCHIVO
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Inicio (Dashboard)", command=self.mostrar_menu_principal)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_archivo.add_command(label="Salir", command=self.app.destroy)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        # 2. MENÚ LIBROS
        menu_libros = tk.Menu(barra_menu, tearoff=0)
        menu_libros.add_command(label="Consultar Libro", command=self.mostrar_busqueda)
        menu_libros.add_command(label="Agregar Libro", command=self.mostrar_catalogo)
        menu_libros.add_command(label="Quitar Libro", command=self.mostrar_baja_libros)
        barra_menu.add_cascade(label="Libros", menu=menu_libros)

        # 3. MENÚ CIRCULACIÓN
        menu_circulacion = tk.Menu(barra_menu, tearoff=0)
        menu_circulacion.add_command(label="Realizar Préstamo", command=self.mostrar_prestamos)
        menu_circulacion.add_command(label="Lista de Préstamos Activos", command=self.mostrar_lista_prestamos)
        menu_circulacion.add_separator()
        menu_circulacion.add_command(label="Gestionar Solicitantes", command=self.mostrar_solicitantes)
        menu_circulacion.add_command(label="Registro de Visitas", command=self.mostrar_registro_visitas)
        barra_menu.add_cascade(label="Circulación", menu=menu_circulacion)

        # 4. MENÚ REPORTES
        menu_reportes = tk.Menu(barra_menu, tearoff=0)
        menu_reportes.add_command(label="📊 Generar Reportes PDF", command=self.mostrar_reportes_avanzados)
        barra_menu.add_cascade(label="Reportes", menu=menu_reportes)

        # 5. MENÚ CONFIGURACIÓN (SOLO ADMIN)
        # Accedemos al usuario a través de la app
        usuario = self.app.usuario_actual
        if usuario and usuario.rol == 'Admin':
            menu_config = tk.Menu(barra_menu, tearoff=0)
            menu_config.add_command(label="🔐 Configuración del Sistema", command=self.mostrar_usuarios_sistema)
            barra_menu.add_cascade(label="Configuración", menu=menu_config)

        # Asignar el menú a la ventana principal (App)
        self.app.config(menu=barra_menu)

    def cerrar_sesion(self):
        """Limpia el usuario, quita el menú y vuelve al login"""
        self.app.usuario_actual = None
        # Quitamos el menú superior pasando un menú vacío
        self.app.config(menu=tk.Menu(self.app)) 
        self.mostrar_login()

    # --- RUTAS DE NAVEGACIÓN ---

    def mostrar_login(self):
        self.limpiar_contenedor()
        controller = LoginController(self.container, self.app)
        controller.view.pack(fill="both", expand=True)

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        # Pasamos 'self' como controller porque el menú necesita navegar
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
        controller = BusquedaController(self.container, on_close=self.mostrar_menu_principal, on_add_book=self.mostrar_catalogo)
        controller.view.pack(fill="both", expand=True)

    def mostrar_prestamos(self):
        self.limpiar_contenedor()
        controller = PrestamoController(
            self.container, 
            usuario_sistema=self.app.usuario_actual, 
            on_close=self.mostrar_menu_principal
        )
        controller.view.pack(fill="both", expand=True)
    
    def mostrar_solicitantes(self):
        self.limpiar_contenedor()
        controller = SolicitanteController(self.container, on_close=self.mostrar_menu_principal)
        controller.view.pack(fill="both", expand=True)

    def mostrar_baja_libros(self):
        self.limpiar_contenedor()
        # Reutilizamos CatalogoController para la lógica de baja (o podrías crear uno propio)
        controller = CatalogoController(
            self.container, 
            id_usuario_actual=self.app.usuario_actual.id_usuario, 
            on_close=self.mostrar_menu_principal
        )
        # Hack rápido: Limpiamos la vista por defecto del controller y ponemos la de Baja
        for widget in controller.view_container.winfo_children(): widget.destroy()
        
        controller.view = FrmBajaLibro(self.container, controller)
        controller.view.pack(fill="both", expand=True)

    def mostrar_lista_prestamos(self):
        self.limpiar_contenedor()
        controller = PrestamoController(
            self.container, 
            usuario_sistema=self.app.usuario_actual, 
            on_close=self.mostrar_menu_principal
        )
        for widget in controller.view_container.winfo_children(): widget.destroy()

        controller.view = FrmListaPrestamos(self.container, controller)
        controller.view.pack(fill="both", expand=True)

    def mostrar_reportes_avanzados(self):
        self.limpiar_contenedor()
        ctrl_navegacion = ControladorNavegacionSimple(self)
        view = FrmGenerarReportes(self.container, ctrl_navegacion)
        view.pack(fill="both", expand=True)

    def mostrar_usuarios_sistema(self):
        self.limpiar_contenedor()
        controller = UsuarioSystemController(self.container, on_close=self.mostrar_menu_principal)
        controller.view.pack(fill="both", expand=True)

    def mostrar_registro_visitas(self):
        self.limpiar_contenedor()
        controller = VisitasController(self.container, on_close=self.mostrar_menu_principal)
        controller.view.pack(fill="both", expand=True)