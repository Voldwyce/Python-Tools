import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit, QMessageBox, QCheckBox, QRadioButton, QButtonGroup
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image
import moviepy.editor as mp

class FileConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter & Resizer")
        self.setGeometry(100, 100, 600, 400)

        self.selected_file_path = ""

        self.file_type_label = QLabel("Seleccione el tipo de archivo a modificar:")
        
        self.image_button = QRadioButton("Imagen")
        self.video_button = QRadioButton("Video")
        self.audio_button = QRadioButton("Audio")

        self.file_type_group = QButtonGroup()
        self.file_type_group.addButton(self.image_button, id=0)
        self.file_type_group.addButton(self.video_button, id=1)
        self.file_type_group.addButton(self.audio_button, id=2)
        self.file_type_group.buttonClicked.connect(self.update_ui)

        self.select_file_label = QLabel("Archivo seleccionado:")
        self.selected_file_text = QLineEdit()
        self.selected_file_text.setReadOnly(True)

        self.select_file_button = QPushButton("Seleccionar archivo")
        self.select_file_button.clicked.connect(self.select_file)

        self.format_label = QLabel("Formato de destino:")
        self.format_combo = QComboBox()

        self.actions_label = QLabel("Acciones adicionales:")
        self.resize_checkbox = QCheckBox("Redimensionar imagen")
        self.resize_checkbox.stateChanged.connect(self.toggle_resize_options)
        self.width_label = QLabel("Ancho:")
        self.width_edit = QLineEdit()
        self.height_label = QLabel("Alto:")
        self.height_edit = QLineEdit()

        self.convert_button = QPushButton("Convertir")
        self.convert_button.clicked.connect(self.convert_file)

        self.disable_resize_options()

        layout = QVBoxLayout()
        layout.addWidget(self.file_type_label)
        layout.addWidget(self.image_button)
        layout.addWidget(self.video_button)
        layout.addWidget(self.audio_button)
        layout.addWidget(self.select_file_label)
        layout.addWidget(self.selected_file_text)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.actions_label)
        layout.addWidget(self.resize_checkbox)
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_edit)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_edit)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

    def update_ui(self, button):
        if button == self.image_button:
            self.enable_resize_options()
            self.populate_formats(["jpg", "png", "gif", "bmp", "tif", "webp", "heic", "svg", "pdf", "ico"])
        elif button == self.video_button:
            self.disable_resize_options()
            self.populate_formats(["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm", "h264", "h265"])
        elif button == self.audio_button:
            self.disable_resize_options()
            self.populate_formats(["mp3", "wav", "aac", "flac", "ogg", "aiff", "alac", "midi"])
        else:
            self.disable_resize_options()
            self.populate_formats([])

    def toggle_resize_options(self, state):
        if state == Qt.Checked:
            self.enable_resize_options()
        else:
            self.disable_resize_options()

    def enable_resize_options(self):
        self.width_label.setEnabled(True)
        self.width_edit.setEnabled(True)
        self.height_label.setEnabled(True)
        self.height_edit.setEnabled(True)

    def disable_resize_options(self):
        self.width_label.setEnabled(False)
        self.width_edit.setEnabled(False)
        self.height_label.setEnabled(False)
        self.height_edit.setEnabled(False)

    def populate_formats(self, formats):
        self.format_combo.clear()
        self.format_combo.addItem("Seleccionar formato")
        for format in formats:
            self.format_combo.addItem(format)

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Archivos (*.jpg *.png *.gif *.bmp *.tif *.webp *.heic *.svg *.pdf *.ico *.mp4 *.mov *.avi *.wmv *.flv *.mkv *.webm *.h264 *.h265 *.mp3 *.wav *.aac *.flac *.ogg *.aiff *.alac *.midi)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.selected_file_path = file_path
            self.selected_file_text.setText(file_path)

    def convert_file(self):
        if not self.selected_file_path or not os.path.isfile(self.selected_file_path):
            QMessageBox.warning(self, "Error", "Por favor seleccione un archivo válido.")
            return

        file_type = ""
        if self.image_button.isChecked():
            file_type = "Imagen"
        elif self.video_button.isChecked():
            file_type = "Video"
        elif self.audio_button.isChecked():
            file_type = "Audio"
        
        dest_format = self.format_combo.currentText().lower()
        
        if file_type == "Imagen":
            self.convert_image(dest_format)
        elif file_type == "Video":
            self.convert_video(dest_format)
        elif file_type == "Audio":
            self.convert_audio(dest_format)

    def convert_image(self, dest_format):
        try:
            img = Image.open(self.selected_file_path)
            if self.resize_checkbox.isChecked():
                width = int(self.width_edit.text())
                height = int(self.height_edit.text())
                img = img.resize((width, height), Image.ANTIALIAS)
            img.save(f"{os.path.splitext(self.selected_file_path)[0]}.{dest_format}")
            QMessageBox.information(self, "Convertido", f"Imagen convertida a {dest_format} exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al convertir imagen: {str(e)}")

    def convert_video(self, dest_format):
        try:
            video = mp.VideoFileClip(self.selected_file_path)
            video.write_videofile(f"{os.path.splitext(self.selected_file_path)[0]}.{dest_format}")
            QMessageBox.information(self, "Convertido", f"Video convertido a {dest_format} exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al convertir video: {str(e)}")

    def convert_audio(self, dest_format):
        try:
            audio = mp.AudioFileClip(self.selected_file_path)
            audio.write_audiofile(f"{os.path.splitext(self.selected_file_path)[0]}.{dest_format}")
            QMessageBox.information(self, "Convertido", f"Audio convertido a {dest_format} exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al convertir audio: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileConverterApp()
    window.show()
    sys.exit(app.exec())
