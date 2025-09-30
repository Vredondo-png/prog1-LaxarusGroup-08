import tkinter as tk
from tkinter import ttk, messagebox

# Datos de bancos y ubicaciones
bancos = [
    "Banco Santander",
    "Banco Galicia",
    "Banco Nación",
    "Banco Macro",
    "BBVA",
    "Banco Ciudad"
]

ubicaciones = {
    "Banco Santander": ["Palermo", "Recoleta", "Belgrano", "San Telmo", "Puerto Madero"],
    "Banco Galicia": ["Palermo,Buenos Aires", "Villa Crespo", "Caballito", "Flores", "Núñez"],
    "Banco Nación": ["Microcentro", "Once", "Barracas", "La Boca", "Constitución"],
    "Banco Macro": ["Almagro", "Balvanera", "Parque Patricios", "Boedo", "Villa Urquiza"],
    "BBVA": ["Retiro", "San Nicolás", "Montserrat", "Villa Devoto", "Colegiales"],
    "Banco Ciudad": ["Centro", "Barrio Norte", "Villa Crespo", "Chacarita", "Agronomía"]
}

def cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var):
    if operacion_var.get() == "depositar":
        ubicacion_label.grid_remove()
        ubicacion_combo.grid_remove()
    else:
        ubicacion_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        ubicacion_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        actualizar_ubicaciones(None, ubicacion_combo, banco_var, ubicacion_var)

def actualizar_ubicaciones(event, ubicacion_combo, banco_var, ubicacion_var):
    banco_seleccionado = banco_var.get()
    if banco_seleccionado:
        if banco_seleccionado in ubicaciones:
            ubicacion_combo.config(values=ubicaciones[banco_seleccionado])
            ubicacion_var.set("")
        else:
            ubicacion_combo.config(values=[])
            ubicacion_var.set("")
    else:
        ubicacion_combo.config(values=[])
        ubicacion_var.set("")

def es_numero_valido(texto):
    if texto == "":
        return False
    
    # Verificar si contiene solo dígitos y puntos/comas
    caracteres_validos = "0123456789.,"
    for caracter in texto:
        if caracter in caracteres_validos:
            continue
        else:
            return False
    return True

def procesar_operacion(monto_var, operacion_var, banco_var, ubicacion_var, resultado_text):
    # Validar monto
    monto_texto = monto_var.get()
    if es_numero_valido(monto_texto)> 25000000:
        messagebox.showerror("Error", "Ingrese una cantidad de dinero que tenga")
        return
    
    monto = float(monto_texto.replace(',', '.'))
    if monto <= 0:
        messagebox.showerror("Error", "El monto debe ser mayor a 0")
        return
    
    # Validar banco
    if banco_var.get() == "":
        messagebox.showerror("Error", "Seleccione un banco")
        return
    
    # Validar ubicación para retiros
    if operacion_var.get() == "retirar":
        if ubicacion_var.get() == "":
            messagebox.showerror("Error", "Seleccione una ubicación para el retiro")
            return
    
    # Generar resumen
    resultado_text.delete(1.0, tk.END)
    
    if operacion_var.get() == "depositar":
        operacion = "DEPÓSITO"
    else:
        operacion = "RETIRO"
    
    resultado = "=== " + operacion + " PROCESADO ===\n\n"
    resultado += "Monto: $" + str(monto) + "\n"
    resultado += "Banco: " + banco_var.get() + "\n"
    
    if operacion_var.get() == "retirar":
        resultado += "Ubicación: " + ubicacion_var.get() + "\n"
    
    resultado += "\nOperación realizada exitosamente.\n"
    
    if operacion_var.get() == "depositar":
        resultado += "El dinero ha sido depositado en " + banco_var.get() + "."
    else:
        resultado += "Puede retirar el dinero en " + banco_var.get() + " - " + ubicacion_var.get() + "."
    
    resultado_text.insert(1.0, resultado)
    messagebox.showinfo("Éxito", operacion + " procesado correctamente")

def limpiar_campos(monto_var, banco_var, ubicacion_var, operacion_var, resultado_text, ubicacion_label, ubicacion_combo):
    monto_var.set("")
    banco_var.set("")
    ubicacion_var.set("")
    operacion_var.set("depositar")
    resultado_text.delete(1.0, tk.END)
    cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var)

def ejecutar_aplicacion():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Depositar y Retirar")
    root.geometry("500x400")
    root.resizable(False, False)
    
    # Frame principal
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Título
    title_label = ttk.Label(main_frame, text="Sistema de Depósitos y Retiros", 
                           font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Variables
    monto_var = tk.StringVar()
    operacion_var = tk.StringVar(value="depositar")
    banco_var = tk.StringVar()
    ubicacion_var = tk.StringVar()
    
    # Monto
    ttk.Label(main_frame, text="Monto ($):", font=("Arial", 10, "bold")).grid(
        row=1, column=0, sticky=tk.W, pady=5)
    monto_entry = ttk.Entry(main_frame, textvariable=monto_var, width=20)
    monto_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    # Tipo de operación
    ttk.Label(main_frame, text="Operación:", font=("Arial", 10, "bold")).grid(
        row=2, column=0, sticky=tk.W, pady=5)
    
    # Frame para los radiobuttons
    radio_frame = ttk.Frame(main_frame)
    radio_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    # Crear elementos de ubicación
    ubicacion_label = ttk.Label(main_frame, text="Ubicación:", font=("Arial", 10, "bold"))
    ubicacion_combo = ttk.Combobox(main_frame, textvariable=ubicacion_var, 
                                  state="readonly", width=18)
    
    # Radiobuttons
    ttk.Radiobutton(radio_frame, text="Depositar", variable=operacion_var, 
                   value="depositar", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var)).pack(side=tk.LEFT)
    ttk.Radiobutton(radio_frame, text="Retirar", variable=operacion_var, 
                   value="retirar", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var)).pack(side=tk.LEFT, padx=(20, 0))
    
    # Banco
    ttk.Label(main_frame, text="Banco:", font=("Arial", 10, "bold")).grid(
        row=3, column=0, sticky=tk.W, pady=5)
    banco_combo = ttk.Combobox(main_frame, textvariable=banco_var, 
                               values=bancos, state="readonly", width=18)
    banco_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    banco_combo.bind("<<ComboboxSelected>>", lambda event: actualizar_ubicaciones(event, ubicacion_combo, banco_var, ubicacion_var))
    
    # Frame para resultado
    resultado_frame = ttk.LabelFrame(main_frame, text="Resumen de la operación", 
                                    padding="10")
    resultado_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))
    
    resultado_text = tk.Text(resultado_frame, height=6, width=50, wrap=tk.WORD)
    resultado_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    # Scrollbar para el texto
    scrollbar = ttk.Scrollbar(resultado_frame, orient=tk.VERTICAL, 
                             command=resultado_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    resultado_text.config(yscrollcommand=scrollbar.set)
    
    # Botones
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=6, column=0, columnspan=2, pady=10)
    
    ttk.Button(button_frame, text="Procesar", 
               command=lambda: procesar_operacion(monto_var, operacion_var, banco_var, ubicacion_var, resultado_text)).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Limpiar", 
               command=lambda: limpiar_campos(monto_var, banco_var, ubicacion_var, operacion_var, resultado_text, ubicacion_label, ubicacion_combo)).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Salir", command=root.quit).pack(side=tk.LEFT, padx=5)
    
    # Configurar el cambio inicial
    cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var)
    
    root.mainloop()
    
    
    
    
if __name__ == "__main__":
    ejecutar_aplicacion()