from src.view.login.frm_login import FrmLogin
from src.model.Usuario import Usuario
import hashlib

class LoginController:
    def __init__(self, view_container, app_main):
        self.view_container = view_container
        self.app_main = app_main
        self.view = FrmLogin(view_container, self)

    def validar_credenciales(self, usuario, password):
        
        if not usuario or not password:
            self.view.mostrar_error("Ingrese usuario y contraseña.")
            return

        pass_hash = hashlib.sha256(password.encode()).hexdigest()

        usuario_obj = Usuario.autenticar(usuario, pass_hash)

        if usuario_obj:
            if usuario_obj.activo == 1:
                self.app_main.iniciar_sesion_exitoso(usuario_obj)
            else:
                self.view.mostrar_error("Usuario desactivado.")
        else:
            self.view.mostrar_error("Credenciales incorrectas.")