# --- IMPORT DE BIBLIOTECAS ---
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import pygame
import time
import os
from collections import Counter

# Librerías nuevas requeridas por la entrega
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE SONIDO ---
try:
    pygame.mixer.init()
    # nombre del archivo de audio (asegúrate que esté en la misma carpeta)
    pygame.mixer.music.load("cafe-music-163375.mp3")
    pygame.mixer.music.play(-1)
    print("🎵 Música de fondo iniciada correctamente.")
except Exception as e:
    print(f"No se pudo reproducir la música: {e}")

# --- DATOS DE LA APLICACIÓN ---
menu = {
    "Café Americano": 2.50,
    "Latte": 3.00,
    "Croissant": 1.75,
    "Pastel de Chocolate": 4.50,
    "Té Verde": 2.25
}

pedido_actual = []
total_actual = 0.0
num_pedido = 0
historial_clientes = []  # lista de diccionarios con nombre, pedido y total

CSV_FILENAME = "historial_cafe_unal.csv"


# --- FUNCIONES ---
def agregar_producto(producto):
    """Agrega un producto a la orden actual y actualiza el total en consola."""
    global total_actual
    pedido_actual.append(producto)
    total_actual += menu[producto]
    print(f"Añadido: {producto.upper()} | Total actual: ${total_actual:.2f}")


def guardar_historial_csv():
    """Guarda el historial_clientes a CSV usando pandas (convierte listas de 'pedido' a strings)."""
    try:
        if not historial_clientes:
            # Si no hay datos, borrar el archivo si existe o no hacer nada.
            return
        df = pd.DataFrame(historial_clientes)
        # Convertir listas a cadena para facilitar lectura en CSV
        if "pedido" in df.columns:
            df["pedido"] = df["pedido"].apply(lambda lst: ";".join(lst) if isinstance(lst, list) else str(lst))
        df.to_csv(CSV_FILENAME, index=False)
        print(f"Historial guardado en {CSV_FILENAME}")
    except Exception as e:
        print("Error guardando CSV:", e)


def mostrar_total():
    """Finaliza el pedido: pide nombre, registra en historial, guarda CSV y muestra confirmación."""
    global total_actual, pedido_actual, num_pedido, historial_clientes
    if pedido_actual:
        nombre_cliente = simpledialog.askstring("Nombre del cliente", "Por favor, ingresa tu nombre:")
        if nombre_cliente:
            num_pedido += 1
            print(f"Pedido #{num_pedido} → {pedido_actual} | Total: ${total_actual:.2f}")
            print(f"Cliente: {nombre_cliente} ☕✨")

            # Guardar en historial (almacen en memoria)
            historial_clientes.append({
                "nombre": nombre_cliente,
                "pedido": pedido_actual.copy(),
                "total": total_actual
            })

            # Guardar CSV actualizado
            guardar_historial_csv()

            messagebox.showinfo(
                "Pedido completado",
                f"Gracias por tu compra, {nombre_cliente}!\n\nTotal: ${total_actual:.2f}"
            )

            # Reset de la orden en memoria (para nueva orden)
            total_actual = 0.0
            pedido_actual = []
        else:
            messagebox.showwarning("Atención", "Debes ingresar un nombre para completar el pedido.")
    else:
        messagebox.showerror("Error", "No has pedido nada. :c")


def resetear_orden():
    """Reinicia la orden actual (no afecta el historial guardado)."""
    global total_actual, pedido_actual
    pedido_actual = []
    total_actual = 0.0
    print("Se ha reseteado tu pedido ☕")
    messagebox.showinfo("Reinicio", "Tu pedido ha sido reiniciado.")


def ver_historial():
    """Muestra una ventana con el historial de clientes (lectura desde memoria)."""
    if not historial_clientes:
        messagebox.showinfo("Historial vacío", "Aún no hay clientes registrados.")
        return

    historial_win = tk.Toplevel(ventana)
    historial_win.title("Historial de Clientes")
    historial_win.geometry("500x380")
    historial_win.configure(bg="#f8f4ed")

    ttk.Label(historial_win, text="Historial de Clientes", font=("Helvetica", 16, "bold")).pack(pady=10)

    text_area = tk.Text(historial_win, wrap="word", height=15, width=60)
    text_area.pack(padx=10, pady=10)

    for cliente in historial_clientes:
        pedido_str = ", ".join(cliente['pedido']) if isinstance(cliente['pedido'], list) else str(cliente['pedido'])
        text_area.insert(
            tk.END,
            f"{cliente['nombre']} - Pedido: {pedido_str} | Total: ${cliente['total']:.2f}\n"
        )

    text_area.config(state="disabled")


def ver_diagrama():
    """
    Función existente que dibuja dos gráficos sencillos en un Canvas:
    - Productos más vendidos (barras)
    - Productos comprados por cliente (barras)
    Sigue usando los datos en memoria (historial_clientes).
    """
    if not historial_clientes:
        messagebox.showinfo("Sin datos", "Aún no hay información para graficar.")
        return

    # --- Recolectar datos ---
    productos_todos = []
    clientes = []
    cantidad_por_cliente = []

    for cliente in historial_clientes:
        productos_todos.extend(cliente["pedido"])
        clientes.append(cliente["nombre"])
        cantidad_por_cliente.append(len(cliente["pedido"]))

    conteo_productos = Counter(productos_todos)

    # --- Ventana del diagrama ---
    diag_win = tk.Toplevel(ventana)
    diag_win.title("📊 Diagrama de Ventas")
    diag_win.geometry("950x750")
    diag_win.configure(bg="#f5f0e6")

    ttk.Label(diag_win, text="Análisis de Ventas - Café UNAL", font=("Helvetica", 22, "bold")).pack(pady=10)

    canvas = tk.Canvas(diag_win, bg="white", width=900, height=640, highlightthickness=0)
    canvas.pack(pady=10)

    # --- Configuración general ---
    margen_izq = 100
    max_bar_height = 200
    bar_width = 70
    espacio_barras = 60

    # ===============================
    # GRÁFICO 1: PRODUCTOS MÁS VENDIDOS
    # ===============================
    canvas.create_text(450, 50, text="Productos más vendidos", font=("Helvetica", 15, "bold"))

    y_base1 = 300
    productos = list(conteo_productos.keys())
    ventas = list(conteo_productos.values())

    if not productos:
        productos = ["—"]
        ventas = [0]

    max_vendidos = max(ventas) if ventas else 1
    total_ancho1 = len(productos) * (bar_width + espacio_barras)
    start_x1 = (900 - total_ancho1) / 2 + 30  # centrado automático

    for i, (producto, cantidad) in enumerate(zip(productos, ventas)):
        bar_height = (cantidad / max_vendidos) * max_bar_height
        x0 = start_x1 + i * (bar_width + espacio_barras)
        y0 = y_base1 - bar_height
        canvas.create_rectangle(x0, y0, x0 + bar_width, y_base1, fill="#a97453", outline="")
        canvas.create_text(x0 + bar_width / 2, y0 - 15, text=str(cantidad), font=("Helvetica", 11, "bold"), fill="#3e2723")
        canvas.create_text(x0 + bar_width / 2, y_base1 + 25, text=producto, font=("Helvetica", 10))

    # --- Separador entre los dos gráficos ---
    canvas.create_line(80, 340, 820, 340, fill="#bbb", width=2)
    canvas.create_text(450, 370, text="Productos comprados por cliente", font=("Helvetica", 15, "bold"))

    # ===============================
    # GRÁFICO 2: CLIENTES ATENDIDOS
    # ===============================
    y_base2 = 640  # base inferior del segundo gráfico
    max_cliente = max(cantidad_por_cliente) if cantidad_por_cliente else 1
    total_ancho2 = len(clientes) * (bar_width + espacio_barras)
    start_x2 = (900 - total_ancho2) / 2 + 30  # centrado automático

    for i, (cliente, cantidad) in enumerate(zip(clientes, cantidad_por_cliente)):
        bar_height = (cantidad / max_cliente) * max_bar_height
        x0 = start_x2 + i * (bar_width + espacio_barras)
        y0 = y_base2 - bar_height - 30  # subir un poco las barras
        canvas.create_rectangle(x0, y0, x0 + bar_width, y_base2 - 30, fill="#6d4c41", outline="")
        # número encima
        canvas.create_text(x0 + bar_width / 2, y0 - 15, text=str(cantidad), font=("Helvetica", 11, "bold"), fill="#3e2723")
        #  nombre del cliente bien visible
        canvas.create_text(x0 + bar_width / 2, y_base2 - 10, text=cliente, font=("Helvetica", 10, "bold"))


def ver_grafico_matplotlib():
    """
    Genera un gráfico profesional con Matplotlib mostrando los productos más vendidos.
    Usa pandas internamente para procesar los datos (aunque la fuente principal es historial_clientes).
    """
    if not historial_clientes:
        messagebox.showinfo("Sin datos", "Aún no hay compras registradas.")
        return

    try:
        df = pd.DataFrame(historial_clientes)
        # Expandir la columna "pedido" (que es lista) y contar valores
        productos = []
        for lista in df["pedido"]:
            productos.extend(lista)
        conteo = pd.Series(productos).value_counts()

        plt.figure(figsize=(8, 5))
        conteo.plot(kind="bar")
        plt.title("Productos más vendidos - Café UNAL")
        plt.xlabel("Producto")
        plt.ylabel("Cantidad Vendida")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error al generar gráfico", f"Ocurrió un error: {e}")


# --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Cafetería - Universidad Nacional")
ventana.geometry("750x600")
ventana.configure(bg="#f5f0e6")

# --- POSTER DIGITAL (PITCH VISUAL) ---
poster_frame = tk.Frame(ventana, bg="#f7f3ed", relief="flat")
poster_frame.pack(fill="x", pady=15)

# Logo centrado
logo_path = "logo.png"
try:
    logo_img = Image.open(logo_path).resize((180, 180))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(poster_frame, image=logo_photo, bg="#f7f3ed")
    logo_label.image = logo_photo
    logo_label.pack(pady=(10, 5))
except Exception:
    logo_label = tk.Label(poster_frame, text="☕", font=("Helvetica", 60), bg="#f7f3ed")
    logo_label.pack(pady=(10, 5))

# Título principal
titulo_pitch = tk.Label(
    poster_frame,
    text="CAFÉ UNAL - Tu momento, tu café",
    font=("Helvetica", 22, "bold"),
    bg="#f7f3ed",
    fg="#3e2723"
)
titulo_pitch.pack()

# --- MENÚ DE PRODUCTOS ---
titulo_label = ttk.Label(ventana, text="Menú de Cafetería", font=("Helvetica", 18, "bold"))
titulo_label.pack(pady=10)

menu_frame = ttk.Frame(ventana)
menu_frame.pack(pady=10)

ttk.Button(menu_frame, text="Café Americano", command=lambda: agregar_producto("Café Americano")).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(menu_frame, text="Latte", command=lambda: agregar_producto("Latte")).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(menu_frame, text="Croissant", command=lambda: agregar_producto("Croissant")).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(menu_frame, text="Pastel de Chocolate", command=lambda: agregar_producto("Pastel de Chocolate")).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(menu_frame, text="Té Verde", command=lambda: agregar_producto("Té Verde")).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(menu_frame, text="Completar Orden", command=mostrar_total).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(menu_frame, text="Intentar de nuevo", command=resetear_orden).grid(row=3, column=0, padx=5, pady=5)

# --- BOTONES EXTRA ---
extra_frame = ttk.Frame(ventana)
extra_frame.pack(pady=15)

ttk.Button(extra_frame, text="📜 Ver Historial de Clientes", command=ver_historial).grid(row=0, column=0, padx=10)
ttk.Button(extra_frame, text="📊 Ver Diagrama de Ventas", command=ver_diagrama).grid(row=0, column=1, padx=10)
ttk.Button(extra_frame, text="📈 Ver gráfico (Matplotlib)", command=ver_grafico_matplotlib).grid(row=1, column=0, padx=10, pady=6)

# --- ANIMACIÓN DE TAZA ---
try:
    taza_img = Image.open("coffee.png").resize((80, 80))
    taza_photo = ImageTk.PhotoImage(taza_img)
    taza_label = tk.Label(ventana, image=taza_photo, bg="#f5f0e6")
    taza_label.place(x=0, y=500)
except Exception:
    taza_label = tk.Label(ventana, text="☕", font=("Arial", 40), bg="#f5f0e6")
    taza_label.place(x=0, y=500)


def mover_taza():
    x = 0
    direccion = 1
    while True:
        if x >= 650:
            direccion = -1
        elif x <= 0:
            direccion = 1
        x += direccion * 5
        taza_label.place(x=x, y=500)
        time.sleep(0.05)


threading.Thread(target=mover_taza, daemon=True).start()

# --- INICIAR LA APP ---
# Si existe CSV previo, opcionalmente podemos precargarlo al iniciar para tener historial persistente:
if os.path.exists(CSV_FILENAME):
    try:
        df_prev = pd.read_csv(CSV_FILENAME)
        # Intentar reconstruir historial_clientes desde CSV (la columna 'pedido' está como "a;b;c")
        historial_clientes = []
        for _, row in df_prev.iterrows():
            pedidos = []
            if "pedido" in row and not pd.isna(row["pedido"]):
                # esperar formato "item1;item2;item3"
                pedidos = [p for p in str(row["pedido"]).split(";") if p != ""]
            nombre = row["nombre"] if "nombre" in row and not pd.isna(row["nombre"]) else "Anónimo"
            total = float(row["total"]) if "total" in row and not pd.isna(row["total"]) else 0.0
            historial_clientes.append({"nombre": nombre, "pedido": pedidos, "total": total})
        print(f"Se cargaron {len(historial_clientes)} registros desde {CSV_FILENAME}")
    except Exception as e:
        print("No se pudo cargar historial previo:", e)

ventana.mainloop()

