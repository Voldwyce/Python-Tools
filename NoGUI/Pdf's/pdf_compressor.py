import os
import shutil
import subprocess
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QFileDialog, QComboBox, QMessageBox, QCheckBox)
from PySide6.QtCore import Qt

# Function to compress PDF via Ghostscript command line interface
def compress(input_file_path, output_folder_path, power=0):
    quality = {
        0: "/default",
        1: "/prepress",
        2: "/printer",
        3: "/ebook",
        4: "/screen"
    }

    if not os.path.isfile(input_file_path):
        raise FileNotFoundError(f"Error: ruta o archivo no encontrado: {input_file_path}")

    if power < 0 or power > len(quality) - 1:
        raise ValueError(f"Error: nivel de compresion no valido: {power}")

    if input_file_path.split('.')[-1].lower() != 'pdf':
        raise ValueError(f"Error: input file is not a PDF: {input_file_path}")

    gs = get_ghostscript_path()
    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(os.path.join(output_folder_path, os.path.basename(input_file_path))),
            input_file_path,
        ]
    )

def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64"]
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError("No se encontro la ruta del ghostscript en ({})".format('/'.join(gs_names)))

class PDFCompressorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Compressor")
        self.setGeometry(100, 100, 600, 300)

        layout = QVBoxLayout()

        self.input_path_label = QLabel("Ruta del PDF de entrada:")
        self.input_path_edit = QLineEdit()
        self.browse_input_button = QPushButton("Seleccionar archivo")
        self.browse_input_button.clicked.connect(self.browse_input_file)

        self.output_path_label = QLabel("Ruta de la carpeta de salida:")
        self.output_path_edit = QLineEdit()
        self.browse_output_button = QPushButton("Seleccionar carpeta")
        self.browse_output_button.clicked.connect(self.browse_output_folder)

        self.compression_label = QLabel("Nivel de compresión:")
        self.compression_combo = QComboBox()
        self.compression_combo.addItems(["Default", "Prepress", "Printer (Recomendado)", "Ebook", "Screen"])

        self.backup_checkbox = QCheckBox("Generar backup del archivo original")
        self.open_checkbox = QCheckBox("Abrir carpeta después de comprimir")

        self.compress_button = QPushButton("Comprimir")
        self.compress_button.clicked.connect(self.compress_pdf)

        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.browse_input_button)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_edit)
        layout.addWidget(self.browse_output_button)
        layout.addWidget(self.compression_label)
        layout.addWidget(self.compression_combo)
        layout.addWidget(self.backup_checkbox)
        layout.addWidget(self.open_checkbox)
        layout.addWidget(self.compress_button)

        self.setLayout(layout)

    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.input_path_edit.setText(file_path)

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if folder_path:
            self.output_path_edit.setText(folder_path)

    def compress_pdf(self):
        input_path = self.input_path_edit.text()
        output_folder = self.output_path_edit.text()
        compression_level = self.compression_combo.currentIndex()
        backup = self.backup_checkbox.isChecked()
        open_after = self.open_checkbox.isChecked()

        if not input_path or not output_folder:
            QMessageBox.critical(self, "Error", "Por favor, especifica las rutas del archivo de entrada y la carpeta de salida.")
            return

        try:
            compress(input_path, output_folder, compression_level)
            
            if backup:
                backup_path = os.path.join(output_folder, os.path.basename(input_path).replace(".pdf", "_BACKUP.pdf"))
                shutil.copyfile(input_path, backup_path)

            QMessageBox.information(self, "Éxito", "Compresión completada.")
            
            if open_after:
                os.startfile(output_folder)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFCompressorApp()
    window.show()
    sys.exit(app.exec())
