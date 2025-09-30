import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import os

class ConfiguracionVentana:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("500x650")
        
        # Centrar ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 650) // 2
        self.root.geometry(f"500x650+{x}+{y}")
        
        # Variables para arrastrar ventana
        self.x_ventana = 0
        self.y_ventana = 0
        
        # Variables de configuración
        self.titulo_var = tk.StringVar(value="Mi Aplicación")
        self.ancho_var = tk.IntVar(value=800)
        self.alto_var = tk.IntVar(value=600)
        self.dimension_var = tk.StringVar(value="800x600")
        self.pos_x_var = tk.IntVar(value=100)
        self.pos_y_var = tk.IntVar(value=100)
        self.centrar_var = tk.BooleanVar(value=True)
        self.redimensionable_var = tk.BooleanVar(value=True)
        self.pantalla_completa_var = tk.BooleanVar(value=False)
        self.siempre_visible_var = tk.BooleanVar(value=False)
        self.color_fondo_var = tk.StringVar(value="#f0f0f0")
        self.tema_var = tk.StringVar(value="claro")
        
        self.crear_interfaz()
        self.cargar_configuracion()
        
    def crear_interfaz(self):
        # Título
        frame_titulo = tk.Frame(self.root, bg="#2c3e50", height=60, cursor="hand2")
        frame_titulo.pack(fill=tk.X)
        frame_titulo.pack_propagate(False)
        
        # Hacer el título arrastrable
        frame_titulo.bind("<Button-1>", self.iniciar_arrastre)
        frame_titulo.bind("<B1-Motion>", self.arrastrar_ventana)
        
        titulo_label = tk.Label(frame_titulo, text="⚙️ Configuración de Ventana", 
                font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        titulo_label.pack(side=tk.LEFT, pady=15, padx=20)
        titulo_label.bind("<Button-1>", self.iniciar_arrastre)
        titulo_label.bind("<B1-Motion>", self.arrastrar_ventana)
        
        # Botón cerrar
        btn_cerrar = tk.Label(frame_titulo, text="✕", font=("Arial", 18, "bold"),
                             bg="#2c3e50", fg="white", cursor="hand2")
        btn_cerrar.pack(side=tk.RIGHT, padx=15)
        btn_cerrar.bind("<Button-1>", lambda e: self.root.destroy())
        
        # Frame principal con scroll
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame_scrollable = tk.Frame(canvas)
        
        frame_scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # SECCIÓN: Dimensiones
        frame_dim = tk.LabelFrame(frame_scrollable, text="📐 Dimensiones", 
                                 font=("Arial", 10, "bold"), padx=15, pady=10)
        frame_dim.pack(fill=tk.X, padx=20, pady=10)
        
        # Opciones predefinidas
        dimensiones = [
            "800x600",
            "1024x768",
            "1280x720",
            "1280x1024",
            "1366x768",
            "1920x1080",
            "Personalizado"
        ]
        
        self.dimension_var = tk.StringVar(value="800x600")
        
        tk.Label(frame_dim, text="Tamaño:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_dim = ttk.Combobox(frame_dim, textvariable=self.dimension_var, 
                                      values=dimensiones, state="readonly", width=20)
        self.combo_dim.grid(row=0, column=1, pady=5, sticky="w")
        self.combo_dim.bind("<<ComboboxSelected>>", self.cambiar_dimension)
        
        # Campos personalizados (deshabilitados por defecto)
        tk.Label(frame_dim, text="Ancho (px):").grid(row=1, column=0, sticky="w", pady=5)
        self.ancho_spin = tk.Spinbox(frame_dim, from_=400, to=2000, textvariable=self.ancho_var, 
                  width=15, state="disabled")
        self.ancho_spin.grid(row=1, column=1, pady=5, sticky="w")
        
        tk.Label(frame_dim, text="Alto (px):").grid(row=2, column=0, sticky="w", pady=5)
        self.alto_spin = tk.Spinbox(frame_dim, from_=300, to=1500, textvariable=self.alto_var, 
                  width=15, state="disabled")
        self.alto_spin.grid(row=2, column=1, pady=5, sticky="w")
        
        # SECCIÓN: Posición
        frame_pos = tk.LabelFrame(frame_scrollable, text="📍 Posición", 
                                 font=("Arial", 10, "bold"), padx=15, pady=10)
        frame_pos.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Checkbutton(frame_pos, text="Centrar ventana en pantalla", 
                      variable=self.centrar_var, command=self.toggle_posicion).grid(row=0, column=0, 
                                                                                     columnspan=2, sticky="w", pady=5)
        
        tk.Label(frame_pos, text="Posición X:").grid(row=1, column=0, sticky="w", pady=5)
        self.pos_x_spin = tk.Spinbox(frame_pos, from_=0, to=2000, textvariable=self.pos_x_var, width=15)
        self.pos_x_spin.grid(row=1, column=1, pady=5, sticky="w")
        
        tk.Label(frame_pos, text="Posición Y:").grid(row=2, column=0, sticky="w", pady=5)
        self.pos_y_spin = tk.Spinbox(frame_pos, from_=0, to=1500, textvariable=self.pos_y_var, width=15)
        self.pos_y_spin.grid(row=2, column=1, pady=5, sticky="w")
        
        # SECCIÓN: Propiedades
        frame_props = tk.LabelFrame(frame_scrollable, text="🎯 Propiedades", 
                                   font=("Arial", 10, "bold"), padx=15, pady=10)
        frame_props.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Checkbutton(frame_props, text="Permitir redimensionar", 
                      variable=self.redimensionable_var).grid(row=0, column=0, sticky="w", pady=3)
        
        tk.Checkbutton(frame_props, text="Modo pantalla completa", 
                      variable=self.pantalla_completa_var).grid(row=1, column=0, sticky="w", pady=3)
        
        tk.Checkbutton(frame_props, text="Siempre visible (topmost)", 
                      variable=self.siempre_visible_var).grid(row=2, column=0, sticky="w", pady=3)
        
        # SECCIÓN: Apariencia
        frame_aparien = tk.LabelFrame(frame_scrollable, text="🎨 Apariencia", 
                                     font=("Arial", 10, "bold"), padx=15, pady=10)
        frame_aparien.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_aparien, text="Color de fondo:").grid(row=0, column=0, sticky="w", pady=5)
        frame_color = tk.Frame(frame_aparien)
        frame_color.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Entry(frame_color, textvariable=self.color_fondo_var, width=15).pack(side=tk.LEFT)
        tk.Button(frame_color, text="🎨", command=self.elegir_color, width=3).pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_aparien, text="Tema:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(frame_aparien, textvariable=self.tema_var, 
                    values=["claro", "oscuro", "sistema"], 
                    state="readonly", width=15).grid(row=1, column=1, sticky="w", pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones de acción
        frame_botones = tk.Frame(self.root, bg="#ecf0f1", height=70)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM)
        frame_botones.pack_propagate(False)
        
        tk.Button(frame_botones, text="💾 Guardar", command=self.guardar_configuracion,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                 width=12).pack(side=tk.LEFT, padx=10, pady=15)
        
        tk.Button(frame_botones, text="👁️ Vista Previa", command=self.vista_previa,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                 width=12).pack(side=tk.LEFT, padx=5, pady=15)
        
        tk.Button(frame_botones, text="🔄 Restablecer", command=self.restablecer,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                 width=12).pack(side=tk.LEFT, padx=5, pady=15)
        
        # Inicializar estado de posición
        self.toggle_posicion()
        
    def cambiar_dimension(self, event=None):
        seleccion = self.dimension_var.get()
        
        if seleccion == "Personalizado":
            self.ancho_spin.config(state="normal")
            self.alto_spin.config(state="normal")
        else:
            self.ancho_spin.config(state="disabled")
            self.alto_spin.config(state="disabled")
            # Aplicar dimensión predefinida
            ancho, alto = seleccion.split('x')
            self.ancho_var.set(int(ancho))
            self.alto_var.set(int(alto))
    
    def toggle_posicion(self):
        if self.centrar_var.get():
            self.pos_x_spin.config(state="disabled")
            self.pos_y_spin.config(state="disabled")
        else:
            self.pos_x_spin.config(state="normal")
            self.pos_y_spin.config(state="normal")
            
    def elegir_color(self):
        color = colorchooser.askcolor(title="Elegir color de fondo")
        if color[1]:
            self.color_fondo_var.set(color[1])
            
    def guardar_configuracion(self):
        config = {
            "titulo": self.titulo_var.get(),
            "dimension": self.dimension_var.get(),
            "ancho": self.ancho_var.get(),
            "alto": self.alto_var.get(),
            "pos_x": self.pos_x_var.get(),
            "pos_y": self.pos_y_var.get(),
            "centrar": self.centrar_var.get(),
            "redimensionable": self.redimensionable_var.get(),
            "pantalla_completa": self.pantalla_completa_var.get(),
            "siempre_visible": self.siempre_visible_var.get(),
            "color_fondo": self.color_fondo_var.get(),
            "tema": self.tema_var.get()
        }
        
        try:
            with open("config_ventana.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("✓ Éxito", "Configuración guardada correctamente")
        except Exception as e:
            messagebox.showerror("✗ Error", f"Error al guardar: {e}")
            
    def cargar_configuracion(self):
        if os.path.exists("config_ventana.json"):
            try:
                with open("config_ventana.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                    
                self.titulo_var.set(config.get("titulo", "Mi Aplicación"))
                self.dimension_var.set(config.get("dimension", "800x600"))
                self.ancho_var.set(config.get("ancho", 800))
                self.alto_var.set(config.get("alto", 600))
                self.cambiar_dimension()
                self.pos_x_var.set(config.get("pos_x", 100))
                self.pos_y_var.set(config.get("pos_y", 100))
                self.centrar_var.set(config.get("centrar", True))
                self.redimensionable_var.set(config.get("redimensionable", True))
                self.pantalla_completa_var.set(config.get("pantalla_completa", False))
                self.siempre_visible_var.set(config.get("siempre_visible", False))
                self.color_fondo_var.set(config.get("color_fondo", "#f0f0f0"))
                self.tema_var.set(config.get("tema", "claro"))
                
                self.toggle_posicion()
            except:
                pass
                
    def restablecer(self):
        if messagebox.askyesno("Confirmar", "¿Restablecer a valores predeterminados?"):
            self.titulo_var.set("Mi Aplicación")
            self.ancho_var.set(800)
            self.alto_var.set(600)
            self.pos_x_var.set(100)
            self.pos_y_var.set(100)
            self.centrar_var.set(True)
            self.redimensionable_var.set(True)
            self.pantalla_completa_var.set(False)
            self.siempre_visible_var.set(False)
            self.color_fondo_var.set("#f0f0f0")
            self.tema_var.set("claro")
            self.toggle_posicion()
            
    def vista_previa(self):
        preview = tk.Toplevel(self.root)
        preview.title(self.titulo_var.get())
        
        ancho = self.ancho_var.get()
        alto = self.alto_var.get()
        
        if self.centrar_var.get():
            # Centrar en pantalla
            screen_width = preview.winfo_screenwidth()
            screen_height = preview.winfo_screenheight()
            x = (screen_width - ancho) // 2
            y = (screen_height - alto) // 2
        else:
            x = self.pos_x_var.get()
            y = self.pos_y_var.get()
            
        preview.geometry(f"{ancho}x{alto}+{x}+{y}")
        preview.configure(bg=self.color_fondo_var.get())
        preview.resizable(self.redimensionable_var.get(), self.redimensionable_var.get())
        preview.attributes('-topmost', self.siempre_visible_var.get())
        
        if self.pantalla_completa_var.get():
            preview.attributes('-fullscreen', True)
            
        # Contenido de ejemplo
        tk.Label(preview, text="✓ Vista Previa", font=("Arial", 20, "bold"),
                bg=self.color_fondo_var.get()).pack(pady=40)
        
        tk.Label(preview, text=f"Título: {self.titulo_var.get()}", 
                font=("Arial", 12), bg=self.color_fondo_var.get()).pack(pady=10)
        
        tk.Label(preview, text=f"Dimensiones: {ancho}x{alto}", 
                font=("Arial", 12), bg=self.color_fondo_var.get()).pack(pady=5)
        
        tk.Label(preview, text=f"Tema: {self.tema_var.get()}", 
                font=("Arial", 12), bg=self.color_fondo_var.get()).pack(pady=5)
        
        tk.Button(preview, text="Cerrar", command=preview.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(pady=30)
    
    def iniciar_arrastre(self, event):
        self.x_ventana = event.x
        self.y_ventana = event.y
    
    def arrastrar_ventana(self, event):
        x = self.root.winfo_x() + event.x - self.x_ventana
        y = self.root.winfo_y() + event.y - self.y_ventana
        self.root.geometry(f"+{x}+{y}")
        
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ConfiguracionVentana()
    app.ejecutar()