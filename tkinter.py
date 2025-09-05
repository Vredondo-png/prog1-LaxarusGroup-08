
import tkinter as tk
from tkinter import messagebox

# Lista de servicios: [código de pago, nombre, monto]
servicios = [
    ["100", "AYSA", 500],
    ["200", "Metrogas", 750],
    ["300", "Edesur", 620],
]

# Métodos de pago
metodos = ["Galicia", "BBVA", "MercadoPago", "Santander"]

servicio_actual = None  # Para guardar el servicio seleccionado

# Buscar servicio
def buscar_servicio(codigo):
    for s in servicios:
        if s[0] == codigo:
            return s
    return None

# Paso 1: continuar después de ingresar código de pago
def continuar():
    global servicio_actual
    codigo = codigo_entry.get()
    servicio_actual = buscar_servicio(codigo)
    
    if servicio_actual:
        # Ocultar widgets de código de pago
        codigo_label.pack_forget()
        codigo_entry.pack_forget()
        continuar_btn.pack_forget()
        
        # Mostrar info del servicio
        nombre = servicio_actual[1]
        monto = servicio_actual[2]
        info_label.config(text=f"Servicio: {nombre}\nMonto: ${monto}")
        info_label.pack(pady=10)
        
        # Mostrar botones para cada método de pago
        for m in metodos:
            btn = tk.Button(root, text=m, width=15, command=lambda m=m: pagar(m))
            btn.pack(pady=3)
            pago_btns.append(btn)
    else:
        messagebox.showerror("Error", f"Código {codigo} no reconocido.")

# Paso 2: pagar cuando se presiona un botón
def pagar(metodo_seleccionado):
    monto = servicio_actual[2]     # Tomar el tercer elemento de la lista que es el monto a pagar
    confirmar = messagebox.askyesno("Confirmar", f"¿Quiere pagar ${monto} con {metodo_seleccionado}?")
    if confirmar:
        messagebox.showinfo("Pago", " Pago realizado")
        root.destroy()  # Cierra la ventana al finalizar

# Ventana principal
root = tk.Tk()
root.title("Pago de Servicios")  # Título de la ventana
root.geometry("350x300")         # Tamaño de la ventana

# Widgets iniciales para código de pago
codigo_label = tk.Label(root, text="Ingrese el código de pago:")
codigo_label.pack(pady=5)
codigo_entry = tk.Entry(root)
codigo_entry.pack(pady=5)
continuar_btn = tk.Button(root, text="Continuar", command=continuar)
continuar_btn.pack(pady=5)

# Label para info del servicio
info_label = tk.Label(root, text="", font=("Arial", 18))

# Lista para guardar botones de pago y poder manipularlos si queremos
pago_btns = []

root.mainloop()    # Mantiene la ventana abierta y permite interacción
