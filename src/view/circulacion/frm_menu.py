import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from src.model.Estadisticas import Estadisticas
from src.utils import resource_path
class FrmMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.controller = controller
        
        self.usuario = self.controller.app.usuario_actual
        
        raw_rol = self.usuario.rol if self.usuario else "Invitado"
        nombre_usuario = self.usuario.nombre if self.usuario else "Usuario"

        self.rol_limpio = str(raw_rol).strip().lower()

        print(f"DEBUG - Rol detectado: '{raw_rol}' -> Normalizado: '{self.rol_limpio}'")

        # --- PALETA DE COLORES ---
        self.COLOR_FONDO_MENU = "#A7744A"
        self.COLOR_FONDO_MAIN = "#F3E7D2" 
        self.COLOR_BOTON_MENU = "#8c5e3c"
        self.COLOR_TEXTO = "#000000"
        self.COLOR_TARJETAS = "#FFFFFF"
        
        self.configure(fg_color=self.COLOR_FONDO_MAIN)
        
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        
        #Barra lateral
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=self.COLOR_FONDO_MENU)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        #LOGO Y TÍTULO
        frm_logo = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        frm_logo.pack(pady=(30, 10), padx=20)

        try:
            ruta_img = resource_path("resources/logo.png")
            
            if os.path.exists(ruta_img):
                img_pil = Image.open(ruta_img)
                self.logo_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(130, 130))
                ctk.CTkLabel(frm_logo, text="", image=self.logo_img).pack(pady=(0, 10))
        except Exception:
            pass 

        ctk.CTkLabel(
            frm_logo, 
            text="BIBLIOTECA\nCONGRESO", 
            font=("Arial", 24, "bold"), 
            text_color="white"
        ).pack()

        #MENÚ DE NAVEGACIÓN
        self.frm_nav = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.frm_nav.pack(fill="x", pady=10)

        self.crear_boton_menu(self.frm_nav, " 🔍 Consultar Libro", self.controller.mostrar_busqueda)
        self.crear_boton_menu(self.frm_nav, " ➕ Agregar Libro", self.controller.mostrar_catalogo)
        self.crear_boton_menu(self.frm_nav, " ➖ Quitar Libro", self.controller.mostrar_baja_libros)
        
        # Separador visual
        ctk.CTkFrame(self.frm_nav, height=2, fg_color="#D7CCC8").pack(fill="x", padx=20, pady=10)
        
        self.crear_boton_menu(self.frm_nav, " ⏳ Préstamos", self.controller.mostrar_prestamos)
        self.crear_boton_menu(self.frm_nav, " ✅ Devoluciones", self.controller.mostrar_lista_prestamos) 
        self.crear_boton_menu(self.frm_nav, " 👥 Lectores", self.controller.mostrar_solicitantes)
        self.crear_boton_menu(self.frm_nav, " 📊 Reportes", self.controller.mostrar_reportes_avanzados)
        self.crear_boton_menu(self.frm_nav, " 🚶 Visitas", self.controller.mostrar_registro_visitas)

        #INICIO DEL CAMBIO
        # Si el usuario es Administrador, le mostramos el botón de gestión de usuarios
        if self.rol_limpio in ["admin", "administrador"]:
             #Pequeño separador visual
             ctk.CTkFrame(self.frm_nav, height=2, fg_color="#D7CCC8").pack(fill="x", padx=20, pady=10)
             
             self.crear_boton_menu(self.frm_nav, " ⚙️ Usuarios", self.controller.mostrar_usuarios_sistema)
        #Area Principal
        self.main_content = ctk.CTkFrame(self, fg_color=self.COLOR_FONDO_MAIN, corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        
        self.main_content.grid_rowconfigure(0, weight=0) 
        self.main_content.grid_rowconfigure(1, weight=1) 
        self.main_content.grid_rowconfigure(2, weight=0) 
        self.main_content.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self.main_content, height=90, fg_color="white", corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.lbl_seccion = ctk.CTkLabel(
            self.header_frame, 
            text=f"Bienvenido, {nombre_usuario}", 
            font=("Arial", 28, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        self.lbl_seccion.pack(side="left", padx=30, pady=20)
        
        if self.rol_limpio in ["admin", "administrador"]:
            self.btn_config = ctk.CTkButton(
                self.header_frame, 
                text="⚙️", 
                font=("Arial", 30), 
                width=50, 
                height=50, 
                fg_color="transparent", 
                text_color=self.COLOR_TEXTO, 
                hover_color="#E0E0E0", 
                command=self.controller.mostrar_usuarios_sistema
            )
            self.btn_config.pack(side="right", padx=30)

        #Dashboard
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.dashboard_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        
        self.dashboard_frame.columnconfigure((0, 1, 2), weight=1)
        
        try:
            datos = Estadisticas.obtener_resumen()
        except Exception:
            datos = {"libros": 0, "prestamos": 0, "usuarios": 0}

        self.crear_tarjeta_info(self.dashboard_frame, "Total Obras", str(datos["libros"]), "📚", 0, 0)
        self.crear_tarjeta_info(self.dashboard_frame, "En Préstamo", str(datos["prestamos"]), "⏳", 0, 1)
        self.crear_tarjeta_info(self.dashboard_frame, "Lectores", str(datos["usuarios"]), "👥", 0, 2)

        lbl_rapidos = ctk.CTkLabel(
            self.dashboard_frame, 
            text="Accesos Rápidos", 
            font=("Arial", 24, "bold"), 
            text_color=self.COLOR_TEXTO
        )
        lbl_rapidos.grid(row=1, column=0, sticky="w", pady=(40, 15), padx=10)

        frame_acciones = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        frame_acciones.grid(row=2, column=0, columnspan=3, sticky="ew")
        frame_acciones.columnconfigure((0, 1), weight=1)
        
        self.crear_boton_rapido(frame_acciones, "Nueva Visita", "🚶", self.controller.mostrar_registro_visitas, 0, 0)
        self.crear_boton_rapido(frame_acciones, "Prestar Libro", "📖", self.controller.mostrar_prestamos, 0, 1)
        self.crear_boton_rapido(frame_acciones, "Devolver Libro", "✅", self.controller.mostrar_lista_prestamos, 1, 0)
        self.crear_boton_rapido(frame_acciones, "Buscar Libro", "🔍", self.controller.mostrar_busqueda, 1, 1)

        #Privacidad y salirse
        self.footer_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", pady=(0, 30), padx=30)
        
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=0)

        self.btn_privacidad = ctk.CTkButton(
            self.footer_frame, 
            text="📜  AVISO DE PRIVACIDAD", 
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            text_color="#A7744A",
            border_width=2,
            border_color="#A7744A",
            hover_color="#E8D6C0",
            height=45,
            width=280,
            command=self.abrir_privacidad
        )
        self.btn_privacidad.grid(row=0, column=0)

        #BOTÓN CERRAR SESIÓN (ESQUINA INFERIOR DERECHA)
        self.btn_logout = ctk.CTkButton(
            self.footer_frame, 
            text="Cerrar Sesión", 
            font=("Arial", 16, "bold"), 
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            width=150, 
            height=45, 
            command=self.confirmar_salida
        )
        self.btn_logout.grid(row=0, column=1, sticky="e", padx=(20, 0))

    # Auxiliares
    def crear_boton_menu(self, parent, texto, comando):
        btn = ctk.CTkButton(
            parent, 
            text=texto, 
            anchor="w", 
            fg_color="transparent", 
            text_color="white", 
            hover_color=self.COLOR_BOTON_MENU, 
            font=("Arial", 18, "bold"),
            height=50,
            command=comando
        )
        btn.pack(fill="x", padx=10, pady=4) 

    def crear_tarjeta_info(self, parent, titulo, dato, icono, fila, col):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_color="#D7CCC8", border_width=2)
        card.grid(row=fila, column=col, padx=10, pady=10, sticky="nsew")
        
        bar = ctk.CTkFrame(card, height=15, fg_color=self.COLOR_FONDO_MENU, corner_radius=0)
        bar.pack(fill="x", side="top")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(expand=True, pady=15)
        
        ctk.CTkLabel(inner, text=icono, font=("Arial", 50)).pack(pady=(0, 5)) 
        ctk.CTkLabel(inner, text=dato, font=("Arial", 42, "bold"), text_color=self.COLOR_TEXTO).pack() 
        ctk.CTkLabel(inner, text=titulo, font=("Arial", 18), text_color="#555555").pack() 

    def crear_boton_rapido(self, parent, texto, icono, comando, fila, col):
        btn = ctk.CTkButton(
            parent, 
            text=f"{icono}  {texto}", 
            font=("Arial", 22, "bold"),
            height=90,
            fg_color="white",
            text_color=self.COLOR_TEXTO,
            hover_color="#EBEBEB",
            border_color=self.COLOR_FONDO_MENU,
            border_width=2,
            command=comando
        )
        btn.grid(row=fila, column=col, padx=15, pady=10, sticky="ew")

    def abrir_privacidad(self):
        filename = "resources/AVISO DE PRIVACIDAD INTEGRAL DE LOS SERVICIOS BIBLIOTECARIOS.pdf"
        ruta_pdf = resource_path(filename)

        if os.path.exists(ruta_pdf):
            try:
                os.startfile(ruta_pdf)
            except Exception as e:
                messagebox.showerror("Error", f"Error al abrir PDF: {e}")
        else:
            messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_pdf}")

    def confirmar_salida(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar su sesión?")
        if respuesta:
            if hasattr(self.controller, 'cerrar_sesion'):
                self.controller.cerrar_sesion()
            else:
                self.controller.mostrar_login()