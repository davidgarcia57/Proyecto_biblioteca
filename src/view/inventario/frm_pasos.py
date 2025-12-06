import customtkinter as ctk
from datetime import datetime

# --- CLASE BASE PARA COMPARTIR HERRAMIENTAS ---
class PasoBase(ctk.CTkFrame):
    def __init__(self, master, titulo_paso):
        super().__init__(master, fg_color="transparent")
        
        # Colores
        self.COLOR_TEXTO = "#5a3b2e"
        self.COLOR_BOTON = "#A7744A"
        self.COLOR_LINEA = "#A7744A"
        
        # Título del Paso
        self.crear_encabezado(titulo_paso)
        
        # Frame principal del grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)
        self.grid_frame.columnconfigure((0, 1), weight=1)

    def crear_encabezado(self, texto):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(frame, text=texto, font=("Georgia", 20, "bold"), text_color=self.COLOR_TEXTO).pack(side="left")
        ctk.CTkFrame(self, height=2, fg_color=self.COLOR_LINEA).pack(fill="x", pady=(0, 20))

    def crear_input(self, label_text, row, col, colspan=1):
        ctk.CTkLabel(self.grid_frame, text=label_text, font=("Georgia", 12, "bold"), text_color=self.COLOR_TEXTO).grid(row=row, column=col, sticky="w", pady=(10, 5), padx=10)
        
        entry = ctk.CTkEntry(self.grid_frame, placeholder_text=label_text, fg_color="white", text_color="black", border_color=self.COLOR_BOTON, height=35)
        entry.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", pady=(0, 5), padx=10)
        return entry

    def validar_vacio(self, entry, nombre_campo):
        """Retorna (True, "") si es válido, o (False, "Mensaje Error")"""
        texto = entry.get().strip()
        if not texto:
            entry.configure(border_color="red")
            return False, f"El campo '{nombre_campo}' es obligatorio."
        entry.configure(border_color=self.COLOR_BOTON)
        return True, ""

    def validar_numero(self, entry, nombre_campo):
        """Valida que sea numérico"""
        texto = entry.get().strip()
        if texto and not texto.isdigit(): # Si tiene texto y no es numero
            entry.configure(border_color="red")
            return False, f"'{nombre_campo}' debe ser un número entero."
        entry.configure(border_color=self.COLOR_BOTON)
        return True, ""

    def limpiar_campos(self):
        """Busca todos los Entry hijos y los limpia"""
        for widget in self.grid_frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, 'end')
                widget.configure(border_color=self.COLOR_BOTON)

# --- PASO 1: DATOS DE CONTROL ---
class Paso1(PasoBase):
    def __init__(self, master):
        super().__init__(master, "1. Datos de Ficha y Clasificación")
        
        self.entry_ficha = self.crear_input("Ficha No. *", 0, 0)
        self.entry_isbn = self.crear_input("ISBN", 0, 1)
        self.entry_clasif = self.crear_input("Clasificación *", 2, 0, colspan=2)
        
        # Checkboxes Ilustraciones
        ctk.CTkLabel(self.grid_frame, text="Código de ilustraciones", font=("Georgia", 12, "bold"), text_color=self.COLOR_TEXTO).grid(row=4, column=0, sticky="w", padx=10, pady=(10,0))
        
        self.scroll_ilus = ctk.CTkScrollableFrame(self.grid_frame, height=150, fg_color="white", border_color=self.COLOR_BOTON, border_width=1, label_text="Seleccione:")
        self.scroll_ilus.grid(row=5, column=0, sticky="ew", padx=10, pady=5)
        
        self.checks = []
        opciones = ["A - Ilustraciones", "B - Mapa", "C - Retratos", "D - Fotografías", "E - Planos", "M - Gráficas", "N - Tablas", "Z - Otros"] # (Lista resumida por brevedad)
        for op in opciones:
            chk = ctk.CTkCheckBox(self.scroll_ilus, text=op, text_color="black", fg_color=self.COLOR_BOTON)
            chk.pack(anchor="w", pady=2)
            self.checks.append(chk)

        # Idioma
        f_idioma = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        f_idioma.grid(row=4, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(f_idioma, text="Idioma", font=("Georgia", 12, "bold"), text_color=self.COLOR_TEXTO).pack(anchor="w")
        self.entry_idioma = ctk.CTkEntry(f_idioma, fg_color="white", text_color="black", border_color=self.COLOR_BOTON)
        self.entry_idioma.pack(fill="x")
        self.entry_idioma.insert(0, "Español")

    def validar(self):
        # 1. Validar Ficha
        ok, msg = self.validar_vacio(self.entry_ficha, "Ficha No.")
        if not ok: return False, msg
        
        # 2. Validar Clasificación
        ok, msg = self.validar_vacio(self.entry_clasif, "Clasificación")
        if not ok: return False, msg
        
        return True, ""

    def obtener_datos(self):
        # Procesar checkboxes
        codigos = [chk.cget("text").split(" - ")[0] for chk in self.checks if chk.get() == 1]
        return {
            "ficha_no": self.entry_ficha.get(),
            "isbn": self.entry_isbn.get(),
            "clasificacion": self.entry_clasif.get(),
            "codigo_ilustracion": ",".join(codigos),
            "idioma": self.entry_idioma.get()
        }
    
    def limpiar(self):
        self.limpiar_campos()
        for chk in self.checks: chk.deselect()
        self.entry_idioma.delete(0, 'end')
        self.entry_idioma.insert(0, "Español")

# --- PASO 2: AUTORÍA ---
class Paso2(PasoBase):
    def __init__(self, master):
        super().__init__(master, "2. Autoría y Título")
        self.entry_autor = self.crear_input("Autor Personal (Principal) *", 0, 0, 2)
        self.entry_corp = self.crear_input("Autor Corporativo", 2, 0, 2)
        self.entry_titulo = self.crear_input("Título / Mención *", 4, 0, 2)
        self.entry_asientos = self.crear_input("Asientos Secundarios", 6, 0, 2)

    def validar(self):
        ok, msg = self.validar_vacio(self.entry_autor, "Autor Personal")
        if not ok: return False, msg
        
        ok, msg = self.validar_vacio(self.entry_titulo, "Título")
        if not ok: return False, msg
        
        return True, ""

    def obtener_datos(self):
        return {
            "autor_nombre": self.entry_autor.get(),
            "autor_corporativo": self.entry_corp.get(),
            "titulo": self.entry_titulo.get(),
            "asientos_secundarios": self.entry_asientos.get()
        }

# --- PASO 3: PUBLICACIÓN (CON VALIDACIONES NUMÉRICAS) ---
class Paso3(PasoBase):
    def __init__(self, master):
        super().__init__(master, "3. Edición, Publicación y Descripción")
        self.entry_edicion = self.crear_input("Edición", 0, 0)
        self.entry_anio = self.crear_input("Año Publicación", 0, 1)
        self.entry_lugar = self.crear_input("Lugar", 2, 0)
        self.entry_editorial = self.crear_input("Editorial", 2, 1)
        self.entry_paginas = self.crear_input("Páginas (Núm)", 4, 0)
        self.entry_dimensiones = self.crear_input("Dimensiones", 4, 1)
        self.entry_serie = self.crear_input("Serie", 6, 0, 2)
        self.entry_desc = self.crear_input("Notas Generales", 8, 0, 2)

    def validar(self):
        # 1. Validar Año (Numérico y Lógico)
        anio = self.entry_anio.get().strip()
        if anio:
            if not anio.isdigit():
                self.entry_anio.configure(border_color="red")
                return False, "El Año debe ser numérico."
            if len(anio) != 4 or int(anio) > datetime.now().year + 1:
                self.entry_anio.configure(border_color="red")
                return False, "Año no válido."
        self.entry_anio.configure(border_color=self.COLOR_BOTON)

        # 2. Validar Páginas (Numérico)
        ok, msg = self.validar_numero(self.entry_paginas, "Páginas")
        if not ok: return False, msg

        return True, ""

    def obtener_datos(self):
        return {
            "edicion": self.entry_edicion.get(),
            "anio": self.entry_anio.get(),
            "lugar_publicacion": self.entry_lugar.get(),
            "editorial_nombre": self.entry_editorial.get(),
            "paginas": self.entry_paginas.get(),
            "dimensiones": self.entry_dimensiones.get(),
            "serie": self.entry_serie.get(),
            "descripcion": self.entry_desc.get()
        }

# --- PASO 4: EJEMPLARES ---
class Paso4(PasoBase):
    def __init__(self, master):
        super().__init__(master, "4. Ejemplares y Auditoría")
        self.entry_ubicacion = self.crear_input("Ubicación", 0, 0)
        self.entry_ubicacion.insert(0, "General")
        
        self.entry_copia = self.crear_input("Ejemplar (Núm)", 0, 1)
        self.entry_copia.insert(0, "1")
        
        self.entry_tomo = self.crear_input("Tomo", 4, 0)
        self.entry_volumen = self.crear_input("Volumen", 4, 1)

    def validar(self):
        # Validar que copia sea numero
        ok, msg = self.validar_numero(self.entry_copia, "Número de Copia")
        if not ok: return False, msg
        
        return True, ""

    def obtener_datos(self):
        # Formatear "Copia X" si solo ponen el numero
        copia = self.entry_copia.get()
        if copia.isdigit():
            copia = f"Copia {copia}"
            
        return {
            "ubicacion": self.entry_ubicacion.get(),
            "numero_copia": copia,
            "tomo": self.entry_tomo.get(),
            "volumen": self.entry_volumen.get()
        }
    
    def limpiar(self):
        self.limpiar_campos()
        self.entry_ubicacion.insert(0, "General")
        self.entry_copia.insert(0, "1")