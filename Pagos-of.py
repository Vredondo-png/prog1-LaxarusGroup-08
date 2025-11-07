import tkinter as tk
from tkinter import messagebox
import json, os
from datetime import datetime

USUARIO_ACTUAL = "candela"

# Archivos
def cargar_datos():
    if not os.path.exists("datos.json"):
        datos = {
            "servicios":[
                {"codigo":"100","nombre":"AYSA","monto":500},
                {"codigo":"200","nombre":"Metrogas","monto":750},
                {"codigo":"300","nombre":"Edesur","monto":620}
            ],
            "metodos_pago":["Galicia","BBVA","MercadoPago","Santander"],
            "empresas_celulares":["Movistar","Claro","Personal","Tuenti"]
        }
        with open("datos.json","w",encoding="utf-8") as f:
            json.dump(datos,f,indent=4,ensure_ascii=False)
    with open("datos.json","r",encoding="utf-8") as f:
        return json.load(f)

def guardar_txt(tipo, desc):
    """Guarda la operación indicando el usuario"""
    with open("operaciones.txt","a",encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {tipo} ({USUARIO_ACTUAL}): {desc}\n")

def guardar_json(tipo,monto,nota):
    ruta="movimientos.json"
    if not os.path.exists(ruta):
        base={"candela":[],"miguel":[],"valentin":[],"sergei":[],"usuario":[]}
        with open(ruta,"w",encoding="utf-8") as f:
            json.dump(base,f,indent=4,ensure_ascii=False)
    with open(ruta,"r",encoding="utf-8") as f:
        datos=json.load(f)
    if USUARIO_ACTUAL not in datos: datos[USUARIO_ACTUAL]=[]
    datos[USUARIO_ACTUAL].append({
        "tipo":tipo,
        "monto":monto,
        "fecha":str(datetime.now()),
        "nota":nota
    })
    with open(ruta,"w",encoding="utf-8") as f:
        json.dump(datos,f,indent=4,ensure_ascii=False)

# Datos
datos = cargar_datos()
servicios = datos["servicios"]
metodos_pago = datos["metodos_pago"]
empresas_celulares = datos["empresas_celulares"]

# Ventana
ventana = tk.Tk()
ventana.title("Sistema de Pagos")
ventana.geometry("400x550")

entrada_codigo = tk.Entry(ventana, font=("Arial",12))
entrada_numero = tk.Entry(ventana, font=("Arial",12))
entrada_sube = tk.Entry(ventana, font=("Arial",12))
servicio_actual = empresa_seleccionada = numero_celular = numero_sube = None

def limpiar(): [w.pack_forget() for w in ventana.winfo_children()]

def crear_boton(texto, comando, ancho=15, alto=2):
    return tk.Button(ventana, text=texto, command=comando, font=("Arial",12), width=ancho, height=alto)

# Menú principal
def menu_principal():
    limpiar()
    tk.Label(ventana,text="Seleccione una opción:",font=("Arial",14,"bold")).pack(pady=20)
    crear_boton("Pagar Servicios", pagar_servicios).pack(pady=10)
    crear_boton("Recargar Celular", recargar_celular).pack(pady=10)
    crear_boton("Cargar SUBE", cargar_sube).pack(pady=10)
    tk.Label(ventana,text=f"Usuario actual: {USUARIO_ACTUAL}",font=("Arial",11,"italic")).pack(side="bottom",pady=10)

# Pagos
def pagar_servicios():
    limpiar()
    tk.Label(ventana,text="Código servicio:",font=("Arial",12)).pack(pady=10)
    entrada_codigo.pack(pady=10)
    crear_boton("Continuar", continuar_pago).pack(pady=15)
    crear_boton("Volver", menu_principal).pack(pady=10)

def buscar_servicio(codigo):
    return next((s for s in servicios if s["codigo"]==codigo), None)

def continuar_pago():
    global servicio_actual
    codigo = entrada_codigo.get()
    servicio_actual = buscar_servicio(codigo)
    if servicio_actual:
        limpiar()
        tk.Label(ventana,text=f"{servicio_actual['nombre']} - ${servicio_actual['monto']}",font=("Arial",14)).pack(pady=15)
        for m in metodos_pago:
            crear_boton(m, lambda x=m: realizar_pago(x), ancho=12, alto=2).pack(pady=5)
        crear_boton("Volver", menu_principal).pack(pady=15)
    else:
        messagebox.showerror("Error","Código no existe")

def realizar_pago(m):
    if messagebox.askyesno("Confirmar",f"Pagar ${servicio_actual['monto']} a {servicio_actual['nombre']} con {m}?"):
        guardar_txt("Pago de servicio",f"{servicio_actual['nombre']} - ${servicio_actual['monto']} con {m}")
        guardar_json("pago_servicio",servicio_actual['monto'],f"{servicio_actual['nombre']} con {m}")
        messagebox.showinfo("Éxito","Pago realizado")
        ventana.destroy()  # Cierra la ventana al finalizar

# Recarga Celular
def recargar_celular():
    limpiar()
    tk.Label(ventana,text="Seleccione empresa:",font=("Arial",12)).pack(pady=10)
    for e in empresas_celulares: crear_boton(e, lambda x=e: ingresar_numero_celular(x), ancho=12, alto=2).pack(pady=5)
    crear_boton("Volver", menu_principal).pack(pady=10)

def ingresar_numero_celular(e):
    global empresa_seleccionada
    empresa_seleccionada=e
    limpiar()
    tk.Label(ventana,text=f"Empresa: {empresa_seleccionada}", font=("Arial",12)).pack(pady=5)
    tk.Label(ventana,text="Número (10 dígitos):", font=("Arial",12)).pack(pady=5)
    entrada_numero.pack(pady=10)
    crear_boton("Continuar", ingresar_monto_celular).pack(pady=15)
    crear_boton("Volver", menu_principal).pack(pady=10)

def ingresar_monto_celular():
    global numero_celular
    numero_celular=entrada_numero.get()
    if not numero_celular.isdigit() or len(numero_celular)!=10:
        return messagebox.showerror("Error","Número inválido. Debe tener 10 dígitos")
    limpiar()
    tk.Label(ventana,text=f"Empresa: {empresa_seleccionada}", font=("Arial",12)).pack(pady=5)
    tk.Label(ventana,text=f"Número: {numero_celular}", font=("Arial",12)).pack(pady=5)
    for m in [1000,2000,3000,4000,5000,6000,7000]:
        crear_boton(f"${m}", lambda x=m: confirmar_recarga(x), ancho=10, alto=1).pack(pady=5)
    crear_boton("Volver", menu_principal, ancho=12, alto=2).pack(pady=10)

def confirmar_recarga(m):
    if messagebox.askyesno("Confirmar",f"Recargar ${m}?"):
        guardar_txt("Recarga celular",f"{empresa_seleccionada}-{numero_celular}-${m}")
        guardar_json("recarga_celular",m,f"{empresa_seleccionada}-{numero_celular}")
        messagebox.showinfo("Éxito","Recarga realizada")
        ventana.destroy()  # Cierra la ventana al finalizar

# Cargar SUBE
def cargar_sube():
    limpiar()
    tk.Label(ventana,text="Número SUBE:",font=("Arial",12)).pack(pady=10)
    entrada_sube.pack(pady=10)
    crear_boton("Continuar", mostrar_montos_sube).pack(pady=15)
    crear_boton("Volver", menu_principal).pack(pady=10)

def mostrar_montos_sube():
    global numero_sube
    numero_sube=entrada_sube.get()
    if not numero_sube.isdigit() or len(numero_sube)!=16:
        return messagebox.showerror("Error","Número SUBE inválido. Debe tener 16 dígitos")
    limpiar()
    tk.Label(ventana,text=f"Número SUBE: {numero_sube}", font=("Arial",12)).pack(pady=5)
    for m in [2000,3000,4000,5000,6000,7000]:
        crear_boton(f"${m}", lambda x=m: confirmar_sube(x), ancho=10, alto=1).pack(pady=5)
    crear_boton("Volver", menu_principal, ancho=12, alto=2).pack(pady=10)

def confirmar_sube(m):
    if messagebox.askyesno("Confirmar",f"Cargar ${m}?"):
        guardar_txt("Carga SUBE",f"N°{numero_sube}-${m}")
        guardar_json("carga_sube",m,f"N°{numero_sube}")
        messagebox.showinfo("Éxito","Carga realizada")
        ventana.destroy()  # Cierra la ventana al finalizar

# Inicio
menu_principal()
ventana.mainloop()
