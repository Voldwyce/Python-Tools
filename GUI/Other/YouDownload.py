import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox
from pytube import YouTube

class YouDownload(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 600, 200)

        self.video_url_label = QLabel("URL del video de YouTube:")
        self.video_url_edit = QLineEdit()
        self.download_button = QPushButton("Descargar")
        self.download_button.clicked.connect(self.download_video)

        self.download_type_label = QLabel("Tipo de descarga:")
        self.download_type_combo = QComboBox()
        self.download_type_combo.addItems(["Video", "Audio (MP3)"])

        layout = QVBoxLayout()
        layout.addWidget(self.video_url_label)
        layout.addWidget(self.video_url_edit)
        layout.addWidget(self.download_type_label)
        layout.addWidget(self.download_type_combo)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_video(self):
        video_url = self.video_url_edit.text().strip()
        download_type = self.download_type_combo.currentText()

        if not video_url:
            QMessageBox.warning(self, "Error", "Por favor ingrese una URL válida.")
            return

        try:
            yt = YouTube(video_url)

            if download_type == "Video":
                stream = yt.streams.get_highest_resolution()
            elif download_type == "Audio (MP3)":
                stream = yt.streams.filter(only_audio=True).first()

            if stream:
                default_filename = stream.default_filename
                save_path = QFileDialog.getSaveFileName(self, "Guardar archivo", default_filename)[0]
                if save_path:
                    stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
                    QMessageBox.information(self, "Descarga completada", "La descarga ha finalizado correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se encontró ningún stream disponible para descargar.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al descargar el video: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouDownload()
    window.show()
    sys.exit(app.exec())
