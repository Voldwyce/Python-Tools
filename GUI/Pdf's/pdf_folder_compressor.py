import os
import shutil
import subprocess
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox, QFileDialog, QComboBox, QCheckBox)

CALIDAD = {
    0: "/default",
    1: "/prepress",
    2: "/printer",
    3: "/ebook",
    4: "/screen"
}


class PDFCompressorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Compresor de PDF")
        self.setGeometry(100, 100, 600, 300)

        self.pathIn_label = QLabel("Carpeta de entrada:")
        self.pathIn_edit = QLineEdit()
        self.pathIn_button = QPushButton("Seleccionar Carpeta")

        self.pathOut_label = QLabel("Carpeta de salida:")
        self.pathOut_edit = QLineEdit()
        self.pathOut_button = QPushButton("Seleccionar Carpeta")

        self.pathBackup_label = QLabel("Carpeta de respaldo:")
        self.pathBackup_edit = QLineEdit()
        self.pathBackup_button = QPushButton("Seleccionar Carpeta")
        self.pathBackup_label.setVisible(False)
        self.pathBackup_edit.setVisible(False)
        self.pathBackup_button.setVisible(False)

        self.power_label = QLabel("Nivel de compresión:")
        self.power_combo = QComboBox()
        self.power_combo.addItems(["Default", "Prepress", "Printer", "Ebook", "Screen"])

        self.backup_check = QCheckBox("Crear respaldo de archivos originales")
        self.backup_check.stateChanged.connect(self.toggle_backup_options)

        self.compress_button = QPushButton("Comprimir")
        self.compress_button.clicked.connect(self.compress_folder)

        layout = QVBoxLayout()
        layout.addWidget(self.pathIn_label)
        layout.addWidget(self.pathIn_edit)
        layout.addWidget(self.pathIn_button)

        layout.addWidget(self.pathOut_label)
        layout.addWidget(self.pathOut_edit)
        layout.addWidget(self.pathOut_button)

        backup_layout = QHBoxLayout()
        backup_layout.addWidget(self.backup_check)
        backup_layout.addStretch(1)
        layout.addLayout(backup_layout)

        backup_options_layout = QVBoxLayout()
        backup_options_layout.addWidget(self.pathBackup_label)
        backup_options_layout.addWidget(self.pathBackup_edit)
        backup_options_layout.addWidget(self.pathBackup_button)
        backup_options_layout.addStretch(1)
        layout.addLayout(backup_options_layout)

        layout.addWidget(self.power_label)
        layout.addWidget(self.power_combo)

        layout.addWidget(self.compress_button)

        self.setLayout(layout)

    def toggle_backup_options(self):
        if self.backup_check.isChecked():
            self.pathBackup_label.setVisible(True)
            self.pathBackup_edit.setVisible(True)
            self.pathBackup_button.setVisible(True)
        else:
            self.pathBackup_label.setVisible(False)
            self.pathBackup_edit.setVisible(False)
            self.pathBackup_button.setVisible(False)

    def select_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Entrada", "")
        if folder_path:
            self.pathIn_edit.setText(folder_path)

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Salida", "")
        if folder_path:
            self.pathOut_edit.setText(folder_path)

    def select_backup_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Respaldo", "")
        if folder_path:
            self.pathBackup_edit.setText(folder_path)

    def compress_folder(self):
        pathIn = self.pathIn_edit.text().strip()
        pathOut = self.pathOut_edit.text().strip()

        if not (pathIn and pathOut):
            QMessageBox.warning(self, "Campos Vacíos", "Por favor complete las carpetas de entrada y salida.")
            return

        power = self.power_combo.currentIndex()

        create_backup = self.backup_check.isChecked()
        pathBackup = self.pathBackup_edit.text().strip() if create_backup else ""

        try:
            comprimir_carpeta(pathIn, pathOut, pathBackup, nivel_compresion=power, crear_respaldo=create_backup)
            QMessageBox.information(self, "Compresión Completada", "La compresión de PDF ha finalizado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al comprimir la carpeta: {str(e)}")


def comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion):
    try:
        gs = obtener_ruta_ghostscript()
        subprocess.call([
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={CALIDAD[nivel_compresion]}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-q",
            f"-sOutputFile={archivo_salida}",
            archivo_entrada,
        ])
    except Exception as e:
        raise RuntimeError(f"Error al comprimir {archivo_entrada}: {str(e)}")


def obtener_ruta_ghostscript():
    nombres_gs = ["gswin64c"]
    for nombre in nombres_gs:
        if shutil.which(nombre):
            return shutil.which(nombre)
    raise FileNotFoundError(
        f"No se encontró el ejecutable de GhostScript en la ruta ({'/'.join(nombres_gs)})"
    )


def mover_pdfs(input_folder, output_folder, successfull_folder):
    ts = os.path.getmtime(input_folder)
    for file_name in os.listdir(input_folder):
        archivo_entrada = os.path.join(input_folder, file_name)
        archivo_salida = os.path.join(output_folder, file_name)

        if os.path.isfile(archivo_entrada):
            os.utime(archivo_entrada, (ts, ts))
            ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
            shutil.copy(archivo_entrada, ruta_archivo_realizado)
            shutil.move(archivo_entrada, archivo_salida)


def comprimir_carpeta(input_folder, output_folder, successfull_folder, nivel_compresion=0, crear_respaldo=False):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if crear_respaldo and not os.path.exists(successfull_folder):
        os.makedirs(successfull_folder)

    archivos_comprimidos = 0
    tam_carpeta = 0
    tam_carpeta_final = 0

    for file_name in os.listdir(input_folder):
        archivo_entrada = os.path.join(input_folder, file_name)
        archivo_salida = os.path.join(output_folder, file_name)

        if os.path.isfile(archivo_entrada):
            if archivo_entrada.lower().endswith('.pdf'):
                tam_inicial = os.path.getsize(archivo_entrada)
                try:
                    comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion)
                    tam_final = os.path.getsize(archivo_salida)
                    ratio = 1 - (tam_final / tam_inicial)

                    if tam_final < tam_inicial:
                        archivos_comprimidos += 1
                        if crear_respaldo:
                            ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                            shutil.move(archivo_entrada, ruta_archivo_realizado)
                        tam_carpeta += tam_inicial
                        tam_carpeta_final += tam_final
                    else:
                        comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion + 1)
                        tam_final_nuevo = os.path.getsize(archivo_salida)
                        ratio_nuevo = 1 - (tam_final_nuevo / tam_inicial)

                        if tam_final_nuevo < tam_inicial:
                            archivos_comprimidos += 1
                            if crear_respaldo:
                                ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                                shutil.move(archivo_entrada, ruta_archivo_realizado)
                            tam_carpeta += tam_inicial
                            tam_carpeta_final += tam_final_nuevo

                except Exception as e:
                    print(f"Error al comprimir {archivo_entrada}: {str(e)}")

    ratio_carpeta = 0
    if tam_carpeta + tam_carpeta_final > 0:
        ratio_carpeta = 1 - (tam_carpeta_final / tam_carpeta)

    print(" **************************************************************")
    print(f" Total de archivos comprimidos: {archivos_comprimidos}")
    print(f" Tamaño final de la compresion: {tam_carpeta / 1000000:.5f} -> {tam_carpeta_final / 1000000:.5f}")
    print(f" Ratio final de compresión: {ratio_carpeta:.0%}")
    print(" **************************************************************")

    if crear_respaldo:
        mover_pdfs(input_folder, output_folder, successfull_folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFCompressorApp()
    window.show()
    sys.exit(app.exec())
