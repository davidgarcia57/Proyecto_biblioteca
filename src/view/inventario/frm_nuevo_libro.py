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

        self.crear_header()

        self.crear_footer()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=10)

        # Instanciar los pasos 
        self.paso1 = Paso1(self.container)
        self.paso2 = Paso2(self.container)
        self.paso3 = Paso3(self.container)
        self.paso4 = Paso4(self.container)

        self.steps = [self.paso1, self.paso2, self.paso3, self.paso4]

        # Iniciar
        self.mostrar_paso(0)

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(side="top", fill="x", padx=40, pady=(20, 10))
        
        self.btn_volver = ctk.CTkButton(
            header, 
            text="⬅ Volver al Menú", 
            font=("Arial", 16, "bold"), 
            fg_color="transparent", 
            text_color=self.COLOR_BOTON,
            border_width=2, 
            border_color=self.COLOR_BOTON, 
            hover_color=self.COLOR_FONDO,
            height=50,
            width=160,
            command=self.controller.volver_al_menu
        )
        self.btn_volver.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            header, 
            text="Ficha de Ingreso de Libros", 
            font=("Arial", 32, "bold"), 
            text_color=self.COLOR_TEXTO
        ).pack(side="left")
        
        self.lbl_paginacion = ctk.CTkLabel(
            header, 
            text="Paso 1 de 4", 
            font=("Arial", 20, "bold"), 
            text_color=self.COLOR_BOTON
        )
        self.lbl_paginacion.pack(side="right", anchor="s")

    def crear_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent", height=100)
        footer.pack(side="bottom", fill="x", padx=40, pady=30)

        self.btn_atras = ctk.CTkButton(
            footer, 
            text="Cancelar", 
            font=("Arial", 18, "bold"),
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            width=160, 
            height=55,
            command=self.anterior_paso
        )
        self.btn_atras.pack(side="left")

        self.btn_siguiente = ctk.CTkButton(
            footer, 
            text="Siguiente ➡", 
            font=("Arial", 18, "bold"),
            fg_color=self.COLOR_BOTON, 
            hover_color=self.COLOR_HOVER, 
            width=200, 
            height=55,
            command=self.siguiente_paso
        )
        self.btn_siguiente.pack(side="right")
        
        self.lbl_mensaje = ctk.CTkLabel(
            footer, 
            text="", 
            font=("Arial", 18, "bold"), 
            height=30
        )
        self.lbl_mensaje.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_paso(self, index):
        for step in self.steps:
            step.pack_forget()
        
        self.steps[index].pack(fill="both", expand=True)
        self.lbl_paginacion.configure(text=f"Paso {index + 1} de {len(self.steps)}")

        # Lógica de botones
        if index == 0:
            self.btn_volver.configure(text="⬅ Volver al Menú", command=self.controller.volver_al_menu)
            self.btn_atras.configure(text="Cancelar", fg_color="#D32F2F")
        else:
            self.btn_volver.configure(text="⬅ Paso Anterior", command=self.anterior_paso)
            self.btn_atras.configure(text="⬅ Atrás", fg_color="gray")

        if index == len(self.steps) - 1:
            self.btn_siguiente.configure(text="💾 GUARDAR FICHA", fg_color="#2E7D32", hover_color="#1B5E20")
        else:
            self.btn_siguiente.configure(text="Siguiente ➡", fg_color=self.COLOR_BOTON, hover_color=self.COLOR_HOVER)

    def siguiente_paso(self):
        paso_actual = self.steps[self.current_step]
        es_valido, mensaje_error = paso_actual.validar()

        if not es_valido:
            self.mostrar_mensaje(f"⚠ {mensaje_error}", True)
            return

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
        datos_completos = {}
        for paso in self.steps:
            datos_completos.update(paso.obtener_datos())
            
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
        for paso in self.steps:
            if hasattr(paso, 'limpiar'):
                paso.limpiar()
            else:
                paso.limpiar_campos()
                
        self.current_step = 0
        self.mostrar_paso(0)
        self.mostrar_mensaje("✅ Listo para nuevo registro", False)

    def mostrar_mensaje(self, mensaje, es_error=False):
        color = "#C62828" if es_error else "#2E7D32"
        self.lbl_mensaje.configure(text=mensaje, text_color=color)