import tkinter as tk
from tkinter import messagebox
import json

def abrir_pagina_cuenta(usuario, datos_guardados, ventana, archivo_json):
    cuenta = tk.Toplevel()
    cuenta.geometry("700x600")
    cuenta.title("Mi Cuenta")

    # Modal
    cuenta.transient(ventana)
    cuenta.grab_set()
    cuenta.focus_set()

    # Bienvenida
    tk.Label(cuenta, text=f"Bienvenido {usuario['usuario']}", font=("Arial", 20, "bold")).pack(pady=10)
    tk.Label(cuenta, text=f"Legajo: {usuario['legajo']} | Banco: {identificar_banco(usuario['legajo'])}",
             font=("Arial", 14)).pack(pady=5)

    # Saldo
    saldo_label = tk.Label(cuenta, text=f"Saldo disponible: ${usuario['saldo']}", font=("Arial", 18, "bold"))
    saldo_label.pack(pady=10)

    # Movimientos
    tk.Label(cuenta, text="Movimientos de cuenta:", font=("Arial", 16, "bold")).pack(pady=10)
    lista_mov = tk.Listbox(cuenta, font=("Arial", 14), width=50, height=8)
    lista_mov.pack()
    for mov in usuario["movimientos"]:
        lista_mov.insert(tk.END, mov)

    # Campo de monto
    frame_monto = tk.Frame(cuenta); frame_monto.pack(pady=15)
    tk.Label(frame_monto, text="Monto: $", font=("Arial", 14, "bold")).pack(side="left")
    monto_entry = tk.Entry(frame_monto, font=("Arial", 14), width=15)
    monto_entry.pack(side="left")

    # Funciones
    def guardar_json():
        with open(archivo_json, "w") as f:
            json.dump(datos_guardados, f, indent=4)

    def depositar():
        try:
            monto = float(monto_entry.get())
            if monto <= 0: raise ValueError
            usuario["saldo"] += monto
            nuevo = f"Depósito: +${monto}"
            usuario["movimientos"].append(nuevo)
            lista_mov.insert(tk.END, nuevo)
            saldo_label.config(text=f"Saldo disponible: ${usuario['saldo']}")
            monto_entry.delete(0, tk.END)
            guardar_json()
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un monto válido.")

    def retirar():
        try:
            monto = float(monto_entry.get())
            if monto <= 0: raise ValueError
            if usuario["saldo"] >= monto:
                usuario["saldo"] -= monto
                nuevo = f"Retiro: -${monto}"
                usuario["movimientos"].append(nuevo)
                lista_mov.insert(tk.END, nuevo)
                saldo_label.config(text=f"Saldo disponible: ${usuario['saldo']}")
                monto_entry.delete(0, tk.END)
                guardar_json()
            else:
                messagebox.showwarning("Error", "Saldo insuficiente.")
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un monto válido.")

    # Botones
    frame_btn = tk.Frame(cuenta); frame_btn.pack(pady=20)
    tk.Button(frame_btn, text="Depositar", font=("Arial", 14, "bold"),
              command=depositar, bd=4).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Retirar", font=("Arial", 14, "bold"),
              command=retirar, bd=4).grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Cerrar sesión", font=("Arial", 14, "bold"),
              command=lambda: (guardar_json(), cuenta.destroy()), bd=4).grid(row=0, column=2, padx=10)

def identificar_banco(legajo):
    bancos = {
        "100": "Banco Santander",
        "200": "BBVA",
        "300": "Banco Galicia",
        "400": "Banco Nación"
    }
    return bancos.get(legajo, "Banco no encontrado")
