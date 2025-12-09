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
        # --- LÓGICA DE VALIDACIÓN (Movida desde la vista) ---
        
        # 1. Campos obligatorios básicos
        if not datos["nombre"] or not datos["usuario"] or not datos["rol"]:
            messagebox.showerror("Error", "Nombre, Usuario y Rol son campos obligatorios")
            return

        p1 = datos["password"]
        p2 = datos["confirm_pass"]

        # 2. Coincidencia de contraseñas
        # (Solo validamos si el usuario escribió algo en los campos de contraseña)
        if (p1 or p2) and (p1 != p2):
            messagebox.showerror("Error de Seguridad", "Las contraseñas no coinciden.\nPor favor verifíquelas.")
            return

        # 3. Obligatoriedad de contraseña para NUEVOS usuarios
        # Si es nuevo (id_actual es None) y no puso contraseña
        if not id_actual and not p1:
            messagebox.showerror("Error", "Debe asignar una contraseña al nuevo usuario.")
            return

        # --- CREACIÓN DEL MODELO ---
        nuevo_user = Usuario(
            id_usuario=id_actual,
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            password_hash=p1, # El modelo sabrá si guardarla o ignorarla (si está vacía en edición)
            rol=datos["rol"],
            activo=datos["activo"]
        )

        # --- PERSISTENCIA ---
        if nuevo_user.guardar():
            # Si es edición y hubo cambio de contraseña, la actualizamos explícitamente
            if id_actual and p1:
                Usuario.cambiar_password(id_actual, p1)
                
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            self.view.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo guardar.\nEs posible que el nombre de usuario ya exista.")

    def eliminar_usuario(self, id_usuario):
        if Usuario.eliminar(id_usuario):
            messagebox.showinfo("Éxito", "Usuario eliminado del sistema.")
            self.view.limpiar_formulario()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")