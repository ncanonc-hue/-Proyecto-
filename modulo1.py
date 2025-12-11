import tkinter as tk
from tkinter import messagebox

# --- DATOS ---
menu = {
    "Café Americano": 2.50,
    "Latte": 3.00,
    "Croissant": 1.75
}

pedido = []
total = 0.0

def agregar(producto):
    global total
    pedido.append(producto)
    total += menu[producto]
    messagebox.showinfo("Producto añadido", f"{producto} añadido.\nTotal: ${total:.2f}")

def finalizar():
    global pedido, total
    if not pedido:
        messagebox.showerror("Error", "No hay productos en el pedido.")
        return
    resumen = ", ".join(pedido)
    messagebox.showinfo("Pedido Finalizado", f"Pedido: {resumen}\nTotal: ${total:.2f}")
    pedido = []
    total = 0.0

def main():
    win = tk.Tk()
    win.title("Módulo 1 - Cafetería (versión básica)")
    win.geometry("350x350")

    tk.Label(win, text="Menú Básico", font=("Arial", 18)).pack(pady=10)

    tk.Button(win, text="Café Americano $2.50", command=lambda: agregar("Café Americano")).pack(pady=5)
    tk.Button(win, text="Latte $3.00", command=lambda: agregar("Latte")).pack(pady=5)
    tk.Button(win, text="Croissant $1.75", command=lambda: agregar("Croissant")).pack(pady=5)

    tk.Button(win, text="Finalizar Pedido", command=finalizar).pack(pady=20)

    win.mainloop()

if __name__ == "__main__":
    main()
