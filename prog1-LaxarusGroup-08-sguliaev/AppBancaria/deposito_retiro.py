import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from datetime import datetime


def abrir_deposito_retiro(parent, cuenta, cuentas_file, movimientos_file):
    
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

    def save_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def cargar_bancos():
        bancos_dict = {}
        try:
            if os.path.exists("bancos.txt"):
                with open("bancos.txt", "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        linea = linea.strip()
                        if linea and "," in linea:
                            codigo, nombre = linea.split(",", 1)
                            bancos_dict[codigo.strip()] = nombre.strip()
            else:
                bancos_default = {
                    "001": "Banco Santander",
                    "002": "Banco Galicia",
                    "003": "Banco Nación",
                    "004": "Banco Macro",
                    "005": "BBVA",
                    "006": "Banco Ciudad"
                }
                with open("bancos.txt", "w", encoding="utf-8") as archivo:
                    for codigo, nombre in bancos_default.items():
                        archivo.write(f"{codigo},{nombre}\n")
                bancos_dict = bancos_default
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar bancos: {str(e)}")
        return bancos_dict

    def cargar_ubicaciones():
        ubicaciones_dict = {}
        try:
            if os.path.exists("ubicaciones.txt"):
                with open("ubicaciones.txt", "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        linea = linea.strip()
                        if linea and "," in linea:
                            partes = linea.split(",")
                            if len(partes) >= 3:
                                codigo_banco = partes[0].strip()
                                codigo_ubicacion = partes[1].strip()
                                nombre_ubicacion = partes[2].strip()
                                
                                if codigo_banco not in ubicaciones_dict:
                                    ubicaciones_dict[codigo_banco] = {}
                                
                                ubicaciones_dict[codigo_banco][codigo_ubicacion] = nombre_ubicacion
            else:
                ubicaciones_default = [
                    "001,U001,Palermo", "001,U002,Recoleta", "001,U003,Belgrano",
                    "002,U001,Villa Crespo", "002,U002,Caballito",
                    "003,U001,Microcentro", "003,U002,Once",
                    "004,U001,Almagro", "004,U002,Balvanera",
                    "005,U001,Retiro", "005,U002,San Nicolás",
                    "006,U001,Centro", "006,U002,Barrio Norte"
                ]
                with open("ubicaciones.txt", "w", encoding="utf-8") as archivo:
                    for linea in ubicaciones_default:
                        archivo.write(linea + "\n")
                
                for linea in ubicaciones_default:
                    partes = linea.split(",")
                    codigo_banco = partes[0].strip()
                    codigo_ubicacion = partes[1].strip()
                    nombre_ubicacion = partes[2].strip()
                    
                    if codigo_banco not in ubicaciones_dict:
                        ubicaciones_dict[codigo_banco] = {}
                    ubicaciones_dict[codigo_banco][codigo_ubicacion] = nombre_ubicacion
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ubicaciones: {str(e)}")
        return ubicaciones_dict

    def obtener_codigo_banco(nombre_banco, bancos_data):
        for codigo, nombre in bancos_data.items():
            if nombre == nombre_banco:
                return codigo
        return None

   
    bancos_data = cargar_bancos()
    ubicaciones_data = cargar_ubicaciones()
    
   
    root = tk.Toplevel(parent)
    root.title("Depositar y Retirar")
    root.geometry("500x550")
    root.resizable(False, False)
    root.transient(parent)
    root.grab_set()
    
    
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
   
    title_label = ttk.Label(main_frame, text="Sistema de Depósitos y Retiros", 
                        font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
   
    monto_var = tk.StringVar()
    operacion_var = tk.StringVar(value="depositar")
    banco_var = tk.StringVar()
    ubicacion_var = tk.StringVar()
    legajo_var = tk.StringVar()
    
    
    ttk.Label(main_frame, text="Monto ($):", font=("Arial", 10, "bold")).grid(
        row=1, column=0, sticky=tk.W, pady=5)
    monto_entry = ttk.Entry(main_frame, textvariable=monto_var, width=20)
    monto_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    
    ttk.Label(main_frame, text="Operación:", font=("Arial", 10, "bold")).grid(
        row=2, column=0, sticky=tk.W, pady=5)
    
    radio_frame = ttk.Frame(main_frame)
    radio_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    
    ttk.Label(main_frame, text="Banco:", font=("Arial", 10, "bold")).grid(
        row=3, column=0, sticky=tk.W, pady=5)
    nombres_bancos = list(bancos_data.values())
    banco_combo = ttk.Combobox(main_frame, textvariable=banco_var, 
                            values=nombres_bancos, state="readonly", width=18)
    banco_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    
    ubicacion_label = ttk.Label(main_frame, text="Ubicación:", font=("Arial", 10, "bold"))
    ubicacion_combo = ttk.Combobox(main_frame, textvariable=ubicacion_var, 
                                state="readonly", width=18)
    legajo_label = ttk.Label(main_frame, text="Legajo:", font=("Arial", 10, "bold"))
    legajo_entry = ttk.Entry(main_frame, textvariable=legajo_var, width=20)
    
    def cargar_ubicaciones_combo():
        """Carga las ubicaciones en el combo según el banco seleccionado"""
        banco_seleccionado = banco_var.get()
        
        print(f"🔍 Cargando ubicaciones para banco: '{banco_seleccionado}'")
        
        if not banco_seleccionado:
            print("⚠️ No hay banco seleccionado")
            ubicacion_combo['values'] = []
            ubicacion_var.set("")
            return
        
        codigo_banco = obtener_codigo_banco(banco_seleccionado, bancos_data)
        print(f"🏦 Código del banco: {codigo_banco}")
        
        if codigo_banco and codigo_banco in ubicaciones_data:
            ubicaciones_lista = list(ubicaciones_data[codigo_banco].values())
            print(f"📍 Ubicaciones encontradas: {ubicaciones_lista}")
            ubicacion_combo['values'] = ubicaciones_lista
            if ubicaciones_lista:
                ubicacion_var.set(ubicaciones_lista[0])
                print(f"✅ Ubicación seleccionada por defecto: {ubicaciones_lista[0]}")
        else:
            print(f"❌ No se encontraron ubicaciones para el código {codigo_banco}")
            ubicacion_combo['values'] = []
            ubicacion_var.set("")
    
    def cambiar_operacion():
        """Muestra u oculta campos según la operación seleccionada"""
        print(f"🔄 Cambiando operación a: {operacion_var.get()}")
        
        # Ocultar todos los campos opcionales
        ubicacion_label.grid_remove()
        ubicacion_combo.grid_remove()
        legajo_label.grid_remove()
        legajo_entry.grid_remove()
        
        # Mostrar campos según operación
        if operacion_var.get() == "retirar":
            print("💰 Mostrando campos para RETIRAR")
            ubicacion_label.grid(row=4, column=0, sticky=tk.W, pady=5)
            ubicacion_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
            # CLAVE: Cargar ubicaciones cuando se selecciona "Retirar"
            cargar_ubicaciones_combo()
        elif operacion_var.get() == "depositar_a":
            print("📤 Mostrando campos para DEPOSITAR A")
            legajo_label.grid(row=4, column=0, sticky=tk.W, pady=5)
            legajo_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def on_banco_change(event):
        """Se ejecuta cuando se cambia el banco"""
        print(f"🏦 Banco cambiado a: {banco_var.get()}")
        # CLAVE: Solo recargar ubicaciones si estamos en modo "retirar"
        if operacion_var.get() == "retirar":
            print("🔄 Recargando ubicaciones porque estamos en modo RETIRAR")
            cargar_ubicaciones_combo()
    
    # Vincular eventos
    banco_combo.bind("<<ComboboxSelected>>", on_banco_change)
    
    
    ttk.Radiobutton(radio_frame, text="Depositar", variable=operacion_var, 
                value="depositar", command=cambiar_operacion).pack(side=tk.LEFT)
    ttk.Radiobutton(radio_frame, text="Retirar", variable=operacion_var, 
                value="retirar", command=cambiar_operacion).pack(side=tk.LEFT, padx=(10, 0))
    ttk.Radiobutton(radio_frame, text="Depositar a", variable=operacion_var, 
                value="depositar_a", command=cambiar_operacion).pack(side=tk.LEFT, padx=(10, 0))
    
    
    resultado_frame = ttk.LabelFrame(main_frame, text="Resumen de la operación", padding="10")
    resultado_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))
    resultado_text = tk.Text(resultado_frame, height=8, width=50, wrap=tk.WORD)
    resultado_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    scrollbar = ttk.Scrollbar(resultado_frame, orient=tk.VERTICAL, command=resultado_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    resultado_text.config(yscrollcommand=scrollbar.set)
    
    def procesar_operacion_integrada():
        
        monto_texto = monto_var.get().strip()
        if not monto_texto or not monto_texto.replace('.', '').replace(',', '').isdigit():
            messagebox.showerror("Error", "Ingrese un monto válido")
            return
        
        monto = float(monto_texto.replace(',', '.'))
        
        if monto <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a 0")
            return
        
        
        if not banco_var.get():
            messagebox.showerror("Error", "Seleccione un banco")
            return
        
        
        cuentas = load_json(cuentas_file, [])
        movimientos = load_json(movimientos_file, {})
        idx = next((i for i, c in enumerate(cuentas) if c["usuario"] == cuenta["usuario"]), None)
        
        if idx is None:
            messagebox.showerror("Error", "Cuenta no encontrada")
            return
        
       
        if operacion_var.get() == "depositar":
            
            cuentas[idx]["saldo"] += monto
            movimientos.setdefault(cuenta["usuario"], []).append({
                "tipo": "deposito",
                "monto": monto,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nota": f"Depósito en {banco_var.get()}"
            })
            operacion_txt = "DEPÓSITO"
            
        elif operacion_var.get() == "retirar":
            if not ubicacion_var.get():
                messagebox.showerror("Error", "Seleccione una ubicación")
                return
            if cuentas[idx]["saldo"] < monto:
                messagebox.showerror("Error", "Saldo insuficiente")
                return
            cuentas[idx]["saldo"] -= monto
            movimientos.setdefault(cuenta["usuario"], []).append({
                "tipo": "retiro",
                "monto": monto,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nota": f"Retiro en {banco_var.get()} - {ubicacion_var.get()}"
            })
            operacion_txt = "RETIRO"
            
        elif operacion_var.get() == "depositar_a":
            if not legajo_var.get():
                messagebox.showerror("Error", "Ingrese el legajo destino")
                return
            if cuentas[idx]["saldo"] < monto:
                messagebox.showerror("Error", "Saldo insuficiente")
                return
            
            
            idx_destino = next((i for i, c in enumerate(cuentas) if c["legajo"] == legajo_var.get()), None)
            if idx_destino is None:
                messagebox.showerror("Error", "Legajo destino no encontrado")
                return
            
            
            cuentas[idx]["saldo"] -= monto
            cuentas[idx_destino]["saldo"] += monto
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            movimientos.setdefault(cuenta["usuario"], []).append({
                "tipo": "transferencia enviada",
                "monto": monto,
                "fecha": fecha,
                "nota": f"Transferencia a legajo {legajo_var.get()}"
            })
            movimientos.setdefault(cuentas[idx_destino]["usuario"], []).append({
                "tipo": "transferencia recibida",
                "monto": monto,
                "fecha": fecha,
                "nota": f"Transferencia de {cuenta['usuario']}"
            })
            operacion_txt = "TRANSFERENCIA"
        
       
        save_json(cuentas_file, cuentas)
        save_json(movimientos_file, movimientos)
        
      
        resultado_text.delete(1.0, tk.END)
        resultado = f"=== {operacion_txt} PROCESADO ===\n\n"
        resultado += f"Monto: ${monto}\n"
        resultado += f"Banco: {banco_var.get()}\n"
        if operacion_var.get() == "retirar":
            resultado += f"Ubicación: {ubicacion_var.get()}\n"
        elif operacion_var.get() == "depositar_a":
            resultado += f"Legajo destino: {legajo_var.get()}\n"
        resultado += f"\nSaldo actual: ${cuentas[idx]['saldo']}\n"
        resultado_text.insert(1.0, resultado)
        
        messagebox.showinfo("Éxito", f"{operacion_txt} procesado correctamente")
    
   
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=6, column=0, columnspan=2, pady=10)
    
    ttk.Button(button_frame, text="Procesar", command=procesar_operacion_integrada).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Cerrar", command=root.destroy).pack(side=tk.LEFT, padx=5)
    
    # Inicializar la interfaz
    cambiar_operacion()