import tkinter as tk
from tkinter import messagebox
import json
import os
import inicio

# BASE_DIR apunta al directorio donde están los archivos .py y los json/txt
BASE_DIR = os.path.dirname(__file__)
CUENTAS_FILE = os.path.join(BASE_DIR, "cuentas.json")
MOVIMIENTOS_FILE = os.path.join(BASE_DIR, "movimientos.json")


def load_json(path, default):
    if not os.path.exists(path):
        # crear archivo con contenido por defecto
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Archivos por defecto (si no existen)
default_cuentas = [
    {"usuario": "alice", "password": "alice123", "legajo": "100", "saldo": 10000},
    {"usuario": "bob",   "password": "bob123",   "legajo": "200", "saldo": 5000},
    {"usuario": "carol", "password": "carol123", "legajo": "300", "saldo": 7500},
    {"usuario": "david", "password": "david123", "legajo": "400", "saldo": 2000},
    {"usuario": "eva",   "password": "eva123",   "legajo": "100", "saldo": 1500}
]
default_movs = {acct["usuario"]: [
    {"tipo": "deposito", "monto": acct["saldo"], "fecha": "2025-01-08 00:00:00", "nota": "Depósito inicial"}
] for acct in default_cuentas}

cuentas = load_json(CUENTAS_FILE, default_cuentas)
movimientos = load_json(MOVIMIENTOS_FILE, default_movs)
# garantizar clave para cada usuario
for c in cuentas:
    movimientos.setdefault(c["usuario"], [])


def identificar_banco(legajo):
    bancos = {
        "100": "Banco Santander",
        "200": "BBVA",
        "300": "Banco Galicia",
        "400": "Banco Nación"
    }
    return bancos.get(legajo, "Banco no encontrado")


def guardar_datos():
    usuario_val = user.get().strip()
    pass_val = password.get().strip()
    legajo_val = lega.get().strip()

    if not usuario_val or not pass_val or not legajo_val:
        messagebox.showwarning("Error", "Complete todos los campos.")
        return

    # buscar cuenta
    cuenta = next((c for c in cuentas if c["usuario"] == usuario_val), None)
    if cuenta is None:
        messagebox.showerror("Acceso denegado", "Usuario no encontrado.")
        return

    if cuenta["password"] != pass_val:
        messagebox.showerror("Acceso denegado", "Contraseña incorrecta.")
        return

    if cuenta["legajo"] != legajo_val:
        messagebox.showerror("Acceso denegado", "Legajo no corresponde a la cuenta.")
        return

    # Abrir ventana de cuenta como modal
    inicio.abrir_pagina_cuenta(cuenta, CUENTAS_FILE, MOVIMIENTOS_FILE, parent=ventana)


# --- INTERFAZ LOGIN --- #
ventana = tk.Tk()
ventana.geometry("800x800")
ventana.resizable(False, False)
ventana.title("Login - Grupo XML")

# Texto principal
tk.Label(ventana, text="GRUPO XML", font=("Arial", 24, "bold")).pack(pady=(40, 20))
tk.Label(ventana, text="Bienvenido al GRUPO XML.\nTrabajamos con Banco Galicia, Santander,\nBBVA, Banco Nación entre otros.",
         font=("Arial", 14)).pack(pady=(5, 30))

# Usuario
frame_usuario = tk.Frame(ventana)
frame_usuario.pack(pady=10)
tk.Label(frame_usuario, text="Usuario: ", font=("Arial", 14, "bold")).pack(side="left")
user = tk.Entry(frame_usuario, font=("Arial", 14), width=25)
user.pack(side="left")

# Contraseña
frame_contra = tk.Frame(ventana)
frame_contra.pack(pady=10)
tk.Label(frame_contra, text="Contraseña: ", font=("Arial", 14, "bold")).pack(side="left")
password = tk.Entry(frame_contra, font=("Arial", 14), width=25, show="*")
password.pack(side="left")

# Legajo
frame_legajo = tk.Frame(ventana)
frame_legajo.pack(pady=10)
tk.Label(frame_legajo, text="Legajo: ", font=("Arial", 14, "bold")).pack(side="left")
lega = tk.Entry(frame_legajo, font=("Arial", 14), width=25)
lega.pack(side="left")

# Botón ingresar
tk.Button(ventana, text="Ingresar", font=("Arial", 16, "bold"), bd=7, bg="red", command=guardar_datos).pack(pady=20)

ventana.mainloop()
