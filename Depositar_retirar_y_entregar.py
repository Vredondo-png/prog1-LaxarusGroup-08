import tkinter as tk
from tkinter import ttk, messagebox
import os

# Función para cargar bancos desde archivo
def cargar_bancos():
    bancos_dict = {}
    try:
        if os.path.exists("bancos.txt"):
            with open("bancos.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea and "," in linea:
                        codigo, nombre = linea.split(",", 1)
                        bancos_dict[codigo.strip()] = nombre.strip()
        else:
            # Crear archivo por defecto si no existe
            bancos_default = {
                "001": "Banco Santander",
                "002": "Banco Galicia",
                "003": "Banco Nación",
                "004": "Banco Macro",
                "005": "BBVA",
                "006": "Banco Ciudad"
            }
            with open("bancos.txt", "w", encoding="utf-8") as archivo:
                for codigo, nombre in bancos_default.items():
                    archivo.write(f"{codigo},{nombre}\n")
            bancos_dict = bancos_default
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar bancos: {str(e)}")
    
    return bancos_dict

# Función para cargar ubicaciones desde archivo
def cargar_ubicaciones():
    ubicaciones_dict = {}
    try:
        if os.path.exists("ubicaciones.txt"):
            with open("ubicaciones.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea and "," in linea:
                        partes = linea.split(",")
                        if len(partes) >= 3:
                            codigo_banco = partes[0].strip()
                            codigo_ubicacion = partes[1].strip()
                            nombre_ubicacion = partes[2].strip()
                            
                            if codigo_banco not in ubicaciones_dict:
                                ubicaciones_dict[codigo_banco] = {}
                            
                            ubicaciones_dict[codigo_banco][codigo_ubicacion] = nombre_ubicacion
        else:
            # Crear archivo por defecto si no existe
            ubicaciones_default = [
                "001,U001,Palermo",
                "001,U002,Recoleta",
                "001,U003,Belgrano",
                "001,U004,San Telmo",
                "001,U005,Puerto Madero",
                "002,U001,Palermo,Buenos Aires",
                "002,U002,Villa Crespo",
                "002,U003,Caballito",
                "002,U004,Flores",
                "002,U005,Núñez",
                "003,U001,Microcentro",
                "003,U002,Once",
                "003,U003,Barracas",
                "003,U004,La Boca",
                "003,U005,Constitución",
                "004,U001,Almagro",
                "004,U002,Balvanera",
                "004,U003,Parque Patricios",
                "004,U004,Boedo",
                "004,U005,Villa Urquiza",
                "005,U001,Retiro",
                "005,U002,San Nicolás",
                "005,U003,Montserrat",
                "005,U004,Villa Devoto",
                "005,U005,Colegiales",
                "006,U001,Centro",
                "006,U002,Barrio Norte",
                "006,U003,Villa Crespo",
                "006,U004,Chacarita",
                "006,U005,Agronomía"
            ]
            with open("ubicaciones.txt", "w", encoding="utf-8") as archivo:
                for linea in ubicaciones_default:
                    archivo.write(linea + "\n")
            
            # Procesar ubicaciones default
            for linea in ubicaciones_default:
                partes = linea.split(",")
                codigo_banco = partes[0].strip()
                codigo_ubicacion = partes[1].strip()
                nombre_ubicacion = partes[2].strip()
                
                if codigo_banco not in ubicaciones_dict:
                    ubicaciones_dict[codigo_banco] = {}
                
                ubicaciones_dict[codigo_banco][codigo_ubicacion] = nombre_ubicacion
                
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar ubicaciones: {str(e)}")
    
    return ubicaciones_dict

def cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var, 
                     legajo_label, legajo_entry):
    # Ocultar todos los campos especiales primero
    ubicacion_label.grid_remove()
    ubicacion_combo.grid_remove()
    legajo_label.grid_remove()
    legajo_entry.grid_remove()
    
    if operacion_var.get() == "depositar":
        pass
    elif operacion_var.get() == "retirar":
        ubicacion_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        ubicacion_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        actualizar_ubicaciones(None, ubicacion_combo, banco_var, ubicacion_var)
    elif operacion_var.get() == "depositar_a":
        legajo_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        legajo_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)

def actualizar_ubicaciones(event, ubicacion_combo, banco_var, ubicacion_var):
    banco_seleccionado = banco_var.get()
    if banco_seleccionado:
        # Buscar el código del banco
        codigo_banco = None
        for cod, nombre in bancos_data.items():
            if nombre == banco_seleccionado:
                codigo_banco = cod
                break
        
        if codigo_banco and codigo_banco in ubicaciones_data:
            # Obtener lista de nombres de ubicaciones
            ubicaciones_nombres = list(ubicaciones_data[codigo_banco].values())
            ubicacion_combo.config(values=ubicaciones_nombres)
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
        if caracter not in caracteres_validos:
            return False
    return True

def obtener_codigo_banco(nombre_banco):
    """Obtiene el código del banco por su nombre"""
    for codigo, nombre in bancos_data.items():
        if nombre == nombre_banco:
            return codigo
    return None

def obtener_codigo_ubicacion(codigo_banco, nombre_ubicacion):
    """Obtiene el código de ubicación por nombre"""
    if codigo_banco in ubicaciones_data:
        for codigo, nombre in ubicaciones_data[codigo_banco].items():
            if nombre == nombre_ubicacion:
                return codigo
    return None

def procesar_operacion(monto_var, operacion_var, banco_var, ubicacion_var, resultado_text, legajo_var):
    # Validar monto
    monto_texto = monto_var.get()
    
    if not es_numero_valido(monto_texto):
        messagebox.showerror("Error", "Ingrese un monto válido")
        return
    
    monto = float(monto_texto.replace(',', '.'))
    
    if monto > 25000000:
        messagebox.showerror("Error", "Ingrese una cantidad de dinero que tenga")
        return
    
    if monto <= 0:
        messagebox.showerror("Error", "El monto debe ser mayor a 0")
        return
    
    # Validar banco
    if banco_var.get() == "":
        messagebox.showerror("Error", "Seleccione un banco")
        return
    
    # Validar según el tipo de operación
    if operacion_var.get() == "retirar":
        if ubicacion_var.get() == "":
            messagebox.showerror("Error", "Seleccione una ubicación para el retiro")
            return
    
    elif operacion_var.get() == "depositar_a":
        if legajo_var.get() == "":
            messagebox.showerror("Error", "Ingrese el número de legajo")
            return
    
    # Obtener códigos
    codigo_banco = obtener_codigo_banco(banco_var.get())
    codigo_ubicacion = None
    if operacion_var.get() == "retirar":
        codigo_ubicacion = obtener_codigo_ubicacion(codigo_banco, ubicacion_var.get())
    
    # Generar resumen
    resultado_text.delete(1.0, tk.END)
    
    if operacion_var.get() == "depositar":
        operacion = "DEPÓSITO"
    elif operacion_var.get() == "retirar":
        operacion = "RETIRO"
    else:
        operacion = "DEPÓSITO A LEGAJO"
    
    resultado = "=== " + operacion + " PROCESADO ===\n\n"
    resultado += "Monto: $" + str(monto) + "\n"
    resultado += "Banco: " + banco_var.get() + " (Código: " + codigo_banco + ")\n"
    
    if operacion_var.get() == "retirar":
        resultado += "Ubicación: " + ubicacion_var.get() + " (Código: " + codigo_ubicacion + ")\n"
    elif operacion_var.get() == "depositar_a":
        resultado += "Legajo destino: " + legajo_var.get() + "\n"
    
    resultado += "\nOperación realizada exitosamente.\n"
    
    if operacion_var.get() == "depositar":
        resultado += "El dinero ha sido depositado en " + banco_var.get() + "."
    elif operacion_var.get() == "retirar":
        resultado += "Puede retirar el dinero en " + banco_var.get() + " - " + ubicacion_var.get() + "."
    else:
        resultado += "El dinero ha sido transferido al legajo " + legajo_var.get() + "."
    
    resultado_text.insert(1.0, resultado)
    messagebox.showinfo("Éxito", operacion + " procesado correctamente")

def limpiar_campos(monto_var, banco_var, ubicacion_var, operacion_var, resultado_text, 
                  ubicacion_label, ubicacion_combo, legajo_label, legajo_entry, legajo_var):
    monto_var.set("")
    banco_var.set("")
    ubicacion_var.set("")
    legajo_var.set("")
    operacion_var.set("depositar")
    resultado_text.delete(1.0, tk.END)
    cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var,
                     legajo_label, legajo_entry)

def ejecutar_aplicacion():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Depositar y Retirar")
    root.geometry("500x450")
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
    legajo_var = tk.StringVar()
    
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
    
    # Crear elementos de ubicación (para retiro)
    ubicacion_label = ttk.Label(main_frame, text="Ubicación:", font=("Arial", 10, "bold"))
    ubicacion_combo = ttk.Combobox(main_frame, textvariable=ubicacion_var, 
                                  state="readonly", width=18)
    
    # Crear elementos para legajo
    legajo_label = ttk.Label(main_frame, text="Legajo:", font=("Arial", 10, "bold"))
    legajo_entry = ttk.Entry(main_frame, textvariable=legajo_var, width=20)
    
    # Radiobuttons de operación
    ttk.Radiobutton(radio_frame, text="Depositar", variable=operacion_var, 
                   value="depositar", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, 
                                                     banco_var, ubicacion_var, legajo_label, 
                                                     legajo_entry)).pack(side=tk.LEFT)
    ttk.Radiobutton(radio_frame, text="Retirar", variable=operacion_var, 
                   value="retirar", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, 
                                                     banco_var, ubicacion_var, legajo_label, 
                                                     legajo_entry)).pack(side=tk.LEFT, padx=(10, 0))
    ttk.Radiobutton(radio_frame, text="Depositar a", variable=operacion_var, 
                   value="depositar_a", 
                   command=lambda: cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, 
                                                     banco_var, ubicacion_var, legajo_label, 
                                                     legajo_entry)).pack(side=tk.LEFT, padx=(10, 0))
    
    # Banco
    ttk.Label(main_frame, text="Banco:", font=("Arial", 10, "bold")).grid(
        row=3, column=0, sticky=tk.W, pady=5)
    
    # Obtener lista de nombres de bancos
    nombres_bancos = list(bancos_data.values())
    
    banco_combo = ttk.Combobox(main_frame, textvariable=banco_var, 
                               values=nombres_bancos, state="readonly", width=18)
    banco_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    banco_combo.bind("<<ComboboxSelected>>", lambda event: actualizar_ubicaciones(event, ubicacion_combo, banco_var, ubicacion_var))
    
    # Frame para resultado
    resultado_frame = ttk.LabelFrame(main_frame, text="Resumen de la operación", 
                                    padding="10")
    resultado_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))
    
    resultado_text = tk.Text(resultado_frame, height=8, width=50, wrap=tk.WORD)
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
               command=lambda: procesar_operacion(monto_var, operacion_var, banco_var, ubicacion_var, 
                                                 resultado_text, legajo_var)).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Limpiar", 
               command=lambda: limpiar_campos(monto_var, banco_var, ubicacion_var, operacion_var, 
                                            resultado_text, ubicacion_label, ubicacion_combo,
                                            legajo_label, legajo_entry, legajo_var)).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Salir", command=root.quit).pack(side=tk.LEFT, padx=5)
    
    # Configurar el cambio inicial
    cambiar_operacion(operacion_var, ubicacion_label, ubicacion_combo, banco_var, ubicacion_var,
                     legajo_label, legajo_entry)
    
    root.mainloop()

if __name__ == "__main__":
    # Cargar datos desde archivos
    bancos_data = cargar_bancos()
    ubicaciones_data = cargar_ubicaciones()
    
    if not bancos_data:
        messagebox.showerror("Error", "No se pudieron cargar los bancos")
    else:
        ejecutar_aplicacion()