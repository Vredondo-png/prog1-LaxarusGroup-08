import tkinter as tk
from tkinter import ttk

class VentanaInteractiva:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurador de Ventana")
        self.root.geometry("500x650")
        
        # Variables de configuración
        self.dimension_var = tk.StringVar(value="500x650")
        self.ancho_var = tk.IntVar(value=500)
        self.alto_var = tk.IntVar(value=650)
        self.pos_x_var = tk.IntVar(value=100)
        self.pos_y_var = tk.IntVar(value=100)
        self.centrar_var = tk.BooleanVar(value=False)
        self.redimensionable_var = tk.BooleanVar(value=True)
        self.pantalla_completa_var = tk.BooleanVar(value=False)
        self.siempre_visible_var = tk.BooleanVar(value=False)
        self.tema_var = tk.StringVar(value="claro")
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Canvas con scrollbar
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # Frame scrollable
        self.frame_scrollable = ttk.Frame(self.canvas)
        
        self.frame_scrollable.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # SECCIÓN: Dimensiones
        frame_dim = ttk.LabelFrame(self.frame_scrollable, text="📐 Dimensiones", padding=15)
        frame_dim.pack(fill=tk.X, padx=20, pady=10)
        
        dimensiones = [
            "500x650",
            "800x600",
            "1024x768",
            "1280x720",
            "1280x1024",
            "1366x768",
            "1920x1080",
            "Personalizado"
        ]
        
        ttk.Label(frame_dim, text="Tamaño:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_dim = ttk.Combobox(frame_dim, textvariable=self.dimension_var, 
                                      values=dimensiones, state="readonly", width=25)
        self.combo_dim.grid(row=0, column=1, pady=5, sticky="w", padx=10)
        self.combo_dim.bind("<<ComboboxSelected>>", self.cambiar_dimension)
        
        ttk.Label(frame_dim, text="Ancho (px):").grid(row=1, column=0, sticky="w", pady=5)
        self.ancho_spin = ttk.Spinbox(frame_dim, from_=400, to=2000, textvariable=self.ancho_var, 
                                      width=23, state="disabled", command=self.aplicar_dimension_personalizada)
        self.ancho_spin.grid(row=1, column=1, pady=5, sticky="w", padx=10)
        
        ttk.Label(frame_dim, text="Alto (px):").grid(row=2, column=0, sticky="w", pady=5)
        self.alto_spin = ttk.Spinbox(frame_dim, from_=300, to=1500, textvariable=self.alto_var, 
                                     width=23, state="disabled", command=self.aplicar_dimension_personalizada)
        self.alto_spin.grid(row=2, column=1, pady=5, sticky="w", padx=10)
        
        # SECCIÓN: Posición
        frame_pos = ttk.LabelFrame(self.frame_scrollable, text="📍 Posición", padding=15)
        frame_pos.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Checkbutton(frame_pos, text="Centrar ventana en pantalla", 
                       variable=self.centrar_var, 
                       command=self.toggle_centrar).pack(anchor="w", pady=5)
        
        pos_frame = ttk.Frame(frame_pos)
        pos_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pos_frame, text="Posición X:").grid(row=0, column=0, sticky="w", pady=5)
        self.pos_x_spin = ttk.Spinbox(pos_frame, from_=0, to=2000, textvariable=self.pos_x_var, 
                                      width=23, command=self.aplicar_posicion)
        self.pos_x_spin.grid(row=0, column=1, pady=5, sticky="w", padx=10)
        
        ttk.Label(pos_frame, text="Posición Y:").grid(row=1, column=0, sticky="w", pady=5)
        self.pos_y_spin = ttk.Spinbox(pos_frame, from_=0, to=1500, textvariable=self.pos_y_var, 
                                      width=23, command=self.aplicar_posicion)
        self.pos_y_spin.grid(row=1, column=1, pady=5, sticky="w", padx=10)
        
        # SECCIÓN: Propiedades
        frame_props = ttk.LabelFrame(self.frame_scrollable, text="🎯 Propiedades", padding=15)
        frame_props.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Checkbutton(frame_props, text="Permitir redimensionar", 
                       variable=self.redimensionable_var,
                       command=self.toggle_redimensionable).pack(anchor="w", pady=3)
        
        ttk.Checkbutton(frame_props, text="Modo pantalla completa", 
                       variable=self.pantalla_completa_var,
                       command=self.toggle_fullscreen).pack(anchor="w", pady=3)
        
        ttk.Checkbutton(frame_props, text="Siempre visible (topmost)", 
                       variable=self.siempre_visible_var,
                       command=self.toggle_topmost).pack(anchor="w", pady=3)
        
        # SECCIÓN: Apariencia
        frame_aparien = ttk.LabelFrame(self.frame_scrollable, text="🎨 Apariencia", padding=15)
        frame_aparien.pack(fill=tk.X, padx=20, pady=10)
        
        tema_frame = ttk.Frame(frame_aparien)
        tema_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(tema_frame, text="Tema:").pack(side=tk.LEFT)
        combo_tema = ttk.Combobox(tema_frame, textvariable=self.tema_var, 
                                  values=["claro", "oscuro"], 
                                  state="readonly", width=20)
        combo_tema.pack(side=tk.LEFT, padx=10)
        combo_tema.bind("<<ComboboxSelected>>", self.cambiar_tema)
        
        # Espaciado final
        ttk.Frame(self.frame_scrollable, height=20).pack()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar que el frame interno se expanda con la ventana
        self.canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _on_canvas_configure(self, event):
        # Ajustar el ancho del frame interno al ancho del canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.frame_scrollable, anchor="nw"), width=canvas_width)
        
        # Aplicar estado inicial
        self.toggle_centrar()
        self.cambiar_tema()
        
        # Bind para scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Bind para ESC
        self.root.bind("<Escape>", lambda e: self.pantalla_completa_var.set(False) or self.toggle_fullscreen())
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def cambiar_dimension(self, event=None):
        seleccion = self.dimension_var.get()
        
        if seleccion == "Personalizado":
            self.ancho_spin.config(state="normal")
            self.alto_spin.config(state="normal")
        else:
            self.ancho_spin.config(state="disabled")
            self.alto_spin.config(state="disabled")
            ancho, alto = seleccion.split('x')
            self.ancho_var.set(int(ancho))
            self.alto_var.set(int(alto))
            self.aplicar_dimension()
    
    def aplicar_dimension(self):
        ancho = self.ancho_var.get()
        alto = self.alto_var.get()
        if self.centrar_var.get():
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - ancho) // 2
            y = (screen_height - alto) // 2
            self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        else:
            x = self.pos_x_var.get()
            y = self.pos_y_var.get()
            self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def aplicar_dimension_personalizada(self):
        self.aplicar_dimension()
    
    def toggle_centrar(self):
        if self.centrar_var.get():
            self.pos_x_spin.config(state="disabled")
            self.pos_y_spin.config(state="disabled")
            # Centrar ventana
            ancho = self.ancho_var.get()
            alto = self.alto_var.get()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - ancho) // 2
            y = (screen_height - alto) // 2
            self.root.geometry(f"+{x}+{y}")
        else:
            self.pos_x_spin.config(state="normal")
            self.pos_y_spin.config(state="normal")
    
    def aplicar_posicion(self):
        if not self.centrar_var.get():
            x = self.pos_x_var.get()
            y = self.pos_y_var.get()
            self.root.geometry(f"+{x}+{y}")
    
    def toggle_redimensionable(self):
        resizable = self.redimensionable_var.get()
        self.root.resizable(resizable, resizable)
    
    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', self.pantalla_completa_var.get())
    
    def toggle_topmost(self):
        self.root.attributes('-topmost', self.siempre_visible_var.get())
    
    def cambiar_tema(self, event=None):
        tema = self.tema_var.get()
        if tema == "oscuro":
            self.root.configure(bg="#2c3e50")
            self.canvas.configure(bg="#2c3e50")
            self.frame_scrollable.configure(style="Dark.TFrame")
            
            # Crear estilo oscuro si no existe
            style = ttk.Style()
            style.configure("Dark.TFrame", background="#2c3e50")
            style.configure("Dark.TLabelframe", background="#34495e", foreground="white")
            style.configure("Dark.TLabelframe.Label", background="#34495e", foreground="white")
        else:
            self.root.configure(bg="#f0f0f0")
            self.canvas.configure(bg="#f0f0f0")
            self.frame_scrollable.configure(style="TFrame")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInteractiva(root)
    root.mainloop()