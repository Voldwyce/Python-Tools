import os
import shutil
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox, QFileDialog, QInputDialog)
import pikepdf

class PDFEncrypterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Encrypter/Decrypter")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.option_label = QLabel("Seleccione una opción:")
        self.encrypt_button = QPushButton("Encriptar")
        self.decrypt_button = QPushButton("Desencriptar")

        self.encrypt_button.clicked.connect(self.encrypt_pdf)
        self.decrypt_button.clicked.connect(self.decrypt_pdf)

        layout.addWidget(self.option_label)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def encrypt_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo PDF", "", "PDF Files (*.pdf)")
        if not path:
            return
        
        owner_password, ok = QInputDialog.getText(self, "Contraseña de Propietario", "Ingrese la contraseña de propietario:")
        if not ok:
            return

        user_password, ok = QInputDialog.getText(self, "Contraseña de Usuario", "Ingrese la contraseña de usuario:")
        if not ok:
            return

        output_file_name = os.path.splitext(path)[0] + "_encrypted.pdf"

        try:
            pdf = pikepdf.open(path)
            pdf.save(output_file_name, encryption=pikepdf.Encryption(owner=owner_password, user=user_password, R=4))
            pdf.close()
            QMessageBox.information(self, "Éxito", "Documento encriptado con éxito.")

            delete_original = QMessageBox.question(self, "Borrar Original", "¿Desea borrar el documento original?",
                                                   QMessageBox.Yes | QMessageBox.No)
            if delete_original == QMessageBox.Yes:
                os.remove(path)
                QMessageBox.information(self, "Éxito", "Documento original borrado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al encriptar el documento: {str(e)}")

    def decrypt_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo PDF", "", "PDF Files (*.pdf)")
        if not path:
            return
        
        password, ok = QInputDialog.getText(self, "Contraseña de Propietario", "Ingrese la contraseña de propietario:")
        if not ok:
            return

        output_file_name = os.path.splitext(path)[0] + "_decrypted.pdf"

        try:
            pdf = pikepdf.open(path, password=password)
            pdf.save(output_file_name)
            pdf.close()
            QMessageBox.information(self, "Éxito", "Documento desencriptado con éxito.")

            delete_original = QMessageBox.question(self, "Borrar Original", "¿Desea borrar el documento original?",
                                                   QMessageBox.Yes | QMessageBox.No)
            if delete_original == QMessageBox.Yes:
                os.remove(path)
                QMessageBox.information(self, "Éxito", "Documento original borrado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al desencriptar el documento: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFEncrypterApp()
    window.show()
    sys.exit(app.exec())
