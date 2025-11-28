import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime
from cambio import programa_intercambio
from pago_servicios import pago_servicios
from deposito_retiro import abrir_deposito_retiro
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = os.path.dirname(__file__)


def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)



BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

def identificar_banco(legajo):
    bancos_file = os.path.join(BASE_DIR, "bancos.txt")
    print(f"Buscando archivo en: {bancos_file}") 
    
    if os.path.exists(bancos_file):
        with open(bancos_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(",", 1)
                if len(parts) != 2:
                    continue
                code, name = parts
                print(f"Comparando: '{code}' con '{legajo}'")  
                if code == str(legajo):  
                    return name
    else:
        print("Archivo bancos.txt no encontrado")
    return "Banco no encontrado"

def abrir_pagina_cuenta(cuenta, cuentas_file, movimientos_file, parent=None):
    
    cuentas = load_json(cuentas_file, [])
    movimientos = load_json(movimientos_file, {})
    usuario = cuenta["usuario"]
    movimientos.setdefault(usuario, [])

    idx = next((i for i, c in enumerate(cuentas) if c["usuario"] == usuario), None)
    if idx is None:
        messagebox.showerror("Error", "Cuenta no encontrada en archivo de cuentas.")
        return

    
    cuenta_win = tk.Toplevel(parent)
    cuenta_win.geometry("1200x700")
    cuenta_win.title(f"Mi Cuenta - {usuario}")
    cuenta_win.resizable(False, False)
    if parent:
        cuenta_win.transient(parent)
        cuenta_win.grab_set()
        cuenta_win.focus()

    
    tk.Label(cuenta_win, text=f"Bienvenido {usuario}", font=("Arial", 22, "bold")).pack(pady=10)
    
    
    banco_var = tk.StringVar()
    banco_var.set(f"Legajo: {cuenta['legajo']} | Banco: {identificar_banco(cuenta['legajo'])}")
    tk.Label(cuenta_win, textvariable=banco_var, font=("Arial", 16)).pack(pady=5)

    
    saldo_var = tk.StringVar()
    saldo_var.set(f"Saldo actual: ${round(float(cuenta['saldo']), 2)}")
    saldo_label = tk.Label(cuenta_win, textvariable=saldo_var, font=("Arial", 20, "bold"))
    saldo_label.pack(pady=10)

    
    tk.Label(cuenta_win, text="Movimientos de cuenta:", font=("Arial", 18, "bold")).pack(pady=10)
    
   
    frame_lista = tk.Frame(cuenta_win)
    frame_lista.pack(pady=5, padx=10, fill="both", expand=True)
    
    lista_mov = tk.Listbox(frame_lista, font=("Arial", 12), width=100, height=15)
    lista_mov.pack(side="left", fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(frame_lista, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    
    lista_mov.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_mov.yview)

   
    def actualizar_todo():
        try:
            print(f"🔄 ACTUALIZANDO DATOS PARA {usuario}")
            
           
            lista_mov.delete(0, tk.END)
            
            
            cuentas_actualizadas = load_json(cuentas_file, [])
            movimientos_actuales = load_json(movimientos_file, {})
            
           
            cuenta_actual = next((c for c in cuentas_actualizadas if c["usuario"] == usuario), None)
            if cuenta_actual:
                saldo_actual = float(cuenta_actual['saldo'])
                saldo_var.set(f"Saldo actual: ${round(saldo_actual, 2)}")
                print(f"💰 Saldo actualizado: ${saldo_actual}")
                
                
                if saldo_actual < 0:
                    saldo_label.config(fg="red")
                else:
                    saldo_label.config(fg="green")
            
           
            movimientos_usuario = movimientos_actuales.get(usuario, [])
            print(f"📊 Movimientos encontrados: {len(movimientos_usuario)}")
            
            if not movimientos_usuario:
                lista_mov.insert(tk.END, "--- No hay movimientos registrados ---")
                lista_mov.itemconfig(tk.END, {'fg': 'gray', 'font': ('Arial', 12, 'italic')})
                print("📭 No hay movimientos para mostrar")
            else:
                
                for mov in reversed(movimientos_usuario):
                    texto = f"{mov['fecha']} - {mov['tipo']}: ${float(mov['monto']):.2f}"
                    if mov.get('nota'):
                        texto += f" - {mov['nota']}"
                    
                    lista_mov.insert(tk.END, texto)
                    print(f"📝 Mostrando movimiento: {texto}")
                    
                    
                    tipo_lower = mov['tipo'].lower()
                    if any(palabra in tipo_lower for palabra in ['depósito', 'deposito', 'ingreso']):
                        lista_mov.itemconfig(tk.END, {'fg': 'green'})
                    elif any(palabra in tipo_lower for palabra in ['retiro', 'pago', 'débito', 'compra']):
                        lista_mov.itemconfig(tk.END, {'fg': 'red'})
                    else:
                        lista_mov.itemconfig(tk.END, {'fg': 'blue'})
            
           
            if movimientos_usuario:
                lista_mov.see(0)
                
        except Exception as e:
            print(f"❌ Error en actualizar_todo: {e}")
            import traceback
            traceback.print_exc()

 
    def forzar_actualizacion():
        """Fuerza una actualización completa"""
        print("🚀 FORZANDO ACTUALIZACIÓN COMPLETA")
        actualizar_todo()

    
    def actualizar_periodicamente():
        actualizar_todo()
        cuenta_win.after(1500, actualizar_periodicamente)


    actualizar_periodicamente()


    def abrir_deposito_retiro_wrapper():
        try:
            print("🎯 Abriendo ventana de Depósito/Retiro...")
            
            
            cuentas_actuales = load_json(cuentas_file, [])
            cuenta_actual = next((c for c in cuentas_actuales if c["usuario"] == usuario), None)
            
            if cuenta_actual is None:
                messagebox.showerror("Error", "No se encontró la cuenta")
                return
                
        
            abrir_deposito_retiro(
                parent=cuenta_win,
                cuenta=cuenta_actual,
                cuentas_file=cuentas_file,
                movimientos_file=movimientos_file,
            )
            
            
            print("🔄 Programando actualización después de depósito/retiro...")
            cuenta_win.after(2000, forzar_actualizacion)
            cuenta_win.after(4000, forzar_actualizacion)
            cuenta_win.after(6000, forzar_actualizacion)
            
        except Exception as e:
            print(f"❌ Error en depósito/retiro: {e}")
            messagebox.showerror("Error", f"Error al abrir depósito/retiro: {e}")

    
    def abrir_pago_servicios():
        try:
            print("🎯 Abriendo ventana de Pago de Servicios...")
            
           
            cuentas_actuales = load_json(cuentas_file, [])
            idx_actual = next((i for i, c in enumerate(cuentas_actuales) if c["usuario"] == usuario), None)
            
            if idx_actual is None:
                messagebox.showerror("Error", "No se encontró la cuenta")
                return
            
           
            pago_servicios(
                cuenta=cuentas_actuales[idx_actual],
                cuentas=cuentas_actuales,
                idx=idx_actual,
                cuentas_file=cuentas_file,
                movimientos=load_json(movimientos_file, {}),
                movimientos_file=movimientos_file,
            )
            
           
            print("🔄 Programando actualización después de pago de servicios...")
            cuenta_win.after(2000, forzar_actualizacion)
            cuenta_win.after(4000, forzar_actualizacion)
            cuenta_win.after(6000, forzar_actualizacion)
            
        except Exception as e:
            print(f"❌ Error en pago de servicios: {e}")
            messagebox.showerror("Error", f"Error al abrir pago de servicios: {e}")

   
    def abrir_compra_divisas():
        try:
            print("🎯 Abriendo ventana de Compra de Divisas...")
            
            
            cuentas_actuales = load_json(cuentas_file, [])
            cuenta_actual = next((c for c in cuentas_actuales if c["usuario"] == usuario), None)
            
            if cuenta_actual is None:
                messagebox.showerror("Error", "No se encontró la cuenta")
                return
                
            
            try:
                programa_intercambio(
                    parent=cuenta_win,
                    usuario=usuario,
                    cuenta=cuenta_actual,
                    cuentas_file=cuentas_file,
                    movimientos_file=movimientos_file,
                )
            except TypeError:
                try:
                    programa_intercambio(usuario)
                except:
                    programa_intercambio(parent=cuenta_win, usuario=usuario)
            
            
            print("🔄 Programando actualización después de compra de divisas...")
            cuenta_win.after(2000, forzar_actualizacion)
            cuenta_win.after(4000, forzar_actualizacion)
            cuenta_win.after(6000, forzar_actualizacion)
            
        except Exception as e:
            print(f"❌ Error en compra de divisas: {e}")
            messagebox.showerror("Error", f"Error al abrir compra de divisas: {e}")

    def imprimir_movimientos():
        """Genera un PDF y permite elegir dónde guardarlo"""
        try:
            # Cargar datos
            cuentas_actuales = load_json(cuentas_file, [])
            movimientos_actuales = load_json(movimientos_file, {})
            cuenta_actual = next((c for c in cuentas_actuales if c["usuario"] == usuario), None)
            
            if cuenta_actual is None:
                messagebox.showerror("Error", "No se encontró la cuenta")
                return
            
            # Ventana para elegir dónde guardar
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_sugerido = f"resumen_{usuario}_{fecha_actual}.pdf"
            
            ruta_archivo = filedialog.asksaveasfilename(
                title="Guardar resumen de cuenta",
                defaultextension=".pdf",
                initialfile=nombre_sugerido,
                filetypes=[("Archivo PDF", "*.pdf"), ("Todos los archivos", "*.*")]
            )
            
            # Si cancela, salir
            if not ruta_archivo:
                return
            
            # Crear PDF
            doc = SimpleDocTemplate(ruta_archivo, pagesize=A4)
            elementos = []
            styles = getSampleStyleSheet()
            
            # Título
            titulo = Paragraph("RESUMEN DE CUENTA BANCARIA", styles['Title'])
            elementos.append(titulo)
            elementos.append(Spacer(1, 0.3*inch))
            
            # Datos de cuenta
            saldo_actual = float(cuenta_actual['saldo'])
            datos = [
                ['Usuario:', usuario],
                ['Legajo:', cuenta_actual['legajo']],
                ['Banco:', identificar_banco(cuenta_actual['legajo'])],
                ['Saldo:', f"${saldo_actual:.2f}"],
                ['Fecha:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            tabla_cuenta = Table(datos, colWidths=[2*inch, 4*inch])
            tabla_cuenta.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
            ]))
            elementos.append(tabla_cuenta)
            elementos.append(Spacer(1, 0.4*inch))
            
            # Movimientos
            movimientos_usuario = movimientos_actuales.get(usuario, [])
            
            if movimientos_usuario:
                elementos.append(Paragraph("MOVIMIENTOS DE CUENTA", styles['Heading2']))
                elementos.append(Spacer(1, 0.2*inch))
                
                datos_mov = [['Fecha', 'Tipo', 'Monto', 'Nota']]
                for mov in reversed(movimientos_usuario):
                    nota = mov.get('nota', '-')
                    datos_mov.append([
                        mov['fecha'],
                        mov['tipo'],
                        f"${float(mov['monto']):.2f}",
                        nota[:25] + '...' if len(nota) > 25 else nota
                    ])
                
                tabla_mov = Table(datos_mov, colWidths=[1.8*inch, 1.8*inch, 1*inch, 1.8*inch])
                tabla_mov.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                ]))
                elementos.append(tabla_mov)
            else:
                elementos.append(Paragraph("No hay movimientos registrados.", styles['Normal']))
            
            # Generar PDF
            doc.build(elementos)
            
            messagebox.showinfo("Éxito", f"PDF guardado en:\n\n{ruta_archivo}")
            
        except ImportError:
            messagebox.showerror("Error", 
                               "No se encontró ReportLab.\n\n"
                               "Instala con: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {e}")

 
    frame_btn = tk.Frame(cuenta_win)
    frame_btn.pack(pady=20)

    tk.Button(frame_btn, text="Deposito/Retiro", font=("Arial", 14, "bold"),
              command=abrir_deposito_retiro_wrapper,
              bd=7, width=18, bg="red").grid(row=0, column=0, padx=10, pady=5)

    tk.Button(frame_btn, text="Pago de servicios", font=("Arial", 14, "bold"),
              command=abrir_pago_servicios, 
              bd=7, width=18, bg="red").grid(row=0, column=1, padx=10, pady=5)

    tk.Button(frame_btn, text="Compra de divisas", font=("Arial", 14, "bold"),
              command=abrir_compra_divisas,
              bd=7, width=18, bg="red").grid(row=0, column=2, padx=10, pady=5)

    tk.Button(frame_btn, text="Imprimir Resumen", font=("Arial", 14, "bold"),
              command=imprimir_movimientos,
              bd=7, width=18, bg="blue", fg="white").grid(row=1, column=1, padx=10, pady=5)

    tk.Button(frame_btn, text="Cerrar", font=("Arial", 14, "bold"), 
              command=cuenta_win.destroy,
              bd=7, width=18, bg="red").grid(row=1, column=2, padx=10, pady=5)

   
    def crear_boton_oculto():
        btn_actualizar = tk.Button(cuenta_win, text="🔃", font=("Arial", 8),
                                 command=forzar_actualizacion, width=2, height=1)
        btn_actualizar.place(relx=0.98, rely=0.02, anchor="ne")
    
    crear_boton_oculto()

   
    print("🚀 INICIANDO VENTANA DE CUENTA")
    actualizar_todo()

    
    def verificar_y_agregar_prueba():
        movimientos_actuales = load_json(movimientos_file, {})
        if usuario not in movimientos_actuales or len(movimientos_actuales[usuario]) == 0:
            print("📝 Agregando movimiento de prueba...")
            
            nuevo_movimiento = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tipo": "Apertura de cuenta",
                "monto": "0.00",
                "nota": "Bienvenido al sistema bancario"
            }
            movimientos_actuales.setdefault(usuario, []).append(nuevo_movimiento)
            save_json_atomic(movimientos_file, movimientos_actuales)
            forzar_actualizacion()

    cuenta_win.after(1000, verificar_y_agregar_prueba)