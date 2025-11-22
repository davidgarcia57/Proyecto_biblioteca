from src.view.login.frm_login import FrmLogin
from src.model.Usuario import Usuario

class LoginController:
    def __init__(self, view_container, app_main):
        self.view_container = view_container
        self.app_main = app_main
        self.view = FrmLogin(view_container, self)

    def validar_credenciales(self, usuario, password):
        # 1. Validación básica (Lógica de Controlador)
        if not usuario or not password:
            self.view.mostrar_error("Ingrese usuario y contraseña.")
            return

        # 2. Llamada al Modelo (El modelo maneja la conexión interna en este caso simple)
        usuario_obj = Usuario.autenticar(usuario, password)

        if usuario_obj:
            if usuario_obj.activo == 1:
                self.app_main.iniciar_sesion_exitoso(usuario_obj)
            else:
                self.view.mostrar_error("Usuario desactivado.")
        else:
            self.view.mostrar_error("Credenciales incorrectas.")