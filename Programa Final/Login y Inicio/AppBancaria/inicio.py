import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import deposito_retiro  # IMPORTAR EL MÓDULO DE DEPÓSITO/RETIRO

# === Función para cargar JSON con valor por defecto ===
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

# === Guardar JSON simple (sin atomic) ===
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# === Función para identificar banco usando JSON externo o diccionario ===
def identificar_banco(legajo):
    bancos_path = os.path.join(os.path.dirname(__file__), "bancos.json")
    bancos = load_json(bancos_path, {})
    return bancos.get(legajo, "Banco no encontrado")

# === Función para abrir la ventana de cuenta ===
def abrir_pagina_cuenta(cuenta, cuentas_file, movimientos_file, parent=None):
    """
    recibe:
      - cuenta: dict de la cuenta autenticada
      - cuentas_file: path a cuentas.json
      - movimientos_file: path a movimientos.json
      - parent: ventana padre (login) para bloquear mientras está abierta
    """
    cuentas = load_json(cuentas_file, [])
    movimientos = load_json(movimientos_file, {})
    usuario = cuenta["usuario"]
    movimientos.setdefault(usuario, [])
    idx = next((i for i, c in enumerate(cuentas) if c["usuario"] == usuario), None)
    if idx is None:
        messagebox.showerror("Error", "Cuenta no encontrada en archivo de cuentas.")
        return

    # ventana cuenta
    cuenta_win = tk.Toplevel(parent)
    cuenta_win.geometry("1200x800")
    cuenta_win.title(f"Mi Cuenta - {usuario}")
    cuenta_win.resizable(False, False)

    # === BLOQUEAR LOGIN ===
    if parent:
        cuenta_win.transient(parent)  # modal
        cuenta_win.grab_set()          # bloquea interacción con login
        cuenta_win.focus()

    # encabezado con primera letra en mayúscula
    nombre_usuario = usuario.capitalize()
    tk.Label(cuenta_win, text=f"Bienvenido {nombre_usuario}", font=("Arial", 22, "bold")).pack(pady=10)
    tk.Label(cuenta_win, text=f"Legajo: {cuenta['legajo']} | Banco: {identificar_banco(cuenta['legajo'])}",
             font=("Arial", 16)).pack(pady=5)

    # saldo
    saldo_var = tk.StringVar(value=f"${cuentas[idx]['saldo']}")
    tk.Label(cuenta_win, textvariable=saldo_var, font=("Arial", 20, "bold")).pack(pady=10)

    # lista de movimientos
    tk.Label(cuenta_win, text="Movimientos de cuenta:", font=("Arial", 18, "bold")).pack(pady=10)
    lista_mov = tk.Listbox(cuenta_win, font=("Arial", 14), width=80, height=15)
    lista_mov.pack(pady=5)
    
    def actualizar_lista_movimientos():
        """Recargar la lista de movimientos desde el archivo"""
        nonlocal movimientos
        movimientos = load_json(movimientos_file, {})
        lista_mov.delete(0, tk.END)
        for mov in movimientos.get(usuario, []):
            lista_mov.insert(tk.END, f"{mov['fecha']} - {mov['tipo']} ${mov['monto']} - {mov.get('nota','')}")
    
    actualizar_lista_movimientos()

    # función para agregar movimientos
    def add_mov(tipo, monto, nota=""):
        nonlocal cuentas, movimientos, idx, usuario
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mov = {"tipo": tipo, "monto": monto, "fecha": fecha, "nota": nota}
        movimientos.setdefault(usuario, []).append(mov)
        lista_mov.insert(tk.END, f"{fecha} - {tipo} ${monto} - {nota}")
        cuentas[idx]["saldo"] += float(monto) if tipo.lower() == "deposito" else -float(monto)
        cuentas[idx]["saldo"] = round(cuentas[idx]["saldo"], 2)
        save_json(cuentas_file, cuentas)
        save_json(movimientos_file, movimientos)
        saldo_var.set(f"${cuentas[idx]['saldo']}")

    # ventana Depósito / Retiro - AHORA CONECTADA AL MÓDULO
    def abrir_deposito_retiro():
        # Llamar a la función del módulo deposito_retiro
        deposito_retiro.abrir_ventana_deposito_retiro(
            cuenta_win, 
            cuenta, 
            cuentas_file, 
            movimientos_file,
            callback_actualizar=lambda: [actualizar_saldo(), actualizar_lista_movimientos()]
        )
    
    def actualizar_saldo():
        """Recargar el saldo desde el archivo"""
        nonlocal cuentas, idx
        cuentas = load_json(cuentas_file, [])
        saldo_var.set(f"${cuentas[idx]['saldo']}")

    # botones principales
    frame_btn = tk.Frame(cuenta_win)
    frame_btn.pack(pady=20)
    tk.Button(frame_btn, text="Deposito/Retiro", font=("Arial", 14, "bold"),
              command=abrir_deposito_retiro, bd=7, width=18, bg="red").grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Pago de servicios", font=("Arial", 14, "bold"),
              command=lambda: messagebox.showinfo("Info", "Próximamente..."), bd=7, width=18, bg="red").grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Compra de divisas", font=("Arial", 14, "bold"),
              command=lambda: messagebox.showinfo("Info", "Próximamente..."), bd=7, width=18, bg="red").grid(row=0, column=2, padx=10)

    # cerrar ventana
    def cerrar_ventana():
        cuenta_win.destroy()
        if parent:
            # Limpiar los campos de login
            try:
                parent.nametowidget(".!frame.!entry").delete(0, tk.END)
                parent.nametowidget(".!frame2.!entry").delete(0, tk.END)
                parent.nametowidget(".!frame3.!entry").delete(0, tk.END)
            except:
                pass
            parent.focus_set()

    tk.Button(frame_btn, text="Cerrar", font=("Arial", 14, "bold"), command=cerrar_ventana,
              bd=7, width=18, bg="red").grid(row=0, column=3, padx=10)