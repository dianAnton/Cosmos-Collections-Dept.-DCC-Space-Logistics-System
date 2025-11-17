import sys
from PyQt5.QtWidgets import QApplication
from frontend.ventanas.ventana_inicio import Inicio
from frontend.ventanas.ventana_principal import VentanaPrincipal


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear las ventanas
    inicio = Inicio()
    ventana_principal = VentanaPrincipal()

    # Mostrar la ventana inicial
    inicio.show()

    # Conectar senales
    inicio.senal_ir_entrada.connect(ventana_principal.show)

    sys.exit(app.exec())