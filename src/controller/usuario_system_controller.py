from src.view.admin.frm_usuarios_sistema import FrmUsuariosSistema
from src.model.Usuario import Usuario
from tkinter import messagebox

class UsuarioSystemController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close
        
        # Inicializamos la vista
        self.view = FrmUsuariosSistema(view_container, self)
        
        # Cargamos los datos iniciales
        self.cargar_tabla()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def cargar_tabla(self):
        usuarios = Usuario.obtener_todos()
        self.view.limpiar_tabla()
        for u in usuarios:
            estado = "Activo" if u.activo == 1 else "Inactivo"
            self.view.agregar_fila(u.id_usuario, u.nombre, u.usuario, u.rol, estado)

    def guardar_usuario(self, datos, id_actual=None):
        if not datos["nombre"] or not datos["usuario"] or not datos["rol"]:
            messagebox.showerror("Error", "Todos los campos (Nombre, Usuario y Rol) son obligatorios")
            return

        # Si es nuevo, la contraseña es obligatoria
        if not id_actual and not datos["password"]:
            messagebox.showerror("Error", "Debe asignar una contraseña al nuevo usuario")
            return

        nuevo_user = Usuario(
            id_usuario=id_actual,
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            password_hash=datos["password"], # Se usará solo si es un INSERT (nuevo)
            rol=datos["rol"],
            activo=1 if datos["activo"] else 0
        )

        if nuevo_user.guardar():
            # Si se editó un usuario existente y se escribió una nueva contraseña, la actualizamos
            if id_actual and datos["password"]:
                Usuario.cambiar_password(id_actual, datos["password"])
                
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            self.view.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo guardar (Posiblemente el nombre de usuario ya existe)")

    def eliminar_usuario(self, id_usuario):
        """Método llamado por el botón 'Eliminar Usuario' de la vista"""
        if Usuario.eliminar(id_usuario):
            messagebox.showinfo("Éxito", "Usuario eliminado del sistema.")
            self.view.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")