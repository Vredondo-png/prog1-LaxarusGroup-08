import tkinter as tk
from tkinter import messagebox

# Lista de servicios
servicios = [
    ["100", "AYSA", 500],
    ["200", "Metrogas", 750],
    ["300", "Edesur", 620],
]

# Opciones
metodos = ["Galicia", "BBVA", "MercadoPago", "Santander"]
empresas_celular = ["Movistar", "Claro", "Personal", "Tuenti"]

# Variables globales
servicio_actual = None
empresa_seleccionada = None
numero_celular = None
numero_sube = None

# FUNCIONES GENERALES 
def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.pack_forget()

# PAGOS DE SERVICIOS
def pagar_servicios():
    limpiar_pantalla()
    tk.Label(root, text="Ingrese el código de pago:").pack(pady=5)
    codigo_entry.pack(pady=5)
    tk.Button(root, text="Continuar", command=continuar).pack(pady=5)

def buscar_servicio(codigo):
    for s in servicios:
        if s[0] == codigo:
            return s
    return None

def continuar():
    global servicio_actual
    codigo = codigo_entry.get()
    servicio_actual = buscar_servicio(codigo)

    if servicio_actual:
        limpiar_pantalla()
        nombre, monto = servicio_actual[1], servicio_actual[2]
        tk.Label(root, text=f"Servicio: {nombre}\nMonto: ${monto}", font=("Arial", 14)).pack(pady=10)
        
        for m in metodos:
            tk.Button(root, text=m, width=20, command=lambda m=m: pagar(m)).pack(pady=3)
    else:
        messagebox.showerror("Error", f"Código {codigo} no reconocido.")

def pagar(metodo):
    monto = servicio_actual[2]
    confirmar = messagebox.askyesno("Confirmar", f"¿Pagar ${monto} con {metodo}?")
    if confirmar:
        messagebox.showinfo("Éxito", "Pago realizado con éxito")
        root.destroy()

# RECARGA DE CELULAR
def recargar():
    limpiar_pantalla()
    tk.Label(root, text="Seleccione la empresa:", font=("Arial", 12)).pack(pady=5)
    for emp in empresas_celular:
        tk.Button(root, text=emp, width=20, command=lambda e=emp: pedir_numero_celular(e)).pack(pady=5)

def pedir_numero_celular(empresa):
    global empresa_seleccionada
    empresa_seleccionada = empresa
    limpiar_pantalla()
    tk.Label(root, text=f"Empresa seleccionada: {empresa}", font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text="Ingrese número de celular (10 dígitos):").pack(pady=5)
    recarga_numero.pack(pady=5)
    tk.Button(root, text="Continuar", command=pedir_monto_celular).pack(pady=10)

def pedir_monto_celular():
    global numero_celular
    numero_celular = recarga_numero.get()

    if not numero_celular.isdigit() or len(numero_celular) != 10:
        messagebox.showerror("Error", "Ingrese un número de celular válido (10 dígitos).")
        return

    limpiar_pantalla()
    tk.Label(root, text=f"Empresa: {empresa_seleccionada}", font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text=f"Número: {numero_celular}", font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text="Seleccione monto (1000 - 7000):", font=("Arial", 12)).pack(pady=5)

    montos = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
    for m in montos:
        tk.Button(root, text=f"${m}", width=15, command=lambda monto=m: confirmar_recarga(monto)).pack(pady=5)

def confirmar_recarga(monto):
    confirmar = messagebox.askyesno("Confirmar", f"¿Recargar ${monto} a {empresa_seleccionada} - {numero_celular}?")
    if confirmar:
        messagebox.showinfo("Éxito", "Recarga realizada con éxito")
        root.destroy()

# CARGA SUBE
def cargar_sube():
    limpiar_pantalla()
    tk.Label(root, text="Ingrese número de SUBE:").pack(pady=5)
    sube_numero.pack(pady=5)
    tk.Button(root, text="Continuar", command=mostrar_montos_sube).pack(pady=10)

def mostrar_montos_sube():
    global numero_sube
    numero_sube = sube_numero.get()

    if not numero_sube.isdigit():
        messagebox.showerror("Error", "Ingrese un número de SUBE válido.")
        return

    limpiar_pantalla()
    tk.Label(root, text=f"Número SUBE: {numero_sube}", font=("Arial", 12)).pack(pady=5)
    tk.Label(root, text="Seleccione un monto:", font=("Arial", 12)).pack(pady=5)

    montos = [2000, 3000, 4000, 5000, 6000, 7000]
    for m in montos:
        tk.Button(root, text=f"${m}", width=15, command=lambda monto=m: confirmar_sube(monto)).pack(pady=5)

def confirmar_sube(monto):
    confirmar = messagebox.askyesno("Confirmar", f"¿Cargar SUBE {numero_sube} con ${monto}?")
    if confirmar:
        messagebox.showinfo("Éxito", "Carga SUBE realizada con éxito")
        root.destroy()

# VENTANA PRINCIPAL 
root = tk.Tk()
root.title("Sistema de Pagos")
root.geometry("350x450")

# Widgets globales reutilizables
codigo_entry = tk.Entry(root)
recarga_numero = tk.Entry(root)
sube_numero = tk.Entry(root)

# Menú principal
tk.Label(root, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Pagar Servicios", width=25, command=pagar_servicios).pack(pady=10)
tk.Button(root, text="Recargar Celular", width=25, command=recargar).pack(pady=10)
tk.Button(root, text="Cargar SUBE", width=25, command=cargar_sube).pack(pady=10)

root.mainloop()











