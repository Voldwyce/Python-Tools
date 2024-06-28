import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QInputDialog, QMessageBox
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Vault Tools")
        self.setGeometry(300, 300, 400, 300)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.label = QLabel("Bienvenido a Python Vault Tools", self)
        self.layout.addWidget(self.label)
        self.label_options = QLabel("Por favor, seleccione una de las siguientes categorias:", self)
        self.layout.addWidget(self.label_options)

        self.pdf_button = QPushButton("Pdf's", self)
        self.pdf_button.clicked.connect(self.pdf_options)
        self.layout.addWidget(self.pdf_button)

        self.other_button = QPushButton("Otros", self)
        self.other_button.clicked.connect(self.other_options)
        self.layout.addWidget(self.other_button)

        self.exit_button = QPushButton("Salir", self)
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

    def pdf_options(self):
        options = ["Comprimir Pdf", "Comprimir carpeta de Pdf's", "Encriptar/Desencriptar Pdf"]
        option, ok = QInputDialog.getItem(self, "Categoría Pdf's", "Seleccione una opción:", options, 0, False)
        
        if ok and option:
            if option == "Comprimir Pdf":
                os.system("python GUI/Pdf's/pdf_compressor.py")
            elif option == "Comprimir carpeta de Pdf's":
                os.system("python GUI/Pdf's/pdf_folder_compressor.py")
            elif option == "Encriptar/Desencriptar Pdf":
                os.system("python GUI/Pdf's/pdf_enc_dec.py")

    def other_options(self):
        options = ["QOTD", "Water Reminder", "Youtube Downloader", "File Converter & Resizer"]
        option, ok = QInputDialog.getItem(self, "Categoría Otros", "Seleccione una opción:", options, 0, False)
        
        if ok and option:
            if option == "QOTD":
                os.system("python GUI/Other/qotd.py")
            elif option == "Water Reminder":
                tiempo, ok = QInputDialog.getInt(self, "Water Reminder", "Cada cuanto quieres recibir el recordatorio? (en minutos):")
                if ok:
                    tiempo = str(tiempo * 60)
                    os.system(f"python NoGUI/Other/water_reminder.pyw -t {tiempo}")
                    QMessageBox.information(self, "Recordatorio", "El recordatorio de agua ha sido configurado.")
            elif option == "Youtube Downloader":
                os.system("python GUI/Other/youDownload.py")
            elif option == "File Converter & Resizer":
                os.system("python GUI/Other/FileConverterApp.py")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()