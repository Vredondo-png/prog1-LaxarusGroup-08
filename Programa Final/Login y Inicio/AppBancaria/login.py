import tkinter as tk
from tkinter import messagebox
import json
import os
import inicio
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CUENTAS_FILE = os.path.join(BASE_DIR, "cuentas.json")
MOVIMIENTOS_FILE = os.path.join(BASE_DIR, "movimientos.json")
TXT_FILE = os.path.join(BASE_DIR, "datos_por_defecto.txt")

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

# === Función para leer cuentas desde TXT ===
def cargar_cuentas_desde_txt(path):
    cuentas = []
    if not os.path.exists(path):
        return cuentas
    with open(path, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(",")
            if len(partes) == 4:
                usuario, password, legajo, saldo = partes
                cuentas.append({
                    "usuario": usuario,
                    "password": password,
                    "legajo": legajo,
                    "saldo": int(saldo)
                })
    return cuentas

# === Cargar cuentas y generar movimientos iniciales ===
default_cuentas = cargar_cuentas_desde_txt(TXT_FILE)
default_movs = {
    c["usuario"]: [
        {"tipo": "deposito", "monto": c["saldo"], "fecha": "2025-01-08 00:00:00", "nota": "Depósito inicial"}
    ] for c in default_cuentas
}

# === Cargar o crear archivos principales ===
cuentas = load_json(CUENTAS_FILE, default_cuentas)
movimientos = load_json(MOVIMIENTOS_FILE, default_movs)

# Asegurar que cada cuenta tenga movimientos
for c in cuentas:
    movimientos.setdefault(c["usuario"], [])

# === Función de login ===
def guardar_datos(user_entry, password_entry, lega_entry):
    usuario_val = user_entry.get().strip()
    pass_val = password_entry.get().strip()
    legajo_val = lega_entry.get().strip()

    if not usuario_val or not pass_val or not legajo_val:
        messagebox.showwarning("Error", "Complete todos los campos.")
        return

    cuenta = next((c for c in cuentas if c["usuario"] == usuario_val), None)
    if not cuenta:
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

# === INTERFAZ LOGIN ===
ventana = tk.Tk()
ventana.geometry("800x800")
ventana.resizable(False, False)
ventana.title("Login - Grupo XML")

# Imagen (logo)
imagen_path = os.path.join(BASE_DIR, "IMG/foto.jpg")
if os.path.exists(imagen_path):
    img = Image.open(imagen_path)
    img = img.resize((200, 200))
    imagen_tk = ImageTk.PhotoImage(img)
    label_imagen = tk.Label(ventana, image=imagen_tk)
    label_imagen.pack(pady=(20, 10))

# Texto principal
tk.Label(ventana, text="GRUPO XML", font=("Arial", 18, "bold")).pack(pady=(5, 20))
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
tk.Button(
    ventana,
    text="Ingresar",
    font=("Arial", 16, "bold"),
    bd=7,
    bg="red",
    command=lambda: guardar_datos(user, password, lega)
).pack(pady=20)

ventana.mainloop()
