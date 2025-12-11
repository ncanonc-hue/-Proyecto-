import sys
import subprocess
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox,
    QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


CSV_FILENAME = "historial_cafe_unal.csv"


class HubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DATA ASSISTANT - HUB FINAL")
        self.setGeometry(300, 200, 450, 650)
        self.setStyleSheet("background-color: #f3f3f3;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # --- Logo ---
        logo_label = QLabel()
        if os.path.exists("logo.png"):
            pixmap = QPixmap("logo.png").scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("LOGO")
            logo_label.setFont(QFont("Arial", 28))
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # --- Título ---
        title = QLabel("Proyecto Final")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Línea separadora
        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(linea)

        # --- Indicadores Globales ---
        indicadores_title = QLabel("📊 Indicadores Globales")
        indicadores_title.setFont(QFont("Arial", 14, QFont.Bold))
        indicadores_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(indicadores_title)

        self.indicadores_label = QLabel(self.cargar_indicadores())
        self.indicadores_label.setFont(QFont("Arial", 11))
        self.indicadores_label.setAlignment(Qt.AlignCenter)
        self.indicadores_label.setStyleSheet("padding: 8px;")
        main_layout.addWidget(self.indicadores_label)

        # 🔄 --- BOTÓN PARA ACTUALIZAR ---
        actualizar_btn = QPushButton("🔄 Actualizar Indicadores")
        actualizar_btn.setStyleSheet("""
            QPushButton {
                background-color: #dfe6e9;
                border: 1px solid #b2bec3;
                border-radius: 6px;
                padding: 8px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #b2bec3;
            }
        """)
        actualizar_btn.clicked.connect(self.actualizar_indicadores)
        main_layout.addWidget(actualizar_btn)

        # --- Espacio ---
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Botones de módulos ---
        botones_frame = QFrame()
        botones_layout = QVBoxLayout(botones_frame)

        estilo_boton = """
            QPushButton {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """

        btn1 = QPushButton("Abrir Módulo 1")
        btn1.setStyleSheet(estilo_boton)
        btn1.clicked.connect(lambda: self.abrir_modulo("modulo1.py"))
        botones_layout.addWidget(btn1)

        btn2 = QPushButton("Abrir Módulo 2")
        btn2.setStyleSheet(estilo_boton)
        btn2.clicked.connect(lambda: self.abrir_modulo("modulo2.py"))
        botones_layout.addWidget(btn2)

        btn3 = QPushButton("Abrir Módulo 3")
        btn3.setStyleSheet(estilo_boton)
        btn3.clicked.connect(lambda: self.abrir_modulo("modulo3.py"))
        botones_layout.addWidget(btn3)

        # botón salir
        btn_exit = QPushButton("Salir")
        btn_exit.setStyleSheet(estilo_boton)
        btn_exit.clicked.connect(self.close)
        botones_layout.addWidget(btn_exit)

        main_layout.addWidget(botones_frame)

        self.setLayout(main_layout)

    # --- Abrir módulos ---
    def abrir_modulo(self, archivo):
        if os.path.exists(archivo):
            subprocess.Popen(["python", archivo])
        else:
            QMessageBox.warning(self, "Error", f"No se encontró el archivo {archivo}")

    # --- Cargar indicadores desde CSV ---
    def cargar_indicadores(self):
        if not os.path.exists(CSV_FILENAME):
            return "No hay datos aún.\nRealiza pedidos en el Módulo 3."

        try:
            df = pd.read_csv(CSV_FILENAME)

            if df.empty:
                return "No hay información registrada."

            total_clientes = len(df)
            total_ventas = df["total"].sum()

            productos = []
            for pedidos in df["pedido"]:
                productos.extend(str(pedidos).split(";"))

            producto_mas_vendido = (
                pd.Series(productos).value_counts().idxmax()
                if productos else "No disponible"
            )

            promedio = len(productos) / total_clientes if total_clientes > 0 else 0

            return (
                f"Clientes atendidos: {total_clientes}\n"
                f"Total ventas: ${total_ventas:.2f}\n"
                f"Producto más vendido: {producto_mas_vendido}\n"
                f"Promedio ítems por cliente: {promedio:.2f}"
            )

        except Exception as e:
            return f"Error al leer datos:\n{e}"

    # --- 🔄 ACTUALIZAR VISUAL DE INDICADORES ---
    def actualizar_indicadores(self):
        self.indicadores_label.setText(self.cargar_indicadores())


def main():
    app = QApplication(sys.argv)
    window = HubWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
