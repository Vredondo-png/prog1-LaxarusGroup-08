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


def abrir_pagina_cuenta(cuenta, cuentas_file, movimientos_file):
    """
    recibe:
      - cuenta: dict de la cuenta autenticada (usuario, password, legajo, saldo)
      - cuentas_file: path a cuentas.json
      - movimientos_file: path a movimientos.json
    """
    # recargar archivos por si cambiaron
    cuentas = load_json(cuentas_file, [])
    movimientos = load_json(movimientos_file, {})

    usuario = cuenta["usuario"]

    # asegurar clave en movimientos
    movimientos.setdefault(usuario, [])

    # index de la cuenta en la lista de cuentas (para guardar luego)
    idx = next((i for i, c in enumerate(cuentas) if c["usuario"] == usuario), None)
    if idx is None:
        messagebox.showerror("Error", "Cuenta no encontrada en archivo de cuentas.")
        return

    # ventana nueva
    cuenta_win = tk.Toplevel()
    cuenta_win.geometry("700x600")
    cuenta_win.title(f"Mi Cuenta - {usuario}")

    tk.Label(cuenta_win, text=f"Bienvenido {usuario}", font=("Arial", 20, "bold")).pack(pady=10)
    tk.Label(cuenta_win, text=f"Legajo: {cuenta['legajo']} | Banco: {identificar_banco(cuenta['legajo'])}", font=("Arial", 14)).pack(pady=5)

    saldo_var = tk.StringVar(value=f"${cuentas[idx]['saldo']}")
    saldo_label = tk.Label(cuenta_win, textvariable=saldo_var, font=("Arial", 18, "bold"))
    saldo_label.pack(pady=10)

    tk.Label(cuenta_win, text="Movimientos de cuenta:", font=("Arial", 16, "bold")).pack(pady=10)
    lista_mov = tk.Listbox(cuenta_win, font=("Arial", 14), width=60, height=10)
    lista_mov.pack()
    for mov in movimientos.get(usuario, []):
        lista_mov.insert(tk.END, f"{mov['fecha']} - {mov['tipo']} ${mov['monto']} - {mov.get('nota','')}")

    frame_monto = tk.Frame(cuenta_win)
    frame_monto.pack(pady=15)
    tk.Label(frame_monto, text="Monto: $", font=("Arial", 14, "bold")).pack(side="left")
    monto_entry = tk.Entry(frame_monto, font=("Arial", 14), width=15)
    monto_entry.pack(side="left")

    def add_mov(tipo, monto, nota=""):
        nonlocal cuentas, movimientos, idx, usuario
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mov = {"tipo": tipo, "monto": monto, "fecha": fecha, "nota": nota}
        movimientos.setdefault(usuario, []).append(mov)
        lista_mov.insert(tk.END, f"{fecha} - {tipo} ${monto} - {nota}")

        # actualizar saldo en cuentas y guardarlo en disco
        cuentas[idx]["saldo"] = round(float(cuentas[idx]["saldo"]) , 2)  # aseguramos float
        save_json_atomic(cuentas_file, cuentas)
        save_json_atomic(movimientos_file, movimientos)
        saldo_var.set(f"${cuentas[idx]['saldo']}")

    def depositar():
        try:
            monto = float(monto_entry.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un monto válido.")
            return
        # actualizar saldo en memoria y luego guardar
        cuentas[idx]["saldo"] = float(cuentas[idx]["saldo"]) + monto
        add_mov("depósito", monto, "Depósito desde app")
        monto_entry.delete(0, tk.END)

    def retirar():
        try:
            monto = float(monto_entry.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un monto válido.")
            return
        if float(cuentas[idx]["saldo"]) >= monto:
            cuentas[idx]["saldo"] = float(cuentas[idx]["saldo"]) - monto
            add_mov("retiro", monto, "Retiro desde app")
            monto_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Saldo insuficiente.")

    frame_btn = tk.Frame(cuenta_win)
    frame_btn.pack(pady=20)
    tk.Button(frame_btn, text="Depositar", font=("Arial", 14, "bold"), command=depositar, bd=4).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Retirar", font=("Arial", 14, "bold"), command=retirar, bd=4).grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Salir", font=("Arial", 14, "bold"), command=cuenta_win.destroy, bd=4).grid(row=0, column=2, padx=10)



