import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)


def abrir_deposito_retiro(parent, cuenta, cuentas_file, movimientos_file, on_update=None):
    """
    parent: ventana padre
    cuenta: dict del usuario actual
    cuentas_file, movimientos_file: rutas a los archivos
    on_update: callback para refrescar la UI principal cuando se hacen cambios
    """

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

    def save_json_atomic(path, data):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)

    def cargar_bancos():
        bancos_dict = {}
        bancos_path = os.path.join(BASE_DIR, "bancos.txt")
        try:
            if os.path.exists(bancos_path):
                with open(bancos_path, "r", encoding="utf-8") as archivo:
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
                with open(bancos_path, "w", encoding="utf-8") as archivo:
                    for codigo, nombre in bancos_default.items():
                        archivo.write(f"{codigo},{nombre}\n")
                bancos_dict = bancos_default
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar bancos: {str(e)}")
        return bancos_dict

    def cargar_ubicaciones():
        ubicaciones_dict = {}
        ubicaciones_path = os.path.join(BASE_DIR, "ubicaciones.txt")
        try:
            if os.path.exists(ubicaciones_path):
                with open(ubicaciones_path, "r", encoding="utf-8") as archivo:
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
                ubicaciones_path = os.path.join(BASE_DIR, "ubicaciones.txt")
                with open(ubicaciones_path, "w", encoding="utf-8") as archivo:
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

    # ===== CARGAR DATOS =====
    bancos_data = cargar_bancos()
    ubicaciones_data = cargar_ubicaciones()

    # ===== CREAR VENTANA =====
    root = tk.Toplevel(parent)
    root.title("Depositar y Retirar")
    root.geometry("500x500")
    root.resizable(False, False)
    # modal
    if parent:
        root.transient(parent)
        root.grab_set()
        root.focus()

    # Frame principal
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Título
    title_label = ttk.Label(main_frame, text="Sistema de Depósitos y Retiros",
                            font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Variables
    monto_var = tk.StringVar()
    operacion_var = tk.StringVar(value="depositar")
    banco_var = tk.StringVar()
    ubicacion_var = tk.StringVar()
    legajo_var = tk.StringVar()

    # Monto
    ttk.Label(main_frame, text="Monto ($):", font=("Arial", 10, "bold")).grid(
        row=1, column=0, sticky=tk.W, pady=5)
    monto_entry = ttk.Entry(main_frame, textvariable=monto_var, width=20)
    monto_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

    # Tipo de operación
    ttk.Label(main_frame, text="Operación:", font=("Arial", 10, "bold")).grid(
        row=2, column=0, sticky=tk.W, pady=5)

    radio_frame = ttk.Frame(main_frame)
    radio_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)

    # Elementos dinámicos
    ubicacion_label = ttk.Label(main_frame, text="Ubicación:", font=("Arial", 10, "bold"))
    ubicacion_combo = ttk.Combobox(main_frame, textvariable=ubicacion_var,
                                   state="readonly", width=18)
    legajo_label = ttk.Label(main_frame, text="Legajo:", font=("Arial", 10, "bold"))
    legajo_entry = ttk.Entry(main_frame, textvariable=legajo_var, width=20)

    def cambiar_operacion():
        ubicacion_label.grid_remove()
        ubicacion_combo.grid_remove()
        legajo_label.grid_remove()
        legajo_entry.grid_remove()

        if operacion_var.get() == "retirar":
            ubicacion_label.grid(row=4, column=0, sticky=tk.W, pady=5)
            ubicacion_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
            actualizar_ubicaciones()
        elif operacion_var.get() == "depositar_a":
            legajo_label.grid(row=4, column=0, sticky=tk.W, pady=5)
            legajo_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)

    def actualizar_ubicaciones():
        banco_seleccionado = banco_var.get()
        if banco_seleccionado:
            codigo_banco = obtener_codigo_banco(banco_seleccionado, bancos_data)
            if codigo_banco and codigo_banco in ubicaciones_data:
                ubicaciones_nombres = list(ubicaciones_data[codigo_banco].values())
                ubicacion_combo.config(values=ubicaciones_nombres)
                ubicacion_var.set("")
            else:
                ubicacion_combo.config(values=[])
                ubicacion_var.set("")

    # Radiobuttons
    ttk.Radiobutton(radio_frame, text="Depositar", variable=operacion_var,
                    value="depositar", command=cambiar_operacion).pack(side=tk.LEFT)
    ttk.Radiobutton(radio_frame, text="Retirar", variable=operacion_var,
                    value="retirar", command=cambiar_operacion).pack(side=tk.LEFT, padx=(10, 0))
    ttk.Radiobutton(radio_frame, text="Depositar a", variable=operacion_var,
                    value="depositar_a", command=cambiar_operacion).pack(side=tk.LEFT, padx=(10, 0))

    # Banco
    ttk.Label(main_frame, text="Banco:", font=("Arial", 10, "bold")).grid(
        row=3, column=0, sticky=tk.W, pady=5)
    nombres_bancos = list(bancos_data.values())
    banco_combo = ttk.Combobox(main_frame, textvariable=banco_var,
                               values=nombres_bancos, state="readonly", width=18)
    banco_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    banco_combo.bind("<<ComboboxSelected>>", lambda e: actualizar_ubicaciones())

    # Resultado
    resultado_frame = ttk.LabelFrame(main_frame, text="Resumen de la operación", padding="10")
    resultado_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky=(tk.W, tk.E))
    resultado_text = tk.Text(resultado_frame, height=8, width=50, wrap=tk.WORD)
    resultado_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
    scrollbar = ttk.Scrollbar(resultado_frame, orient=tk.VERTICAL, command=resultado_text.yview)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    resultado_text.config(yscrollcommand=scrollbar.set)

    # ===== FUNCION PRINCIPAL =====
    def procesar_operacion_integrada():
        # Validar monto
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

        # Cargar datos actuales
        cuentas = load_json(cuentas_file, [])
        movimientos = load_json(movimientos_file, {})
        idx_local = next((i for i, c in enumerate(cuentas) if c["usuario"] == cuenta["usuario"]), None)
        if idx_local is None:
            messagebox.showerror("Error", "Cuenta no encontrada")
            return

        # Procesar según operación
        if operacion_var.get() == "depositar":
            cuentas[idx_local]["saldo"] = round(float(cuentas[idx_local].get("saldo", 0)) + monto, 2)
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
            if cuentas[idx_local]["saldo"] < monto:
                messagebox.showerror("Error", "Saldo insuficiente")
                return
            cuentas[idx_local]["saldo"] = round(float(cuentas[idx_local]["saldo"]) - monto, 2)
            movimientos.setdefault(cuenta["usuario"], []).append({
                "tipo": "retiro",
                "monto": monto,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nota": f"Retiro en {banco_var.get()} - {ubicacion_var.get()}"
            })
            operacion_txt = "RETIRO"

        elif operacion_var.get() == "depositar_a":
            if not legajo_var.get().strip():
                messagebox.showerror("Error", "Ingrese el legajo destino")
                return

            legajo_destino = legajo_var.get().strip()
            destino_idx = next((i for i, c in enumerate(cuentas) if c["legajo"] == legajo_destino), None)
            if destino_idx is None:
                messagebox.showerror("Error", "No se encontró una cuenta con ese legajo.")
                return
            if destino_idx == idx_local:
                messagebox.showerror("Error", "No puede transferirse a sí mismo.")
                return
            if cuentas[idx_local]["saldo"] < monto:
                messagebox.showerror("Error", "Saldo insuficiente para transferir.")
                return

            cuentas[idx_local]["saldo"] = round(float(cuentas[idx_local]["saldo"]) - monto, 2)
            cuentas[destino_idx]["saldo"] = round(float(cuentas[destino_idx].get("saldo", 0)) + monto, 2)

            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            movimientos.setdefault(cuenta["usuario"], []).append({
                "tipo": "transferencia_salida",
                "monto": monto,
                "fecha": fecha_actual,
                "nota": f"Transferencia a legajo {legajo_destino}"
            })
            movimientos.setdefault(cuentas[destino_idx]["usuario"], []).append({
                "tipo": "transferencia_entrada",
                "monto": monto,
                "fecha": fecha_actual,
                "nota": f"Recibido de legajo {cuenta['legajo']}"
            })
            operacion_txt = f"TRANSFERENCIA a legajo {legajo_destino}"

        else:
            messagebox.showerror("Error", "Seleccione una operación válida.")
            return

        # Guardar datos de forma atómica
        save_json_atomic(cuentas_file, cuentas)
        save_json_atomic(movimientos_file, movimientos)

        # Mostrar resumen
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Operación: {operacion_txt}\n")
        resultado_text.insert(tk.END, f"Monto: ${monto}\n")
        resultado_text.insert(tk.END, f"Banco: {banco_var.get()}\n")
        if operacion_var.get() == "retirar":
            resultado_text.insert(tk.END, f"Ubicación: {ubicacion_var.get()}\n")
        if operacion_var.get() == "depositar_a":
            resultado_text.insert(tk.END, f"Legajo destino: {legajo_var.get()}\n")
        resultado_text.insert(tk.END, "\n¡Operación completada exitosamente!")

        messagebox.showinfo("Éxito", "Operación realizada correctamente.")

        # 🔁 Actualizar saldo en ventana principal
        if on_update:
            try:
                on_update()
            except Exception:
                pass

    # Botones
    ttk.Button(main_frame, text="Ejecutar operación", command=procesar_operacion_integrada).grid(
        row=6, column=0, columnspan=2, pady=(10, 10)
    )
    ttk.Button(main_frame, text="Cerrar", command=root.destroy).grid(
        row=7, column=0, columnspan=2, pady=(5, 0)
    )
