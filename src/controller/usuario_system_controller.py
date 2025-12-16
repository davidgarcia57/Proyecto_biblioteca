from src.view.admin.frm_usuarios_sistema import FrmUsuariosSistema
from src.model.Usuario import Usuario
from tkinter import messagebox
import hashlib

class UsuarioSystemController:
    # Agregamos id_usuario_sesion al init
    def __init__(self, view_container, id_usuario_sesion, on_close=None):
        self.view_container = view_container
        self.on_close = on_close
        self.id_usuario_sesion = id_usuario_sesion # Guardamos quién está logueado
        
        self.view = FrmUsuariosSistema(view_container, self)
        self.cargar_tabla()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def cargar_tabla(self):
        usuarios = Usuario.obtener_todos()
        self.view.limpiar_tabla()
        for u in usuarios:
            estado = "Activo" if u.activo == 1 else "Inactivo"
            # Mostramos visualmente quién es el usuario actual en la tabla
            nombre_mostrar = u.nombre
            if u.id_usuario == self.id_usuario_sesion:
                nombre_mostrar += " (TÚ)"
                
            self.view.agregar_fila(u.id_usuario, nombre_mostrar, u.usuario, u.rol, estado)

    def guardar_usuario(self, datos, id_editar=None):
        # 1. Validaciones
        if not datos["nombre"] or not datos["usuario"] or not datos["rol"]:
            messagebox.showerror("Error", "Nombre, Usuario y Rol son obligatorios")
            return

        p1 = datos["password"]
        p2 = datos["confirm_pass"]

        # Si es nuevo, la contraseña es obligatoria
        if not id_editar and not p1:
            messagebox.showerror("Error", "La contraseña es obligatoria para nuevos usuarios")
            return

        if p1 != p2:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        pass_hash = None
        if p1:
            pass_hash = hashlib.sha256(p1.encode()).hexdigest()

        # 2. Crear objeto
        nuevo_user = Usuario(
            id_usuario=id_editar,
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            password_hash=pass_hash,
            rol=datos["rol"],
            activo=datos["activo"]
        )

        # 3. Guardar
        if nuevo_user.guardar():
            # Si el usuario se editó a sí mismo y cambió su pass, aquí podríamos avisarle
            if id_editar == self.id_usuario_sesion and pass_hash:
                 messagebox.showinfo("Aviso", "Has cambiado tu propia contraseña.\nÚsala la próxima vez que inicies sesión.")
            
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            self.view.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo guardar (El usuario ya existe o error de BD)")

    def eliminar_usuario(self, id_usuario_a_eliminar):
        # --- PROTECCIÓN ANTI-SUICIDIO ---
        # Convertimos a string por seguridad al comparar
        if str(id_usuario_a_eliminar) == str(self.id_usuario_sesion):
            messagebox.showwarning("Acción Denegada", "❌ No puedes eliminar tu propia cuenta mientras estás conectado.")
            return
        
        if Usuario.eliminar(id_usuario_a_eliminar):
            messagebox.showinfo("Éxito", "Usuario eliminado del sistema.")
            self.view.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")