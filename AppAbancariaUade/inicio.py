import tkinter as tk
from tkinter import messagebox
import json
import os #Para verificar que el archivo exista en el documento JSON
from pagina2 import abrir_pagina_cuenta

ARCHIVO_USUARIOS = "usuarios.json"

# Cargar datos de usuarios
if os.path.exists(ARCHIVO_USUARIOS):
    with open(ARCHIVO_USUARIOS, "r") as f:
        datos_guardados = json.load(f)
else:
    datos_guardados = []

ventana = tk.Tk()
ventana.geometry("800x600")
ventana.resizable(False, False)
ventana.title("Inicio")

# Validación: solo letras en Usuario
def solo_letras(caracter):
    return caracter.isalpha() or caracter == ""

vcmd = ventana.register(solo_letras)

# UI
titulo = tk.Label(ventana,text="Banco XML", font=("Arial", 22, "bold"))
titulo.configure(background="red",borderwidth=5,relief="solid")
titulo.pack(pady=(20, 40))

# Frame principal para los campos
frame_campos = tk.Frame(ventana)
frame_campos.pack(pady=30)

# Etiqueta ancho fijo para alinear todo
label_width = 12
entry_width = 25
pad_y = 15

# Usuario
tk.Label(frame_campos, text="Usuario:", font=("Arial", 14), width=label_width, anchor="e").grid(row=0, column=0, pady=pad_y)
user = tk.Entry(frame_campos, font=("Arial", 14), width=entry_width, validate="key", validatecommand=(vcmd, "%P"))
user.grid(row=0, column=1, pady=pad_y)

# Contraseña
tk.Label(frame_campos, text="Contraseña:", font=("Arial", 14), width=label_width, anchor="e").grid(row=1, column=0, pady=pad_y)
password = tk.Entry(frame_campos, font=("Arial", 14), width=entry_width, show="*")
password.grid(row=1, column=1, pady=pad_y)

# Legajo
tk.Label(frame_campos, text="Legajo:", font=("Arial", 14), width=label_width, anchor="e").grid(row=2, column=0, pady=pad_y)
legajo = tk.Entry(frame_campos, font=("Arial", 14), width=entry_width)
legajo.grid(row=2, column=1, pady=pad_y)


# Guardar o loguear
def guardar_datos():
    usuario_val = user.get().strip()
    pass_val = password.get().strip()
    legajo_val = legajo.get().strip()

    if not usuario_val or not pass_val or not legajo_val:
        messagebox.showwarning("Error", "Complete todos los campos.")
        return

    bancos_validos = {"100", "200", "300", "400"}
    if legajo_val not in bancos_validos:
        messagebox.showerror("Error", "El legajo no corresponde a ningún banco válido.")
        return

    # Buscar si el usuario ya existe
    usuario_existente = next((u for u in datos_guardados if u["usuario"] == usuario_val), None)

    if usuario_existente:
        if usuario_existente["password"] != pass_val:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            return
        # Logueo exitoso con cuenta existente
        abrir_pagina_cuenta(usuario_existente, datos_guardados, ventana, ARCHIVO_USUARIOS)
    else:
        # Crear nueva cuenta
        nuevo_usuario = {
            "usuario": usuario_val,
            "password": pass_val,
            "legajo": legajo_val,
            "saldo": 10000,
            "movimientos": ["Depósito inicial: $10000"]
        }
        datos_guardados.append(nuevo_usuario)
        with open(ARCHIVO_USUARIOS, "w") as f:
            json.dump(datos_guardados, f, indent=4)
        abrir_pagina_cuenta(nuevo_usuario, datos_guardados, ventana, ARCHIVO_USUARIOS)

    # Limpiar campos
    user.delete(0, tk.END)
    password.delete(0, tk.END)
    legajo.delete(0, tk.END)

# Botón Ingresar
btn = tk.Button(frame_campos, text="Ingresar", font=("Arial", 16, "bold"),
                command=guardar_datos, bd=2, width=12)
btn.configure(background="red", borderwidth=5, relief="solid")

# Lo colocamos en la misma columna que los Entry (columna 1), fila siguiente
btn.grid(row=3, column=1, pady=30)  # sticky="e" lo pega a la derecha


ventana.mainloop()
