import tkinter as tk
from tkinter import ttk

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

# --- FUNCIONES ---
def agregar_producto(producto):
    """Añade un producto al pedido y actualiza el total."""
    global total_actual 
    # se usa  'global' para modificar la variable fuera de la funcion
    
    pedido_actual.append(producto)
    total_actual += menu[producto]
    
    print(f"Añadido: {producto}")
     # se imprime en la terminal para depurar
    print(f"Pedido actual: {pedido_actual}")
    print(f"Total actual: ${total_actual:.2f}")
    
    # Actualizar la interfaz gráfica para mostrar el pedido
    actualizar_pedido_display()

def actualizar_pedido_display():
    """Actualiza el widget de texto que muestra el pedido actual."""
    pedido_texto.delete(1.0, tk.END)  # Limpiar el contenido anterior
    
    if pedido_actual:
        for producto in pedido_actual:
            precio = menu[producto]
            pedido_texto.insert(tk.END, f"• {producto} - ${precio:.2f}\n")
    else:
        pedido_texto.insert(tk.END, "No hay productos en el pedido")

def mostrar_total():
    """Formatea y muestra el total en la interfaz."""
    # Actualizar la etiqueta del total en la ventana
    total_label.config(text=f"Total: ${total_actual:.2f}")
    print(f"El total final a mostrar es: ${total_actual:.2f}")

def limpiar_pedido():
    """Limpia el pedido actual y reinicia el total."""
    global pedido_actual, total_actual
    pedido_actual = []
    total_actual = 0.0
    actualizar_pedido_display()
    total_label.config(text="Total: $0.00")
    print("Pedido limpiado")

# --- CONFIGURACION DE LA VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Cafetería  - Universidad Nacional ")
ventana.geometry("700x500")

# --- WIDGETS DE LA INTERFAZ ---

# Titulo
titulo_label = ttk.Label(ventana, text="Menú de Cafeteria", font=("Helvetica", 18, "bold"))
titulo_label.pack(pady=10)

# Frame para los botones del menu (para organizarlos mejor)
menu_frame = ttk.Frame(ventana)
menu_frame.pack(pady=10)

# Se crea un boton para cada item del menú
# El comando 'lambda' es necesario para pasar un argumento a la funcion
ttk.Button(menu_frame, text="Café Americano", command=lambda: agregar_producto("Café Americano")).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(menu_frame, text="Latte", command=lambda: agregar_producto("Latte")).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(menu_frame, text="Croissant", command=lambda: agregar_producto("Croissant")).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(menu_frame, text="Pastel de Chocolate", command=lambda: agregar_producto("Pastel de Chocolate")).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(menu_frame, text="Té Verde", command=lambda: agregar_producto("Té Verde")).grid(row=2, column=0, padx=5, pady=5)

# --- WIDGETS AÑADIDOS ---

# 1. Etiqueta para "Tu Pedido"
pedido_titulo = ttk.Label(ventana, text="Tu Pedido:", font=("Helvetica", 14, "bold"))
pedido_titulo.pack(pady=(20, 5))

# 2. Widget de Texto para mostrar el pedido_actual
pedido_frame = ttk.Frame(ventana)
pedido_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

pedido_texto = tk.Text(pedido_frame, height=8, width=60, font=("Helvetica", 10))
pedido_scrollbar = ttk.Scrollbar(pedido_frame, orient=tk.VERTICAL, command=pedido_texto.yview)
pedido_texto.configure(yscrollcommand=pedido_scrollbar.set)

pedido_texto.grid(row=0, column=0, sticky="nsew")
pedido_scrollbar.grid(row=0, column=1, sticky="ns")

pedido_frame.grid_rowconfigure(0, weight=1)
pedido_frame.grid_columnconfigure(0, weight=1)

# Frame para los botones de control
control_frame = ttk.Frame(ventana)
control_frame.pack(pady=15)

# 3. Botón para "Calcular Total"
calcular_btn = ttk.Button(control_frame, text="Calcular Total", command=mostrar_total)
calcular_btn.grid(row=0, column=0, padx=10)

# Botón adicional para limpiar el pedido
limpiar_btn = ttk.Button(control_frame, text="Limpiar Pedido", command=limpiar_pedido)
limpiar_btn.grid(row=0, column=1, padx=10)

# 4. Etiqueta final para mostrar el resultado del total
total_label = ttk.Label(ventana, text="Total: $0.00", font=("Helvetica", 16, "bold"), foreground="blue")
total_label.pack(pady=10)

# Iniciar la aplicación
ventana.mainloop()