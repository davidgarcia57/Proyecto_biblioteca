import customtkinter as ctk
from tkinter import messagebox
from src.view.inventario.frm_pasos import Paso1, Paso2, Paso3, Paso4

class FrmNuevoLibro(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Colores
        self.COLOR_FONDO = "#F3E7D2"
        self.COLOR_TEXTO = "#5a3b2e"
        self.COLOR_BOTON = "#A7744A"
        self.COLOR_HOVER = "#8c5e3c"
        
        self.configure(fg_color=self.COLOR_FONDO)

        # Variables
        self.current_step = 0
        self.steps = [] 

        # --- HEADER ---
        self.crear_header()

        # --- CONTENEDOR DE PASOS ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=10)

        # Instanciar los pasos desde el nuevo módulo
        self.paso1 = Paso1(self.container)
        self.paso2 = Paso2(self.container)
        self.paso3 = Paso3(self.container)
        self.paso4 = Paso4(self.container)

        self.steps = [self.paso1, self.paso2, self.paso3, self.paso4]

        # --- FOOTER (Botones) ---
        self.crear_footer()

        # Iniciar
        self.mostrar_paso(0)

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(20, 10))
        
        self.btn_volver = ctk.CTkButton(
            header, text="⬅ Volver al Menú", font=("Arial", 14, "bold"),
            fg_color="transparent", text_color=self.COLOR_BOTON,
            border_width=2, border_color=self.COLOR_BOTON, hover_color=self.COLOR_HOVER,
            command=self.controller.volver_al_menu
        )
        self.btn_volver.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(header, text="Ficha de Ingreso de Libros", font=("Georgia", 26, "bold"), text_color=self.COLOR_TEXTO).pack(side="left")
        
        self.lbl_paginacion = ctk.CTkLabel(header, text="Paso 1 de 4", font=("Arial", 14, "bold"), text_color=self.COLOR_BOTON)
        self.lbl_paginacion.pack(side="right", anchor="s")

    def crear_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent", height=60)
        footer.pack(fill="x", side="bottom", padx=40, pady=30)

        self.btn_atras = ctk.CTkButton(
            footer, text="Cancelar", font=("Georgia", 14),
            fg_color="#D32F2F", hover_color="#B71C1C", width=120, height=40,
            command=self.anterior_paso
        )
        self.btn_atras.pack(side="left")

        self.btn_siguiente = ctk.CTkButton(
            footer, text="Siguiente", font=("Georgia", 14, "bold"),
            fg_color=self.COLOR_BOTON, hover_color=self.COLOR_HOVER, width=150, height=40,
            command=self.siguiente_paso
        )
        self.btn_siguiente.pack(side="right")
        
        self.lbl_mensaje = ctk.CTkLabel(footer, text="", font=("Arial", 12, "bold"))
        self.lbl_mensaje.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_paso(self, index):
        # Ocultar todos
        for step in self.steps:
            step.pack_forget()
        
        # Mostrar actual
        self.steps[index].pack(fill="both", expand=True)
        self.lbl_paginacion.configure(text=f"Paso {index + 1} de {len(self.steps)}")

        # Lógica de botones
        if index == 0:
            self.btn_volver.configure(text="⬅ Volver al Menú", command=self.controller.volver_al_menu)
            self.btn_atras.configure(text="Cancelar", fg_color="#D32F2F")
        else:
            self.btn_volver.configure(text="⬅ Paso Anterior", command=self.anterior_paso)
            self.btn_atras.configure(text="Atrás", fg_color="gray")

        if index == len(self.steps) - 1:
            self.btn_siguiente.configure(text="GUARDAR FICHA", fg_color="#2E7D32")
        else:
            self.btn_siguiente.configure(text="Siguiente", fg_color=self.COLOR_BOTON)

    def siguiente_paso(self):
        # 1. Validar el paso actual usando su propio método
        paso_actual = self.steps[self.current_step]
        es_valido, mensaje_error = paso_actual.validar()

        if not es_valido:
            self.mostrar_mensaje(mensaje_error, True)
            return

        # 2. Avanzar o Guardar
        if self.current_step == len(self.steps) - 1:
            self.evento_guardar()
        else:
            self.current_step += 1
            self.mostrar_paso(self.current_step)
            self.mostrar_mensaje("")

    def anterior_paso(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.mostrar_paso(self.current_step)
            self.mostrar_mensaje("")
        else:
            self.controller.volver_al_menu()

    def evento_guardar(self):
        # Recolectar datos de TODOS los pasos
        datos_completos = {}
        for paso in self.steps:
            datos_completos.update(paso.obtener_datos())
            
        # Enviar al controlador
        self.controller.registrar_libro_completo(datos_completos)

    def confirmar_registro(self, id_generado):
        respuesta = messagebox.askyesno(
            "Registro Exitoso",
            f"¡Libro guardado correctamente!\n\nNo. Adquisición Asignado: {id_generado}\n\n¿Desea registrar otro libro ahora?"
        )
        if respuesta:
            self.limpiar_todo()
        else:
            self.controller.volver_al_menu()

    def limpiar_todo(self):
        # Limpia cada paso usando su método interno
        for paso in self.steps:
            if hasattr(paso, 'limpiar'): # Paso1 y Paso4 tienen métodos específicos
                paso.limpiar()
            else:
                paso.limpiar_campos() # Paso2 y Paso3 usan el genérico
                
        self.current_step = 0
        self.mostrar_paso(0)
        self.mostrar_mensaje("")

    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "red" if es_error else "#2E7D32"
        self.lbl_mensaje.configure(text=mensaje, text_color=color)