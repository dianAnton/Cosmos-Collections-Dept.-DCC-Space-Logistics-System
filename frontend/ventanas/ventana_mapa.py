from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                             QDesktopWidget, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPixmap
from backend import consultas
from backend.consultas import cargar_planetas
from utilidades import radio_planeta
import parametros
import os

# Rua donde estan los sprites
# os.path.dirname(__file__) ruta desde donde se ejecuta el archivo actual 
ruta_sprites = os.path.join(os.path.dirname(__file__), '..', 'sprites')


# Container donde se dibujan los planetas
class MapaCanvas(QWidget):
    
    
    def __init__(self, planetas, width, height, factor_radio):
        super().__init__()
        
        self.planetas = list(planetas)
        self.setFixedSize(width, height)
        self.factor_radio = factor_radio
        
        # Cargar sprites por tipo de planeta
        self.sprites = {}
        for tipo in ["criogenico", "gas", "liquido", "plasma", "rocoso"]:
            path = os.path.join(ruta_sprites, f"{tipo}.png")
            if os.path.exists(path):

                # Guardamos la imgen como pixeles, segun su tipo
                self.sprites[tipo] = QPixmap(path)


    # Dibujar los planetas en el container (canvas) establecido
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Calculos para trabajar con coordenadas
        # Determinar límites de coordenadas
        if (parametros.x1 is not None and 
            parametros.y1 is not None and 
            parametros.x2 is not None and 
            parametros.y2 is not None):
            x_min, x_max = parametros.x1, parametros.x2
            y_min, y_max = parametros.y1, parametros.y2

        else:
            xs = []
            ys = []
            for p in self.planetas:
                xs.append(p.coordenada_x)
                ys.append(p.coordenada_y)

            if xs:
                x_min, x_max = min(xs), max(xs)
            
            else:
                # Si la lista de planetas esta vacia
                x_min, x_max = 0, 1

            if ys:
                y_min, y_max = min(ys), max(ys)
            
            else:
                y_min, y_max = 0, 1
        
        
        # Aseguramos que haya un rango minimo 
        if x_min == x_max: 
            x_min -= 1
            x_max += 1
        
        if y_min == y_max: 
            y_min -= 1
            y_max += 1
        
        # Rango de coordenadas
        x_range = x_max - x_min
        y_range = y_max - y_min

        # Fondo oscuro
        painter.fillRect(self.rect(), QColor("#050505"))

        # Dibujar cada planeta
        for p in self.planetas:
            vx = (p.coordenada_x - x_min) / x_range * w

            # Invierte el eje y para la representacion visual
            vy = h - (p.coordenada_y - y_min) / y_range * h

            # Calcular radio visual según tamaño del planeta
            radio_real = radio_planeta(p.id_planeta, p.tamano) 

            # calcular un radia decente
            r = max(3.0, radio_real * self.factor_radio)

            # Dibujar sprite según tipo o círculo si no existe
            tipo = p.tipo.lower()
            
            if tipo in self.sprites:
                pix = self.sprites[tipo].scaled(int(2 * r), int(2 * r),
                                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
                painter.drawPixmap(int(vx - pix.width() / 2), int(vy - pix.height() / 2), pix)
            
            # Los planetas de tipo Solido los representamos con rocoso
            else:
                
                # QPixmap(os.path.join(ruta_sprites, f"solido.png")) incorporar planetas solidos
                # self.sprites["rocoso"] reemplazar planetas solidos por rocosos
                pix = QPixmap(os.path.join(ruta_sprites, f"solido.png")).scaled(int(2 * r), int(2 * r),
                                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                painter.drawPixmap(int(vx - pix.width() / 2), int(vy - pix.height() / 2), pix)


# Ventana completa
class VentanaMapa(QWidget):
    senal_cerrar = pyqtSignal()

    def __init__(self, archivo_planetas_path: str):
        super().__init__()
        self.setWindowTitle("Mapa de Planetas")
        
        self.setFixedSize(1230, 670)
        self.archivo_path = archivo_planetas_path
        self.setup_ui()
        self.center()


    # Centrar la ventana siempre
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        layout.setContentsMargins(15, 15, 15, 15)
        self.setStyleSheet("background-color: #101010; color: #ede9e8;")

        try:

            # Cargar planetas y filtrar
            gen_planetas = cargar_planetas(self.archivo_path)
            planetas_gen = consultas.encontrar_planetas_cercanos(
                gen_planetas,
                parametros.x1, parametros.y1,
                parametros.x2, parametros.y2,
                parametros.cantidad
            )
            planetas = list(planetas_gen)
            
            if not planetas:
                QMessageBox.information(self, "Mapa Vacío", 
                    "No se encontraron planetas en las coordenadas especificadas en parametros.py")

        except (AttributeError, TypeError, ValueError) as error:
            QMessageBox.critical(self, "Error", f"No se pudo cargar planetas para el mapa: {error}")
            planetas = []

        # Crear canvas del mapa
        canvas = MapaCanvas(planetas, 1200, 600, parametros.factor_radio)
        
        # Centrar el canvas en el layout
        canvas_layout = QHBoxLayout()
        canvas_layout.addStretch()
        canvas_layout.addWidget(canvas)
        canvas_layout.addStretch()
        layout.addLayout(canvas_layout)


        # Botón inferior
        botones = QHBoxLayout()
        boton_volver = QPushButton("Cerrar Mapa")
        boton_volver.clicked.connect(self.cerrar_ventana)
        
        # --- MEJORA ESTÉTICA: Estilo de botón ---
        boton_volver.setCursor(Qt.PointingHandCursor)
        boton_volver.setStyleSheet("""
            QPushButton {
                background-color: #9c9c9c; 
                color: #ede9e8; 
                border: 1px solid #3a3a3c; 
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a3a3c;
            }
        """)

        botones.addStretch()
        botones.addWidget(boton_volver)
        botones.addStretch()
        layout.addLayout(botones)
        layout.addStretch()


    def cerrar_ventana(self):
        self.close()
        self.senal_cerrar.emit()