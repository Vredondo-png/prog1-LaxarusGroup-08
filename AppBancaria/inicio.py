import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def identificar_banco(legajo):
    bancos = {
        "100": "Banco Santander",
        "200": "BBVA",
        "300": "Banco Galicia",
        "400": "Banco Nación"
    }
    return bancos.get(legajo, "Banco no encontrado")

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

    # Modal: bloquea ventana de login
    if parent:
        cuenta_win.transient(parent)
        cuenta_win.grab_set()
        cuenta_win.focus()

    # encabezado
    tk.Label(cuenta_win, text=f"Bienvenido {usuario}", font=("Arial", 22, "bold")).pack(pady=10)
    tk.Label(cuenta_win, text=f"Legajo: {cuenta['legajo']} | Banco: {identificar_banco(cuenta['legajo'])}",
             font=("Arial", 16)).pack(pady=5)

    saldo_var = tk.StringVar(value=f"${cuentas[idx]['saldo']}")
    tk.Label(cuenta_win, textvariable=saldo_var, font=("Arial", 20, "bold")).pack(pady=10)

    tk.Label(cuenta_win, text="Movimientos de cuenta:", font=("Arial", 18, "bold")).pack(pady=10)
    lista_mov = tk.Listbox(cuenta_win, font=("Arial", 14), width=80, height=15)
    lista_mov.pack(pady=5)
    for mov in movimientos.get(usuario, []):
        lista_mov.insert(tk.END, f"{mov['fecha']} - {mov['tipo']} ${mov['monto']} - {mov.get('nota','')}")

    def add_mov(tipo, monto, nota=""):
        nonlocal cuentas, movimientos, idx, usuario
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mov = {"tipo": tipo, "monto": monto, "fecha": fecha, "nota": nota}
        movimientos.setdefault(usuario, []).append(mov)
        lista_mov.insert(tk.END, f"{fecha} - {tipo} ${monto} - {nota}")
        cuentas[idx]["saldo"] = round(float(cuentas[idx]["saldo"]), 2)
        save_json_atomic(cuentas_file, cuentas)
        save_json_atomic(movimientos_file, movimientos)
        saldo_var.set(f"${cuentas[idx]['saldo']}")

    # ventana vacía de Depósito/Retiro
    def abrir_deposito_retiro():
        sub_win = tk.Toplevel(cuenta_win)
        sub_win.geometry("600x400")
        sub_win.title("Depósito / Retiro")
        sub_win.resizable(False, False)
        sub_win.transient(cuenta_win)
        sub_win.grab_set()
        sub_win.focus()
        tk.Label(sub_win, text="Ventana de Depósito/Retiro (a completar)", font=("Arial", 18, "bold")).pack(pady=50)

    # botones
    frame_btn = tk.Frame(cuenta_win)
    frame_btn.pack(pady=20)
    tk.Button(frame_btn, text="Deposito/Retiro", font=("Arial", 14, "bold"), command=abrir_deposito_retiro,
              bd=7, width=18,bg="red").grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Pago de servicios", font=("Arial", 14, "bold"),
              command=lambda: messagebox.showinfo("Info", "Próximamente..."), bd=7, width=18,bg="red").grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Compra de divisas", font=("Arial", 14, "bold"),
              command=lambda: messagebox.showinfo("Info", "Próximamente..."), bd=7, width=18,bg="red").grid(row=0, column=2, padx=10)
    tk.Button(frame_btn, text="Cerrar", font=("Arial", 14, "bold"), command=cuenta_win.destroy,
              bd=7, width=18,bg="red").grid(row=0, column=3, padx=10)
