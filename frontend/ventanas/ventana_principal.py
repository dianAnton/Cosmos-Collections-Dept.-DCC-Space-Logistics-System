from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QDesktopWidget,
    QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt

from backend import logica_ventana_principal


# Definit la ventana principal
class VentanaPrincipal(QWidget):
    

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Departamento de las Colecciones del Cosmos")
        self.setFixedSize(860, 530) 
        
        # Almacena el path del archivo seleccionado
        self.archivo_path = None 

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
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Contenido Principal
        content_widget = QWidget()
        content_widget.setObjectName("Container")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(80, 10, 80, 15)
        content_layout.setSpacing(10)
        content_widget.setStyleSheet("background-color: #050505; color: #ede9e8;")

        # Barra superior
        top_bar_layout = QHBoxLayout()
        
        # Botón para QFileDialog
        self.upload_button = QPushButton("Subir Archivo")
        self.upload_button.setObjectName("UploadButton")
        self.upload_button.setCursor(Qt.PointingHandCursor)
        self.upload_button.clicked.connect(self.abrir_archivo)
        top_bar_layout.addWidget(self.upload_button)
        self.upload_button.setStyleSheet("""
                                       #UploadButton {
                                        background-color: #9c9c9c; 
                                        color: #ede9e8; 
                                        border: 1px solid #3a3a3c; 
                                        padding: 8px 12px;
                                        border-radius: 6px;
                                        font-size: 13px;
                                        font-weight: bold;
                                       }
                                       
                                       QPushButton#UploadButton:hover {
                                        background-color: #3a3a3c;
                                       }
                                       """)
        

        # Label para mostrar el archivo cargado
        self.path_label = QLabel("Ningún archivo seleccionado.")
        self.path_label.setObjectName("PathLabel")
        top_bar_layout.addWidget(self.path_label, 1)
        self.path_label.setStyleSheet("""
                                       QLabel#PathLabel {
                                        color: #9c9c9c;
                                        padding-left: 10px;
                                        font-size: 12px;
                                       }
                                       """)

        # Botón de Mapa 
        self.mapa_button = QPushButton("Entrar al Mapa")
        self.mapa_button.setObjectName("MapaButton")
        self.mapa_button.setCursor(Qt.PointingHandCursor)
        self.mapa_button.clicked.connect(self.abrir_mapa)
        top_bar_layout.addWidget(self.mapa_button)
        self.mapa_button.setStyleSheet("""
                                       #MapaButton {
                                        background-color: #d1a252; 
                                        color: #000000; 
                                        border: 1px solid #3a3a3c; 
                                        padding: 8px 12px;
                                        border-radius: 6px;
                                        font-size: 13px;
                                        font-weight: bold;
                                       }
                                       
                                       QPushButton#MapaButton:hover {
                                        background-color: #f0b95d;
                                       }
                                       """)
        
        # Botón Ejecutar Consulta (Requerido)
        self.ejecutar_button = QPushButton("Ejecutar Consulta")
        self.ejecutar_button.setObjectName("EjecutarButton")
        self.ejecutar_button.setCursor(Qt.PointingHandCursor)
        self.ejecutar_button.clicked.connect(self.ejecutar_consulta)
        top_bar_layout.addWidget(self.ejecutar_button)
        self.ejecutar_button.setStyleSheet("""
                                       #EjecutarButton {
                                        background-color: #ede9e8; 
                                        color: #000000; 
                                        border: 1px solid #3a3a3c; 
                                        padding: 8px 12px;
                                        border-radius: 6px;
                                        font-size: 13px;
                                        font-weight: bold;
                                       }
                                       
                                       QPushButton#EjecutarButton:hover {
                                        background-color: #cccccc;
                                       }
                                       """)
        
        # Anadir la barra superior al container principal
        content_layout.addLayout(top_bar_layout)

        # Input de texto para consulta
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Entidad, filtro=valor, otro_filtro=valor...")
        self.query_input.setObjectName("QueryInput")
        content_layout.addWidget(self.query_input)
        self.query_input.setStyleSheet("""
                                       QLineEdit#QueryInput {
                                        background-color: #101010; 
                                        color: #ede9e8; 
                                        border: 1px solid #3a3a3c; 
                                        padding: 12px;
                                        border-radius: 8px;
                                        font-size: 15px;
                                       }
                                       
                                       QLineEdit#QueryInput:focus {
                                        border: 1px solid #d1a252;
                                       }
                                       """)

        # Area de texto para resultados 
        self.results_area = QTextEdit()
        self.results_area.setPlaceholderText("Los resultados de la consulta aparecerán aquí...")
        self.results_area.setReadOnly(True)
        self.results_area.setObjectName("ResultsArea")
        content_layout.addWidget(self.results_area, 1)
        self.results_area.setStyleSheet("""
                                       QTextEdit#ResultsArea {
                                        background-color: #101010; 
                                        color: #ede9e8; 
                                        border: 1px solid #3a3a3c; 
                                        padding: 12px;
                                        border-radius: 8px;
                                        font-size: 15px;
                                       }
                                       
                                       QTextEdit#ResultsArea:focus {
                                        border: 1px solid #d1a252;
                                       }
                                        
                                       /* Scrollbar para el área de resultados (QTextEdit) */
                                       QScrollBar:vertical {
                                        border: none;
                                        background: #101010;
                                        width: 10px;
                                        margin: 0px 0px 0px 0px;
                                       }
                                       
                                       QScrollBar::handle:vertical {
                                        background: #3a3a3c;
                                        min-height: 20px;
                                        border-radius: 5px;
                                       }
                                       
                                       QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                        height: 0px;
                                       }
                                       """)

        layout_principal.addWidget(content_widget, 7)
        self.setLayout(layout_principal)


    # logica ventana principal
    def abrir_archivo(self):
        logica_ventana_principal.abrir_archivo_import(self)


    def ejecutar_consulta(self):
        logica_ventana_principal.ejecutar_consulta_import(self)

    def abrir_mapa(self):
        logica_ventana_principal.abrir_mapa_import(self)