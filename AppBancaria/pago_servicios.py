import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime


def pago_servicios(cuenta, cuentas, idx, cuentas_file, movimientos, movimientos_file):
   
    
    def save_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    
    servicios = [
        ["100", "AYSA", 500],
        ["200", "Metrogas", 750],
        ["300", "Edesur", 620],
    ]

   
    metodos = ["Galicia", "BBVA", "MercadoPago", "Santander"]
    empresas_celular = ["Movistar", "Claro", "Personal", "Tuenti"]

    
    servicio_actual = None
    empresa_seleccionada = None
    numero_celular = None
    numero_sube = None

    
    def limpiar_pantalla():
        for widget in root.winfo_children():
            widget.pack_forget()

    def verificar_saldo(monto):
        
        return cuenta["saldo"] >= monto

    def descontar_saldo(monto, concepto):
        
        if not verificar_saldo(monto):
            messagebox.showerror("Error", "Saldo insuficiente")
            return False
        
        cuenta["saldo"] -= monto
        cuentas[idx]["saldo"] = cuenta["saldo"]
        
       
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mov = {"tipo": "pago", "monto": monto, "fecha": fecha, "nota": concepto}
        movimientos.setdefault(cuenta["usuario"], []).append(mov)
        
        
        save_json(cuentas_file, cuentas)
        save_json(movimientos_file, movimientos)
        
        return True

    
    def pagar_servicios():
        limpiar_pantalla()
        tk.Label(root, text="Ingrese el código de pago:", font=("Arial", 12)).pack(pady=5)
        codigo_entry.pack(pady=5)
        tk.Button(root, text="Continuar", command=continuar).pack(pady=5)
        tk.Button(root, text="Volver", command=mostrar_menu).pack(pady=5)

    def buscar_servicio(codigo):
        for s in servicios:
            if s[0] == codigo:
                return s
        return None

    def continuar():
        nonlocal servicio_actual
        codigo = codigo_entry.get()
        servicio_actual = buscar_servicio(codigo)

        if servicio_actual:
            limpiar_pantalla()
            nombre, monto = servicio_actual[1], servicio_actual[2]
            tk.Label(root, text=f"Servicio: {nombre}\nMonto: ${monto}", font=("Arial", 14)).pack(pady=10)
            tk.Label(root, text=f"Saldo actual: ${round(cuenta['saldo'],2)}", font=("Arial", 12)).pack(pady=5)
            
            if not verificar_saldo(monto):
                tk.Label(root, text="⚠️ SALDO INSUFICIENTE", font=("Arial", 12, "bold"), fg="red").pack(pady=5)
            
            for m in metodos:
                tk.Button(root, text=m, width=20, command=lambda m=m: pagar(m)).pack(pady=3)
            
            tk.Button(root, text="Volver", command=pagar_servicios).pack(pady=10)
        else:
            messagebox.showerror("Error", f"Código {codigo} no reconocido.")

    def pagar(metodo):
        monto = servicio_actual[2]
        nombre = servicio_actual[1]
        
        if not verificar_saldo(monto):
            messagebox.showerror("Error", "Saldo insuficiente para realizar el pago")
            return
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Pagar ${monto} con {metodo}?\n\nSaldo actual: ${cuenta['saldo']}\nSaldo después: ${cuenta['saldo'] - monto}")
        if confirmar:
            if descontar_saldo(monto, f"Pago {nombre}"):
                messagebox.showinfo("Éxito", f"Pago de ${monto} realizado con éxito\nNuevo saldo: ${cuenta['saldo']}")
                root.destroy()

   
    def recargar():
        limpiar_pantalla()
        tk.Label(root, text="Seleccione la empresa:", font=("Arial", 12)).pack(pady=5)
        for emp in empresas_celular:
            tk.Button(root, text=emp, width=20, command=lambda e=emp: pedir_numero_celular(e)).pack(pady=5)
        tk.Button(root, text="Volver", command=mostrar_menu).pack(pady=10)

    def pedir_numero_celular(empresa):
        nonlocal empresa_seleccionada
        empresa_seleccionada = empresa
        limpiar_pantalla()
        tk.Label(root, text=f"Empresa seleccionada: {empresa}", font=("Arial", 12)).pack(pady=5)
        tk.Label(root, text="Ingrese número de celular (10 dígitos):").pack(pady=5)
        recarga_numero.delete(0, tk.END)
        recarga_numero.pack(pady=5)
        tk.Button(root, text="Continuar", command=pedir_monto_celular).pack(pady=10)
        tk.Button(root, text="Volver", command=recargar).pack(pady=5)

    def pedir_monto_celular():
        nonlocal numero_celular
        numero_celular = recarga_numero.get()

        if not numero_celular.isdigit() or len(numero_celular) != 10:
            messagebox.showerror("Error", "Ingrese un número de celular válido (10 dígitos).")
            return

        limpiar_pantalla()
        tk.Label(root, text=f"Empresa: {empresa_seleccionada}", font=("Arial", 12)).pack(pady=5)
        tk.Label(root, text=f"Número: {numero_celular}", font=("Arial", 12)).pack(pady=5)
        tk.Label(root, text=f"Saldo actual: ${round(cuenta['saldo'],2)}", font=("Arial", 12)).pack(pady=5)
        tk.Label(root, text="Seleccione monto (1000 - 7000):", font=("Arial", 12)).pack(pady=5)

        montos = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
        for m in montos:
            btn = tk.Button(root, text=f"${m}", width=15, command=lambda monto=m: confirmar_recarga(monto))
            if not verificar_saldo(m):
                btn.config(state="disabled", bg="gray")
            btn.pack(pady=5)
        
        tk.Button(root, text="Volver", command=lambda: pedir_numero_celular(empresa_seleccionada)).pack(pady=10)

    def confirmar_recarga(monto):
        if not verificar_saldo(monto):
            messagebox.showerror("Error", "Saldo insuficiente para realizar la recarga")
            return
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Recargar ${monto} a {empresa_seleccionada} - {numero_celular}?\n\nSaldo actual: ${cuenta['saldo']}\nSaldo después: ${cuenta['saldo'] - monto}")
        if confirmar:
            if descontar_saldo(monto, f"Recarga {empresa_seleccionada} {numero_celular}"):
                messagebox.showinfo("Éxito", f"Recarga de ${monto} realizada con éxito\nNuevo saldo: ${cuenta['saldo']}")
                root.destroy()

    
    def cargar_sube():
        limpiar_pantalla()
        tk.Label(root, text="Ingrese número de SUBE (16 dígitos):", font=("Arial", 12)).pack(pady=5)
        sube_numero.delete(0, tk.END)
        sube_numero.pack(pady=5)
        tk.Button(root, text="Continuar", command=mostrar_montos_sube).pack(pady=10)
        tk.Button(root, text="Volver", command=mostrar_menu).pack(pady=5)

    def mostrar_montos_sube():
        nonlocal numero_sube
        numero_sube = sube_numero.get()

        if not numero_sube.isdigit() or len(numero_sube) != 16:
            messagebox.showerror("Error", "Ingrese un número de SUBE válido (16 dígitos).")
            return

        limpiar_pantalla()
        tk.Label(root, text=f"Número SUBE: {numero_sube}", font=("Arial", 12)).pack(pady=5)
        tk.Label(root, text=f"Saldo actual: ${round(cuenta['saldo'],2)}", font=("Arial", 12)).pack(pady=5)
        tk.Label(root, text="Seleccione un monto:", font=("Arial", 12)).pack(pady=5)

        montos = [2000, 3000, 4000, 5000, 6000, 7000]
        for m in montos:
            btn = tk.Button(root, text=f"${m}", width=15, command=lambda monto=m: confirmar_sube(monto))
            if not verificar_saldo(m):
                btn.config(state="disabled", bg="gray")
            btn.pack(pady=5)
        
        tk.Button(root, text="Volver", command=cargar_sube).pack(pady=10)

    def confirmar_sube(monto):
        if not verificar_saldo(monto):
            messagebox.showerror("Error", "Saldo insuficiente para realizar la carga")
            return
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Cargar SUBE {numero_sube} con ${monto}?\n\nSaldo actual: ${cuenta['saldo']}\nSaldo después: ${cuenta['saldo'] - monto}")
        if confirmar:
            if descontar_saldo(monto, f"Carga SUBE {numero_sube}"):
                messagebox.showinfo("Éxito", f"Carga SUBE de ${monto} realizada con éxito\nNuevo saldo: ${cuenta['saldo']}")
                root.destroy()

    def mostrar_menu():
        limpiar_pantalla()
        tk.Label(root, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=10)
        tk.Label(root, text=f"Saldo disponible: ${round(cuenta['saldo'],2)}", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(root, text="Pagar Servicios", width=25, command=pagar_servicios).pack(pady=10)
        tk.Button(root, text="Recargar Celular", width=25, command=recargar).pack(pady=10)
        tk.Button(root, text="Cargar SUBE", width=25, command=cargar_sube).pack(pady=10)
        tk.Button(root, text="Salir", width=25, command=root.destroy).pack(pady=10)

  
    root = tk.Tk()
    root.title("Sistema de Pagos")
    root.geometry("400x500")

   
    codigo_entry = tk.Entry(root, font=("Arial", 12))
    recarga_numero = tk.Entry(root, font=("Arial", 12))
    sube_numero = tk.Entry(root, font=("Arial", 12))

    
    mostrar_menu()

    root.mainloop()