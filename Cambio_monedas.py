from tkinter import *
from tkinter import ttk
import tkinter as tk

# Funcion para comprobar input
def corregir_input():
    allowed_symbols='0123456789.'
    current_str_value = entry_amount1.get()
    if current_str_value == '':
        var_amount2.set(value=0.0)
        return False
    if current_str_value[0] == '.':
        return False
    for char in current_str_value:
        if char not in allowed_symbols:
            current_str_value = current_str_value.replace(char, '')
    if '.' not in current_str_value:
        current_str_value = current_str_value + ".0"
    if current_str_value.count(".") == 2:
        var_amount1.set(value=current_str_value[:current_str_value.index('.')+1]) 
    new_float_value = float(current_str_value)
    var_amount1.set(value=new_float_value)

# Funcion para obtener tasa
def get_currency(moneda):
    for i in range(len(monedas)):
        if moneda == monedas[i]:
            return currency[i]

# Funcion para mostrar tasas
def display_tasa():
    moneda1 = var_moneda1.get()
    moneda2 = var_moneda2.get()
    if moneda1 == "ARS":
        amount2 = 1 * get_currency(moneda2)
    elif moneda2 == "ARS":
        amount2 = 1 / get_currency(moneda1)
    else:
        amount2 = 1 / get_currency(moneda1) * get_currency(moneda2)
    var_currency.set(f"1 {var_moneda1.get()} = {amount2} {var_moneda2.get()}")

#  Funcion para recalcular intercambio
def recalcular_intercambio():
    moneda1 = var_moneda1.get()
    moneda2 = var_moneda2.get()
    amount1 = var_amount1.get()
    if moneda1 == "ARS":
        amount2 = amount1 * get_currency(moneda2)
    elif moneda2 == "ARS":
        amount2 = amount1 / get_currency(moneda1)
    else:
        amount2 = amount1 / get_currency(moneda1) * get_currency(moneda2)
    var_amount2.set(value=amount2)

# Funcion en caso de que entry cambiado
def on_entry_change(var, index, mode): 
    corregir_input()
    if  var_amount1.get() > get_displayed_saldo():
        info_window = tk.Toplevel(root)
        info_window.title("Information")
        info_label = tk.Label(info_window, text="La cantidad ingresada supera su saldo actual")
        info_label.pack(padx=20, pady=20)
        close_button = ttk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack(pady=10)
        var_amount1.set(value=get_displayed_saldo())
    recalcular_intercambio()

# Funcion para recalcular intercambio
def on_combobox_changed(event):
    var_displayed_saldo.set(value=set_displayed_saldo())
    if var_moneda1.get() == var_moneda2.get() or var_moneda2.get() == '':
        var_moneda2.set(value='')
        var_currency.set(f"1 {var_moneda1.get()} = ")
    else:
        display_tasa()
        recalcular_intercambio()

# Funcion para obtener current saldo depende de moneda elegida
def get_displayed_saldo():
    for i in range(len(monedas)):
        if var_moneda1.get() == monedas[i]:
            return saldos[i]
        
def get_saldo(moneda):
    for i in range(len(monedas)):
        if moneda == monedas[i]:
            return saldos[i]

# Funcion para configurar texto de currnet saldo
def set_displayed_saldo():
    #var_displayed_saldo.set(value=f"Saldo: {var_moneda1.get()} {str(get_displayed_saldo())}")
    return f"Saldo: {var_moneda1.get()} {str(get_displayed_saldo())}"

# Funcion para ejecutar intercambio
def intercambiar():
    
    resultado_text.insert("1.0", f"{var_moneda1.get()} {var_amount1.get()} ----> {var_moneda2.get()} {var_amount2.get()}\n")
    if  var_amount1.get() > get_displayed_saldo():
        info_window = tk.Toplevel(root)
        info_window.title("Information")
        info_label = tk.Label(info_window, text="La cantidad ingresada supera su saldo actual")
        info_label.pack(padx=20, pady=20)
        close_button = ttk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack(pady=10)
        var_amount1.set(value=get_displayed_saldo())
    else:
        for i in range(len(saldos)):
            if monedas[i] == var_moneda1.get():
                saldos[i] = saldos[i] - var_amount1.get()
            elif monedas[i] == var_moneda2.get():
                saldos[i] = saldos[i] + var_amount2.get()
        resultado_text.insert(2.0,f"Saldo actual:\n")
        resultado_text.insert(3.0,f"ARS: {str(get_saldo('ARS'))}\n")
        resultado_text.insert(4.0,f"USD: {str(get_saldo('USD'))}\n")     
        resultado_text.insert(5.0,f"EUR: {str(get_saldo('EUR'))}\n")
        resultado_text.insert(6.0,f"BRL: {str(get_saldo('BRL'))}\n")
        resultado_text.insert(7.0,"-------------------------------\n")
        var_displayed_saldo.set(value=set_displayed_saldo())

    if get_displayed_saldo() == 0.0:
        var_amount1.set(value=0.0)

# Crear ventana principal
root = tk.Tk()
root.title("Depositar y Retirar")
root.geometry("500x500")
root.resizable(False, False)

# Título
title_label = tk.Label(root, text="Sistema de Intercambio de monedas", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Frame principal
main_frame = tk.Frame(root)
main_frame.pack(pady=10)

# Listas
monedas = ['ARS', 'USD', 'EUR', 'BRL']
currency = [1.0, 0.00074, 0.00064, 0.0040]
saldos = [9999.0, 34.0, 2456.0, 1000.0]

# Variables
var_moneda1 = tk.StringVar()
var_moneda2 = tk.StringVar()
var_amount1 = tk.DoubleVar(value=0.0)
var_amount2 = tk.DoubleVar(value=0.0)
var_displayed_saldo = tk.StringVar()
var_currency = tk.StringVar(value=f"1 ARS = {currency[1]} USD")

# Combobox Moneda №1
combobox_moneda1 = ttk.Combobox(main_frame, textvariable=var_moneda1, values=monedas, state='readonly', width=5)
combobox_moneda1.current(0)
combobox_moneda1.grid(row=0, column=0, pady=0, padx=10)
combobox_moneda1.bind("<<ComboboxSelected>>", on_combobox_changed)

# Entry Amount №1
entry_amount1 = ttk.Entry(main_frame, textvariable=var_amount1)
entry_amount1.grid(row=0, column=1, pady=0, padx=10)
var_amount1.trace_add("write", on_entry_change)

# Label Saldo
var_displayed_saldo.set(value=set_displayed_saldo())
label_saldo = ttk.Label(main_frame, textvariable=var_displayed_saldo, font=("Arial", 8, "italic"))
label_saldo.grid(row=1, column=1, padx=10, sticky='W')

# Combobox Moneda №2
combobox_moneda2 = ttk.Combobox(main_frame, textvariable=var_moneda2, values=monedas, state='readonly', width=5)
combobox_moneda2.current(1)
combobox_moneda2.grid(row=2, column=0, pady=10, padx=10)
combobox_moneda2.bind("<<ComboboxSelected>>", on_combobox_changed)

# Label Amount №2
label_amount2 = tk.Label(main_frame, textvariable=var_amount2, bg="White", width=20, anchor="w")
label_amount2.grid(row=2, column=1, pady=10, padx=10)

# Label Currency
label_currency = tk.Label(root, textvariable=var_currency, bg="SlateGray1")
label_currency.pack()

# Botones
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

button_ejecutar = ttk.Button(button_frame, text="Ejecutar", command=intercambiar)
button_ejecutar.grid(row=0, column=0)

button_clear = ttk.Button(button_frame, text="Limpiar", command = lambda : resultado_text.delete(1.0, tk.END))
button_clear.grid(row=0, column=1)

button_cerrar = ttk.Button(button_frame, text="Cerrar", command = lambda : root.destroy())
button_cerrar.grid(row=0, column=2)

# Frame para resultado
frame_resultado = tk.LabelFrame(root, text="Resumen de la operación")
frame_resultado.pack()

resultado_text = tk.Text(frame_resultado, height=10, width=50, wrap=tk.WORD)
resultado_text.grid(row=0, column=0)

# Scrollbar para el texto
scrollbar = tk.Scrollbar(frame_resultado, orient=tk.VERTICAL, command=resultado_text.yview)
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
resultado_text.config(yscrollcommand=scrollbar.set)

root.mainloop()