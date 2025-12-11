import tkinter as tk
from tkinter import messagebox
import csv
from collections import Counter

pedido = []
total = 0.0
FILENAME = "modulo2_historial.csv"

menu = {
    "Café Americano": 2.50,
    "Latte": 3.00,
    "Croissant": 1.75,
    "Té Verde": 2.00
}

def guardar_csv(nombre, pedido, total):
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, ";".join(pedido), total])

def agregar(prod):
    global total
    pedido.append(prod)
    total += menu[prod]
    messagebox.showinfo("Añadido", f"Agregado {prod}.\nTotal: ${total:.2f}")

def mostrar_diagrama(canvas):
    canvas.delete("all")
    conteo = Counter(pedido)

    x = 50
    for producto, cantidad in conteo.items():
        canvas.create_rectangle(x, 200 - cantidad*20, x+50, 200, fill="brown")
        canvas.create_text(x+25, 210, text=producto, font=("Arial", 8))
        x += 80

def finalizar(canvas):
    global pedido, total
    if not pedido:
        messagebox.showerror("Error", "No has agregado productos.")
        return

    nombre = "Cliente"
    guardar_csv(nombre, pedido, total)
    mostrar_diagrama(canvas)

    messagebox.showinfo("Guardado", f"Pedido guardado.\nTotal: ${total:.2f}")
    pedido = []
    total = 0.0

def main():
    win = tk.Tk()
    win.title("Módulo 2 - Cafetería (versión extendida)")
    win.geometry("450x450")

    tk.Label(win, text="Módulo 2", font=("Arial", 20)).pack()

    canvas = tk.Canvas(win, width=400, height=250, bg="white")
    canvas.pack(pady=10)

    for p in menu:
        tk.Button(win, text=p, command=lambda x=p: agregar(x)).pack()

    tk.Button(win, text="Finalizar y generar gráfico", command=lambda: finalizar(canvas)).pack(pady=10)

    win.mainloop()

if __name__ == "__main__":
    main()