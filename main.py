import customtkinter as ctk
from src.controller.catalogo_controller import CatalogoController

# Configuracion temporal de como se ve (DEMO)
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la Ventana Principal (Temporal hasta que encontremos el estilo DEMO)
        self.title("Sistema de Biblioteca - Congreso de Durango")
        self.geometry("1100x800")
        self.minsize(800, 600)

        # Aqui iria el log-in (IMPORTANTE DEJARLO COMO ESTA HASTA CREAR EL LOG-IN) 
        # Por ahora solo acepta el valor 1 (estaba trasteando para crear un inicio de sesion pero no me da el tiempo) para que el sistema de auditoría funcione.
        id_usuario_sesion = 1 

        # Controlador
        self.controlador_catalogo = CatalogoController(self, id_usuario_actual=id_usuario_sesion)

        # Aquí está la vista (Nota mental: siempre invocarla JAJAJAJAJAJAJ p.p)
        self.controlador_catalogo.view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()