import tkinter as tk
from tkinter import messagebox
import pagina2  # importamos la segunda ventana

# Lista global
datos_guardados = []


def identificar_banco(legajo):
    bancos = {
        "100": "Banco Santander",
        "200": "BBVA",
        "300": "Banco Galicia",
        "400": "Banco Nación"
    }
    return bancos.get(legajo, "Banco no encontrado")


def guardar_datos():
    usuario_val = user.get()
    pass_val = password.get()
    legajo_val = lega.get()

    if not usuario_val or not pass_val or not legajo_val:
        messagebox.showwarning("Error", "Complete todos los campos.")
        return

    # Guardar datos
    datos_guardados.append({
        "usuario": usuario_val,
        "password": pass_val,
        "legajo": legajo_val
    })

    # Mostrar banco
    banco = identificar_banco(legajo_val)
    messagebox.showinfo("Resultado", f"Usuario: {usuario_val}\nBanco: {banco}")

    # Abrir segunda ventana
    pagina2.abrir_pagina_cuenta(usuario_val, datos_guardados)


# ---------------- INTERFAZ LOGIN ---------------- #
ventana = tk.Tk()
ventana.geometry("600x500")
ventana.resizable(False, False)
ventana.title("Login - Grupo XML")

titulo = tk.Label(ventana, text="GRUPO XML", font=("Arial", 18, "bold"))
titulo.pack(pady=(20, 40))

info = tk.Label(ventana, text="Bienvenido al GRUPO XML.\n"
                              "Trabajamos con Banco Galicia, Santander,\nBBVA, Banco Nación entre otros.",
                font=("Arial", 14))
info.pack(pady=(20, 60))

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

# Botón
tk.Button(ventana, text="Ingresar", font=("Arial", 16, "bold"), bd=4, command=guardar_datos).pack(pady=20)

ventana.mainloop()
 