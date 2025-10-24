import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# FUNCIONES DE ARCHIVOS

def cargar_datos():
    """Carga los datos desde datos.json o lo crea con valores por defecto."""
    if not os.path.exists("datos.json"):
        datos_iniciales = {
            "servicios": [
                {"codigo": "100", "nombre": "AYSA", "monto": 500},
                {"codigo": "200", "nombre": "Metrogas", "monto": 750},
                {"codigo": "300", "nombre": "Edesur", "monto": 620}
            ],
            "metodos_pago": ["Galicia", "BBVA", "MercadoPago", "Santander"],
            "empresas_celulares": ["Movistar", "Claro", "Personal", "Tuenti"]
        }
        with open("datos.json", "w", encoding="utf-8") as archivo:
            json.dump(datos_iniciales, archivo, indent=4, ensure_ascii=False)
    
    with open("datos.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_operacion(tipo, descripcion):
    """Guarda una operación realizada en un archivo de texto."""
    with open("operaciones.txt", "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        archivo.write(f"[{fecha}] {tipo}: {descripcion}\n")

# CARGA DE DATOS

datos = cargar_datos()
servicios = datos["servicios"]
metodos_pago = datos["metodos_pago"]
empresas_celulares = datos["empresas_celulares"]

# VARIABLES GLOBALES 

servicio_actual = None
empresa_seleccionada = None
numero_celular = None
numero_sube = None

#  FUNCIONES GENERALES 

def limpiar_pantalla():
    """Limpia la ventana actual."""
    for widget in ventana_principal.winfo_children():
        widget.pack_forget()

#  PAGOS DE SERVICIOS 

def pagar_servicios():
    limpiar_pantalla()
    tk.Label(ventana_principal, text="Ingrese el código del servicio:").pack(pady=5)
    entrada_codigo.pack(pady=5)
    tk.Button(ventana_principal, text="Continuar", command=continuar_pago).pack(pady=5)

def buscar_servicio(codigo):
    """Busca un servicio por su código."""
    for servicio in servicios:
        if servicio["codigo"] == codigo:
            return servicio
    return None

def continuar_pago():
    """Valida el código e inicia el proceso de pago."""
    global servicio_actual
    codigo = entrada_codigo.get()
    servicio_actual = buscar_servicio(codigo)

    if servicio_actual:
        limpiar_pantalla()
        nombre = servicio_actual["nombre"]
        monto = servicio_actual["monto"]
        tk.Label(ventana_principal, text=f"Servicio: {nombre}\nMonto: ${monto}", font=("Arial", 14)).pack(pady=10)
        
        for metodo in metodos_pago:
            tk.Button(ventana_principal, text=metodo, width=20, command=lambda m=metodo: realizar_pago(m)).pack(pady=3)
    else:
        messagebox.showerror("Error", f"El código {codigo} no está registrado.")

def realizar_pago(metodo):
    """Confirma y guarda el pago."""
    monto = servicio_actual["monto"]
    nombre = servicio_actual["nombre"]
    confirmar = messagebox.askyesno("Confirmar", f"¿Desea pagar ${monto} a {nombre} con {metodo}?")
    if confirmar:
        guardar_operacion("Pago de servicio", f"{nombre} - ${monto} con {metodo}")
        messagebox.showinfo("Éxito", "El pago se realizó correctamente.")
        ventana_principal.destroy()

# RECARGA DE CELULAR

def recargar_celular():
    limpiar_pantalla()
    tk.Label(ventana_principal, text="Seleccione la empresa:", font=("Arial", 12)).pack(pady=5)
    for empresa in empresas_celulares:
        tk.Button(ventana_principal, text=empresa, width=20, command=lambda e=empresa: ingresar_numero_celular(e)).pack(pady=5)

def ingresar_numero_celular(empresa):
    """Solicita el número de celular."""
    global empresa_seleccionada
    empresa_seleccionada = empresa
    limpiar_pantalla()
    tk.Label(ventana_principal, text=f"Empresa seleccionada: {empresa}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_principal, text="Ingrese número de celular (10 dígitos):").pack(pady=5)
    entrada_numero.pack(pady=5)
    tk.Button(ventana_principal, text="Continuar", command=ingresar_monto_celular).pack(pady=10)

def ingresar_monto_celular():
    """Pide el monto de recarga."""
    global numero_celular
    numero_celular = entrada_numero.get()

    if not numero_celular.isdigit() or len(numero_celular) != 10:
        messagebox.showerror("Error", "Ingrese un número válido de 10 dígitos.")
        return

    limpiar_pantalla()
    tk.Label(ventana_principal, text=f"Empresa: {empresa_seleccionada}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_principal, text=f"Número: {numero_celular}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_principal, text="Seleccione el monto (1000 - 7000):", font=("Arial", 12)).pack(pady=5)

    montos = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
    for monto in montos:
        tk.Button(ventana_principal, text=f"${monto}", width=15, command=lambda m=monto: confirmar_recarga(m)).pack(pady=5)

def confirmar_recarga(monto):
    """Confirma y guarda la recarga."""
    confirmar = messagebox.askyesno("Confirmar", f"¿Recargar ${monto} a {empresa_seleccionada} - {numero_celular}?")
    if confirmar:
        guardar_operacion("Recarga de celular", f"{empresa_seleccionada} - {numero_celular} - ${monto}")
        messagebox.showinfo("Éxito", "Recarga realizada con éxito.")
        ventana_principal.destroy()

# CARGA SUBE 

def cargar_sube():
    limpiar_pantalla()
    tk.Label(ventana_principal, text="Ingrese número de SUBE:").pack(pady=5)
    entrada_sube.pack(pady=5)
    tk.Button(ventana_principal, text="Continuar", command=mostrar_montos_sube).pack(pady=10)
def mostrar_montos_sube():
    """Muestra los montos disponibles para cargar la SUBE."""
    global numero_sube
    numero_sube = entrada_sube.get()

    # Validación: debe ser numérico y tener 16 dígitos
    if not numero_sube.isdigit() or len(numero_sube) != 16:
        messagebox.showerror("Error", "Ingrese un número de SUBE válido de 16 dígitos.")
        return

    limpiar_pantalla()
    tk.Label(ventana_principal, text=f"Número SUBE: {numero_sube}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_principal, text="Seleccione un monto:", font=("Arial", 12)).pack(pady=5)

    montos = [2000, 3000, 4000, 5000, 6000, 7000]
    for monto in montos:
        tk.Button(ventana_principal, text=f"${monto}", width=15, command=lambda m=monto: confirmar_carga_sube(m)).pack(pady=5)


def confirmar_carga_sube(monto):
    """Confirma y guarda la carga SUBE."""
    confirmar = messagebox.askyesno("Confirmar", f"¿Cargar la SUBE {numero_sube} con ${monto}?")
    if confirmar:
        guardar_operacion("Carga SUBE", f"N° {numero_sube} - ${monto}")
        messagebox.showinfo("Éxito", "Carga de SUBE realizada con éxito.")
        ventana_principal.destroy()

# VENTANA PRINCIPAL 

ventana_principal = tk.Tk()
ventana_principal.title("Sistema de Pagos")
ventana_principal.geometry("350x450")

# Entradas reutilizables
entrada_codigo = tk.Entry(ventana_principal)
entrada_numero = tk.Entry(ventana_principal)
entrada_sube = tk.Entry(ventana_principal)

# Menú principal
tk.Label(ventana_principal, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=10)
tk.Button(ventana_principal, text="Pagar Servicios", width=25, command=pagar_servicios).pack(pady=10)
tk.Button(ventana_principal, text="Recargar Celular", width=25, command=recargar_celular).pack(pady=10)
tk.Button(ventana_principal, text="Cargar SUBE", width=25, command=cargar_sube).pack(pady=10)

ventana_principal.mainloop()
