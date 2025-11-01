from tkinter import *
from tkinter import ttk
import tkinter as tk
from pathlib import Path
import json
from tkinter import messagebox
import os

BASE_DIR = os.path.dirname(__file__)


def programa_intercambio(parent, usuario, on_update=lambda: None):
    """
    Ventana modal para intercambio de monedas.
    parent: ventana padre
    usuario: nombre de usuario (string)
    on_update: callback para ejecutar después de guardar cambios
    """

    file_path = os.path.join(BASE_DIR, "cuentas.json")
    try:
        cuentas_lista = json.loads(open(file_path, encoding="utf-8").read())
    except Exception:
        messagebox.showerror("Error", "No se pudo leer cuentas.json")
        return

    indx = None
    for i, u in enumerate(cuentas_lista):
        if u['usuario'] == usuario:
            indx = i
            break
    if indx is None:
        messagebox.showerror("Error", "Usuario no encontrado")
        return
    user = cuentas_lista[indx]

    # Tasas de conversión relativas a ARS (valores estáticos - modificables)
    currency = {"ARS": 1.0, "USD": 0.00074, "EUR": 0.00064, "BRL": 0.0040}

    root = tk.Toplevel(parent)
    root.title("Intercambio de Monedas")
    root.geometry("500x350")
    root.resizable(False, False)
    # modal
    if parent:
        root.transient(parent)
        root.grab_set()
        root.focus()

    var_moneda1 = tk.StringVar(value="ARS")
    var_moneda2 = tk.StringVar(value="USD")
    var_amount1 = tk.DoubleVar(value=0.0)
    var_amount2 = tk.DoubleVar(value=0.0)
    var_displayed_saldo = tk.StringVar()
    var_currency = tk.StringVar(value=f"1 ARS = {currency['USD']} USD")

    def get_displayed_saldo():
        return user.get('saldo', 0) if var_moneda1.get() == "ARS" else user.get(f"saldo_{var_moneda1.get()}", 0)

    def set_displayed_saldo():
        return f"Saldo: {round(get_displayed_saldo(),2)} {var_moneda1.get()}"

    def corregir_input():
        try:
            f = float(var_amount1.get())
        except Exception:
            f = 0.0
        if f > get_displayed_saldo():
            f = get_displayed_saldo()
        var_amount1.set(f)
        recalcular_intercambio()

    def get_currency(moneda):
        return currency[moneda]

    def recalcular_intercambio():
        m1 = var_moneda1.get()
        m2 = var_moneda2.get()
        a1 = var_amount1.get()
        if m1 == m2:
            a2 = a1
        elif m1 == "ARS":
            a2 = a1 * get_currency(m2)
        elif m2 == "ARS":
            a2 = a1 / get_currency(m1)
        else:
            a2 = a1 / get_currency(m1) * get_currency(m2)
        var_amount2.set(round(a2, 2))

    def on_entry_change(*args):
        corregir_input()

    def on_combobox_changed(event):
        if var_moneda1.get() == var_moneda2.get():
            var_currency.set(f"1 {var_moneda1.get()} = 1 {var_moneda2.get()}")
        else:
            m1, m2 = var_moneda1.get(), var_moneda2.get()
            if m1 == "ARS":
                amount2 = 1 * get_currency(m2)
            elif m2 == "ARS":
                amount2 = 1 / get_currency(m1)
            else:
                amount2 = 1 / get_currency(m1) * get_currency(m2)
            var_currency.set(f"1 {m1} = {round(amount2,4)} {m2}")
        var_displayed_saldo.set(set_displayed_saldo())
        recalcular_intercambio()

    def intercambiar():
        a1 = float(var_amount1.get())
        a2 = float(var_amount2.get())
        if a1 <= 0:
            messagebox.showerror("Error", "Ingrese un monto mayor a 0")
            return
        if a1 > get_displayed_saldo():
            messagebox.showerror("Error", "Saldo insuficiente")
            return

        tipo_saldo1 = "saldo" if var_moneda1.get() == "ARS" else f"saldo_{var_moneda1.get()}"
        tipo_saldo2 = "saldo" if var_moneda2.get() == "ARS" else f"saldo_{var_moneda2.get()}"

        # Aplicar cambios en la estructura en memoria
        user[tipo_saldo1] = round(float(user.get(tipo_saldo1, 0)) - a1, 4)
        user[tipo_saldo2] = round(float(user.get(tipo_saldo2, 0)) + a2, 4)
        cuentas_lista[indx] = user

        # Guardar en archivo de forma atómica
        tmp = file_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cuentas_lista, f, ensure_ascii=False, indent=4)
        os.replace(tmp, file_path)

        # llamar callback para actualizar UI principal
        try:
            on_update()
        except Exception:
            pass

        var_displayed_saldo.set(set_displayed_saldo())
        messagebox.showinfo("Éxito", f"Intercambio completado: {round(a1,2)} {var_moneda1.get()} → {round(a2,2)} {var_moneda2.get()}")

    # Layout
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, padx=10)

    ttk.Label(main_frame, text="De:").grid(row=0, column=0, sticky="w")
    cb1 = ttk.Combobox(main_frame, textvariable=var_moneda1, values=list(currency.keys()), state='readonly', width=6)
    cb1.grid(row=0, column=1, padx=5)
    cb1.bind("<<ComboboxSelected>>", on_combobox_changed)

    entry1 = ttk.Entry(main_frame, textvariable=var_amount1, width=12)
    entry1.grid(row=0, column=2, padx=5)
    var_amount1.trace_add("write", on_entry_change)

    ttk.Label(main_frame, text="Saldo:").grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(main_frame, textvariable=var_displayed_saldo).grid(row=1, column=1, columnspan=2, sticky="w")
    var_displayed_saldo.set(set_displayed_saldo())

    ttk.Label(main_frame, text="A:").grid(row=2, column=0, sticky="w", pady=(10,0))
    cb2 = ttk.Combobox(main_frame, textvariable=var_moneda2, values=list(currency.keys()), state='readonly', width=6)
    cb2.grid(row=2, column=1, padx=5)
    cb2.bind("<<ComboboxSelected>>", on_combobox_changed)

    tk.Label(main_frame, textvariable=var_amount2, width=20, bg="White", anchor="w").grid(row=2, column=2, padx=5)

    tk.Label(root, textvariable=var_currency, bg="SlateGray1").pack(fill='x', pady=8)
    ttk.Button(root, text="Ejecutar", command=intercambiar).pack(pady=8)
    ttk.Button(root, text="Cerrar", command=root.destroy).pack(pady=(0, 8))
