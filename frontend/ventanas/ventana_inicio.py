from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton, QDesktopWidget
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


# Definir la ventana de inicio
class Inicio(QWidget):

    # Senal para abrir la ventana principal
    senal_ir_entrada = pyqtSignal()


    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Departamento de las Colecciones del Cosmos")
        self.setFixedSize(840, 530)

        self.setup_ui()
        self.center()


    # Centrar la ventana siempre
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def setup_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(50, 50, 50, 50)
        layout_principal.setSpacing(1) 

        # Heading 
        fuente_titulo_1 = QFont("Times New Roman", 50, QFont.Bold)
        fuente_titulo_1.setStretch(QFont.Condensed)
        titulo_label_1 = QLabel("<span style='color: #d1a252;'>D</span>"
        "<span style='color: #ede9e8;'>EPARTAMENTO DE LAS</span>", self)
        titulo_label_1.setFont(fuente_titulo_1)
        titulo_label_1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        titulo_label_1.setStyleSheet("color: #ede9e8;") 
        layout_principal.addWidget(titulo_label_1)

        fuente_titulo_2 = QFont("Times New Roman", 75, QFont.Bold)
        fuente_titulo_2.setStretch(QFont.Condensed)
        titulo_label_2 = QLabel("<span style='color: #d1a252;'>C</span>"
        "<span style='color: #ede9e8;'>OLECCIONES DEL</span>", self)
        titulo_label_2.setFont(fuente_titulo_2)
        titulo_label_2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        titulo_label_2.setStyleSheet("color: #ede9e8;") 
        layout_principal.addWidget(titulo_label_2)

        fuente_titulo_3 = QFont("Times New Roman", 95, QFont.Bold)
        fuente_titulo_3.setStretch(QFont.Condensed)
        titulo_label_3 = QLabel("<span style='color: #d1a252;'>C</span>"
        "<span style='color: #ede9e8;'>OSMOS</span>", self)
        titulo_label_3.setFont(fuente_titulo_3)
        titulo_label_3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        titulo_label_3.setStyleSheet("color: #ede9e8; margin: 0; padding: 0;") 
        layout_principal.addWidget(titulo_label_3)
        
        # Subheading
        bienvenida_label = QLabel("BIENVENIDO", self)
        font = QFont("Arial", 30, QFont.Bold) 
        font.setStretch(QFont.Condensed)
        bienvenida_label.setFont(font)
        bienvenida_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        bienvenida_label.setStyleSheet("color: #ede9e8; margin:0; padding: 0;") 
        layout_principal.addWidget(bienvenida_label)

        # Boton ingresar a la ventana principal
        self.boton_ingresar = QPushButton("Ingresar a la Ventana Principal", self)
        fuente_boton = QFont("Times New Roman", 42, QFont.Bold)
        fuente_boton.setStretch(QFont.Condensed)
        self.boton_ingresar.setFont(fuente_boton)
        self.boton_ingresar.setCursor(Qt.PointingHandCursor)
        self.boton_ingresar.setStyleSheet("""
                                            QPushButton {
                                                background-color: #050505;
                                                color: #ede9e8;
                                                padding: 0;
                                                font-size: 35px;
                                                margin-left: 400px;
                                                                                        
                                            }
                                            QPushButton:hover {
                                                font-size: 28px;
                                                color: #9c9c9c;
                                            }
                                        """)
        layout_principal.addWidget(self.boton_ingresar)
        
        # Manejo al presionar el boton
        self.boton_ingresar.clicked.connect(self.boton_ingresar_ventana_principal_clicked)
        
        self.setLayout(layout_principal)
        self.setStyleSheet("background-color: #050505;")


    def boton_ingresar_ventana_principal_clicked(self):
        print("Botón de ingreso presionado. Navegando a la Ventana Principal...")

        # Ocultar ventana actual
        self.hide()

        # Emitir senal
        self.senal_ir_entrada.emit()
