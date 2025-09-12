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
    "Banco Santander": ["Palermo, Buenos Aires", "Recoleta, Buenos Aires", "Belgrano, Buenos Aires", "San Telmo, Buenos Aires", "Puerto Madero, Buenos Aires"],
    "Banco Galicia": ["Villa Crespo, Buenos Aires", "Caballito, Buenos Aires", "Flores, Buenos Aires", "Núñez, Buenos Aires", "Córdoba, Córdoba"],
    "Banco Nación": ["Microcentro, Buenos Aires", "Once, Buenos Aires", "Barracas, Buenos Aires", "La Boca, Buenos Aires", "Rosario, Santa Fe"],
    "Banco Macro": ["Almagro, Buenos Aires", "Balvanera, Buenos Aires", "Parque Patricios, Buenos Aires", "Boedo, Buenos Aires", "Mendoza, Mendoza"],
    "BBVA": ["Retiro, Buenos Aires", "San Nicolás, Buenos Aires", "Montserrat, Buenos Aires", "Villa Devoto, Buenos Aires", "Mar del Plata, Buenos Aires"],
    "Banco Ciudad": ["Centro, Buenos Aires", "Barrio Norte, Buenos Aires", "Villa Crespo, Buenos Aires", "Chacarita, Buenos Aires", "La Plata, Buenos Aires"]
}

def cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, banco_destino_label, banco_destino_combo, banco_destino_var, alias_label, alias_entry):
    if operacion_var.get() == "depositar":
        ubicacion_label.grid_remove()
        ubicacion_combo.grid_remove()
        banco_destino_label.grid_remove()
        banco_destino_combo.grid_remove()
        alias_label.grid_remove()
        alias_entry.grid_remove()
    elif operacion_var.get() == "retirar":
        ubicacion_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        ubicacion_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        banco_destino_label.grid_remove()
        banco_destino_combo.grid_remove()
        alias_label.grid_remove()
        alias_entry.grid_remove()
        actualizar_ubicaciones(None, ubicacion_combo, banco_var, ubicacion_var)
    else:  # transaccion
        ubicacion_label.grid_remove()
        ubicacion_combo.grid_remove()
        banco_destino_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        banco_destino_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        alias_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        alias_entry.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)

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
    
    caracteres_validos = "0123456789.,"
    for caracter in texto:
        if caracter in caracteres_validos:
            continue
        else:
            return False
    return True

def procesar_operacion(monto_var, operacion_var, banco_var, ubicacion_var, banco_destino_var, alias_var, resultado_text):
    monto_texto = monto_var.get()
    if not es_numero_valido(monto_texto):
        messagebox.showerror("Error", "Ingrese un monto válido")
        return
    
    monto = float(monto_texto.replace(',', '.'))
    if monto <= 0:
        messagebox.showerror("Error", "El monto debe ser mayor a 0")
        return
    
    if monto > 25000000:
        messagebox.showerror("Error", "Ingrese una cantidad de dinero que tenga")
        return
    
    if banco_var.get() == "":
        messagebox.showerror("Error", "Seleccione un banco")
        return
    
    if operacion_var.get() == "retirar":
        if ubicacion_var.get() == "":
            messagebox.showerror("Error", "Seleccione una ubicación para el retiro")
            return
    
    if operacion_var.get() == "transaccion":
        if banco_destino_var.get() == "":
            messagebox.showerror("Error", "Seleccione un banco de destino")
            return
        if banco_var.get() == banco_destino_var.get():
            messagebox.showerror("Error", "El banco origen y destino no pueden ser el mismo")
            return
        if monto < 20000:
            messagebox.showerror("Error", "El monto mínimo para transacciones es de $20.000")
            return
        if alias_var.get().strip() == "":
            messagebox.showerror("Error", "Ingrese el alias del destinatario")
            return
    
    resultado_text.delete(1.0, tk.END)
    
    if operacion_var.get() == "depositar":
        operacion = "DEPÓSITO"
    elif operacion_var.get() == "retirar":
        operacion = "RETIRO"
    else:
        operacion = "TRANSACCIÓN"
    
    resultado = "=== " + operacion + " PROCESADO ===\n\n"
    resultado += "Monto: $" + str(monto) + "\n"
    resultado += "Banco origen: " + banco_var.get() + "\n"
    
    if operacion_var.get() == "retirar":
        resultado += "Ubicación: " + ubicacion_var.get() + "\n"
    elif operacion_var.get() == "transaccion":
        resultado += "Banco destino: " + banco_destino_var.get() + "\n"
        resultado += "Alias destinatario: " + alias_var.get() + "\n"
    
    resultado += "\nOperación realizada exitosamente.\n"
    
    if operacion_var.get() == "depositar":
        resultado += "El dinero ha sido depositado en " + banco_var.get() + "."
    elif operacion_var.get() == "retirar":
        resultado += "Puede retirar el dinero en " + banco_var.get() + " - " + ubicacion_var.get() + "."
    else:
        resultado += "La transacción se realizó desde " + banco_var.get() + " hacia " + banco_destino_var.get() + " para " + alias_var.get() + "."
    
    resultado_text.insert(1.0, resultado)
    messagebox.showinfo("Éxito", operacion + " procesado correctamente")

def limpiar_campos(monto_var, banco_var, ubicacion_var, banco_destino_var, alias_var, operacion_var, resultado_text, ubicacion_label, ubicacion_combo, banco_destino_label, banco_destino_combo, alias_label, alias_entry):
    monto_var.set("")
    banco_var.set("")
    ubicacion_var.set("")
    banco_destino_var.set("")
    alias_var.set("")
    operacion_var.set("depositar")
    resultado_text.delete(1.0, tk.END)
    cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, banco_destino_label, banco_destino_combo, banco_destino_var, alias_label, alias_entry)

def ejecutar_aplicacion():
    root = tk.Tk()
    root.title("Depositar, Retirar y Transacción")
    root.geometry("500x480")
    root.resizable(False, False)
    
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    title_label = ttk.Label(main_frame, text="Sistema de Depósitos, Retiros y Transacciones", 
                           font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Variables 
    monto_var = tk.StringVar()
    operacion_var = tk.StringVar(value="depositar")
    banco_var = tk.StringVar()
    ubicacion_var = tk.StringVar()
    banco_destino_var = tk.StringVar()
    alias_var = tk.StringVar()
    
    # Monto
    ttk.Label(main_frame, text="Monto ($):", font=("Arial", 10, "bold")).grid(
        row=1, column=0, sticky=tk.W, pady=5)
    monto_entry = ttk.Entry(main_frame, textvariable=monto_var, width=20)
    monto_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    ttk.Label(main_frame, text="Operación:", font=("Arial", 10, "bold")).grid(
        row=2, column=0, sticky=tk.W, pady=5)
    
    radio_frame = ttk.Frame(main_frame)
    radio_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    # Elementos que aparecen/desaparecen según la operación
    ubicacion_label = ttk.Label(main_frame, text="Ubicación:", font=("Arial", 10, "bold"))
    ubicacion_combo = ttk.Combobox(main_frame, textvariable=ubicacion_var, 
                                  state="readonly", width=18)
    
    banco_destino_label = ttk.Label(main_frame, text="Banco destino:", font=("Arial", 10, "bold"))
    banco_destino_combo = ttk.Combobox(main_frame, textvariable=banco_destino_var,
                                      values=bancos, state="readonly", width=18)
    
    alias_label = ttk.Label(main_frame, text="Alias destinatario:", font=("Arial", 10, "bold"))
    alias_entry = ttk.Entry(main_frame, textvariable=alias_var, width=20)
    
    # Botones de operación
    ttk.Radiobutton(radio_frame, text="Depositar", variable=operacion_var, 
                   value="depositar", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, banco_destino_label, banco_destino_combo, banco_destino_var, alias_label, alias_entry)).pack(side=tk.LEFT)
    ttk.Radiobutton(radio_frame, text="Retirar", variable=operacion_var, 
                   value="retirar", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, banco_destino_label, banco_destino_combo, banco_destino_var, alias_label, alias_entry)).pack(side=tk.LEFT, padx=(10, 0))
    ttk.Radiobutton(radio_frame, text="Transacción", variable=operacion_var, 
                   value="transaccion", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, banco_destino_label, banco_destino_combo, banco_destino_var, alias_label, alias_entry)).pack(side=tk.LEFT, padx=(10, 0))
    
    # Banco origen
    ttk.Label(main_frame, text="Banco origen:", font=("Arial", 10, "bold")).grid(
        row=3, column=0, sticky=tk.W, pady=5)
    banco_combo = ttk.Combobox(main_frame, textvariable=banco_var, 
                               values=bancos, state="readonly", width=18)
    banco_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    banco_combo.bind("<<ComboboxSelected>>", lambda event: actualizar_ubicaciones(event, ubicacion_combo, banco_var, ubicacion_var))
    
    # Resultado
    resultado_frame = ttk.LabelFrame(main_frame, text="Resumen de la operación", 
                                    padding="10")
    resultado_frame.grid(row=6, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))
    
    resultado_text = tk.Text(resultado_frame, height=6, width=50, wrap=tk.WORD)
    resultado_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    scrollbar = ttk.Scrollbar(resultado_frame, orient=tk.VERTICAL, 
                             command=resultado_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    resultado_text.config(yscrollcommand=scrollbar.set)
    
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=10)
    
    # Botones principales
    ttk.Button(button_frame, text="Procesar", 
               command=lambda: procesar_operacion(monto_var, operacion_var, banco_var, ubicacion_var, banco_destino_var, alias_var, resultado_text)).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Limpiar", 
               command=lambda: limpiar_campos(monto_var, banco_var, ubicacion_var, banco_destino_var, alias_var, operacion_var, resultado_text, ubicacion_label, ubicacion_combo, banco_destino_label, banco_destino_combo, alias_label, alias_entry)).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Salir", command=root.quit).pack(side=tk.LEFT, padx=5)
    
    # Inicializar la vista
    cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, banco_destino_label, banco_destino_combo, banco_destino_var, alias_label, alias_entry)
    
    root.mainloop()

ejecutar_aplicacion()