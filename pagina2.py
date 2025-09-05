import tkinter as tk
from tkinter import messagebox

saldo = 10000
movimientos = ["Depósito inicial: $10000"]


def abrir_pagina_cuenta(usuario_val, datos_guardados):
    global saldo

    # Obtener últimos datos guardados
    ultimo = datos_guardados[-1]
    legajo = ultimo["legajo"]
    banco = identificar_banco(legajo)

    # Nueva ventana aparte
    cuenta = tk.Toplevel()
    cuenta.geometry("700x600")
    cuenta.title("Mi Cuenta")

    # Bienvenida y datos
    tk.Label(cuenta, text=f"Bienvenido {usuario_val}", font=("Arial", 20, "bold")).pack(pady=10)
    tk.Label(cuenta, text=f"Legajo: {legajo} | Banco: {banco}", font=("Arial", 14)).pack(pady=5)

    # Saldo
    saldo_label = tk.Label(cuenta, text=f"Saldo disponible: ${saldo}", font=("Arial", 18, "bold"))
    saldo_label.pack(pady=10)

    # Movimientos
    tk.Label(cuenta, text="Movimientos de cuenta:", font=("Arial", 16, "bold")).pack(pady=10)
    lista_mov = tk.Listbox(cuenta, font=("Arial", 14), width=50, height=8)
    lista_mov.pack()
    for mov in movimientos:
        lista_mov.insert(tk.END, mov)

    # Campo de monto
    frame_monto = tk.Frame(cuenta)
    frame_monto.pack(pady=15)
    tk.Label(frame_monto, text="Monto: $", font=("Arial", 14, "bold")).pack(side="left")
    monto_entry = tk.Entry(frame_monto, font=("Arial", 14), width=15)
    monto_entry.pack(side="left")

    # Funciones locales
    def depositar():
        global saldo
        try:
            monto = float(monto_entry.get())
            if monto <= 0:
                raise ValueError
            saldo += monto
            nuevo = f"Depósito: +${monto}"
            movimientos.append(nuevo)
            lista_mov.insert(tk.END, nuevo)
            saldo_label.config(text=f"Saldo disponible: ${saldo}")
            monto_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un monto válido.")

    def retirar():
        global saldo
        try:
            monto = float(monto_entry.get())
            if monto <= 0:
                raise ValueError
            if saldo >= monto:
                saldo -= monto
                nuevo = f"Retiro: -${monto}"
                movimientos.append(nuevo)
                lista_mov.insert(tk.END, nuevo)
                saldo_label.config(text=f"Saldo disponible: ${saldo}")
                monto_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Saldo insuficiente.")
        except ValueError:
            messagebox.showwarning("Error", "Ingrese un monto válido.")

    # Botones
    frame_btn = tk.Frame(cuenta)
    frame_btn.pack(pady=20)

    tk.Button(frame_btn, text="Depositar", font=("Arial", 14, "bold"),
              command=depositar, bd=4).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Retirar", font=("Arial", 14, "bold"),
              command=retirar, bd=4).grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Salir", font=("Arial", 14, "bold"),
              command=cuenta.destroy, bd=4).grid(row=0, column=2, padx=10)


def identificar_banco(legajo):
    bancos = {
        "100": "Banco Santander",
        "200": "BBVA",
        "300": "Banco Galicia",
        "400": "Banco Nación"
    }
    return bancos.get(legajo, "Banco no encontrado")
 