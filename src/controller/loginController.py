from src.dao.usuario_dao import UsuarioDAO
from src.view.login.frm_login import FrmLogin

class LoginController:
    def __init__(self, view_container, app_main):
        """
        app_main: Es una referencia a la clase App en main.py para poder cambiar de pantalla
        """
        self.view_container = view_container
        self.app_main = app_main
        self.dao = UsuarioDAO()
        
        # Inicializamos la vista
        self.view = FrmLogin(view_container, self)

    def validar_credenciales(self, usuario, password):
        if not usuario or not password:
            self.view.mostrar_error("Por favor ingrese usuario y contraseña.")
            return

        # Consultar BD
        usuario_obj = self.dao.autenticar(usuario, password)

        if usuario_obj:
            # LOGIN EXITOSO: Llamamos al método en main.py para cambiar de pantalla
            print(f"Bienvenido {usuario_obj.nombre_completo}")
            self.app_main.iniciar_sesion_exitoso(usuario_obj)
        else:
            self.view.mostrar_error("Usuario o contraseña incorrectos.")