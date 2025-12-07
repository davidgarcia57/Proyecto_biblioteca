import customtkinter as ctk
from tkinter import ttk, messagebox

class PopupFicha(ctk.CTkToplevel):
    def __init__(self, master, data, callback_baja, callback_guardar_cambios):
        super().__init__(master)
        self.title("Detalle y Gestión de la Obra")
        self.geometry("900x720")
        self.callback_baja = callback_baja
        self.callback_guardar = callback_guardar_cambios
        
        # Hacemos la ventana modal
        self.grab_set()
        self.focus_force()

        self.obra = data.get('obra', {})
        self.ejemplares = data.get('ejemplares', [])
        
        self.editando = False
        self.entries = {} 

        # --- HEADER ---
        self.frm_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_header.pack(fill="x", padx=20, pady=(20,5))
        
        # Título
        self.entries['titulo'] = ctk.CTkEntry(self.frm_header, font=("Georgia", 20, "bold"), 
                                              # Al inicio usamos el color del fondo para que parezca Label
                                              fg_color=self.cget("fg_color"), 
                                              border_width=0, width=600)
        self.entries['titulo'].insert(0, self.obra.get('titulo', 'Sin Título'))
        self.entries['titulo'].configure(state="disabled")
        self.entries['titulo'].pack(side="left")

        # --- GRID DE DATOS ---
        frm_datos = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        frm_datos.pack(fill="x", padx=20, pady=10)

        campos = [
            ("ISBN:", 'isbn', 0, 0),
            ("Clasificación:", 'clasificacion', 0, 1),
            ("Idioma:", 'idioma', 0, 2),
            ("Editorial:", 'editorial', 1, 0), 
            ("Año:", 'anio', 1, 1),
            ("Edición:", 'edicion', 1, 2),
            ("Páginas:", 'paginas', 2, 0),
            ("Dimensiones:", 'dimensiones', 2, 1),
            ("Serie:", 'serie', 2, 2)
        ]

        for lbl, key, r, c in campos:
            ctk.CTkLabel(frm_datos, text=lbl, font=("Arial", 12, "bold"), text_color="#A7744A").grid(row=r*2, column=c, sticky="w", padx=15, pady=(10,0))
            
            val = str(self.obra.get(key, '') or '')
            
            # CORRECCIÓN: Insertar en estado normal, luego deshabilitar
            entry = ctk.CTkEntry(frm_datos, font=("Arial", 12), fg_color="#F9F9F9", border_color="#D0D0D0")
            entry.insert(0, val)
            entry.configure(state="disabled")
            entry.grid(row=r*2+1, column=c, sticky="ew", padx=15, pady=(0,10))
            
            # CORRECCIÓN: Agregamos 'editorial' a las entries para que se desbloquee también
            # (Aunque nota: cambiar el texto aquí no cambiará el ID en la BD automáticamente sin lógica extra)
            if key != 'autor': 
                self.entries[key] = entry

        frm_datos.columnconfigure((0,1,2), weight=1)

        # --- SINOPSIS ---
        ctk.CTkLabel(self, text="Sinopsis / Descripción:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(10,0))
        self.txt_desc = ctk.CTkTextbox(self, height=80, fg_color="white", text_color="black")
        self.txt_desc.pack(fill="x", padx=20, pady=5)
        self.txt_desc.insert("0.0", self.obra.get('descripcion', '') or '')
        self.txt_desc.configure(state="disabled")

        # --- BOTÓN EDICIÓN ---
        frm_btns_edit = ctk.CTkFrame(self, fg_color="transparent")
        frm_btns_edit.pack(fill="x", padx=20, pady=5)
        self.btn_editar = ctk.CTkButton(frm_btns_edit, text="✏️ Modificar Datos", fg_color="#A7744A", command=self.toggle_edicion)
        self.btn_editar.pack(side="right")

        # --- TABLA COPIAS ---
        ctk.CTkLabel(self, text="Gestión de Copias Físicas:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15,5))
        frm_tabla = ctk.CTkFrame(self, fg_color="transparent")
        frm_tabla.pack(fill="both", expand=True, padx=20, pady=(0,20))

        self.tree = ttk.Treeview(frm_tabla, columns=("ID", "Copia", "Ubicación", "Estado"), show="headings", height=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Copia", text="Etiqueta")
        self.tree.heading("Ubicación", text="Ubicación Física")
        self.tree.heading("Estado", text="Estado Actual")
        self.tree.column("ID", width=50, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        for ej in self.ejemplares:
            self.tree.insert("", "end", values=(ej['id'], ej['copia'], ej['ubicacion'], ej['estado']))

        # Panel Baja
        frm_baja = ctk.CTkFrame(frm_tabla, fg_color="#F3E7D2", width=150)
        frm_baja.pack(side="right", fill="y", padx=(10,0))
        frm_baja.pack_propagate(False)
        ctk.CTkLabel(frm_baja, text="Zona de Baja", text_color="#D32F2F", font=("Arial", 12, "bold")).pack(pady=10)
        ctk.CTkButton(frm_baja, text="Quitar libro\nSeleccionado", fg_color="#D32F2F", hover_color="#B71C1C", height=50, command=self.evento_baja).pack(pady=10, padx=10)

    def toggle_edicion(self):
        self.editando = not self.editando
        
        nuevo_estado = "normal" if self.editando else "disabled"
        # CORRECCIÓN DEL ERROR DE CONSOLA: Usamos el color de fondo real, no "transparent"
        bg_color = self.cget("fg_color") 
        nuevo_color = "white" if self.editando else bg_color
        borde = 2 if self.editando else 0
        
        # Configurar Título
        self.entries['titulo'].configure(state=nuevo_estado, fg_color=nuevo_color, border_width=borde)
        
        # Configurar campos generales
        for k, entry in self.entries.items():
            if k == 'titulo': continue
            entry.configure(state=nuevo_estado, border_color="#A7744A" if self.editando else "#D0D0D0")
            
        self.txt_desc.configure(state=nuevo_estado)

        if self.editando:
            self.btn_editar.configure(text="💾 Guardar Cambios", fg_color="#2E7D32")
        else:
            self.btn_editar.configure(text="✏️ Modificar Datos", fg_color="#A7744A")
            self.recolectar_y_guardar()

    def recolectar_y_guardar(self):
        datos_nuevos = {
            'id_obra': self.obra.get('id_obra'),
            'titulo': self.entries['titulo'].get(),
            'isbn': self.entries['isbn'].get(),
            'clasificacion': self.entries['clasificacion'].get(),
            'idioma': self.entries['idioma'].get(),
            'anio': self.entries['anio'].get(),
            'edicion': self.entries['edicion'].get(),
            'paginas': self.entries['paginas'].get(),
            'dimensiones': self.entries['dimensiones'].get(),
            'serie': self.entries['serie'].get(),
            'descripcion': self.txt_desc.get("0.0", "end").strip()
        }
        
        if messagebox.askyesno("Confirmar", "¿Desea guardar los cambios realizados?"):
            self.callback_guardar(datos_nuevos)

    def evento_baja(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)
        self.callback_baja(item['values'][0], item['values'][3], item['values'][1])