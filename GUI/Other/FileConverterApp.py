import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, 
                               QComboBox, QLineEdit, QMessageBox, QCheckBox, QStackedWidget, QProgressBar, 
                               QGridLayout, QGroupBox, QHBoxLayout, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PIL import Image
import moviepy.editor as mp

class ConversionThread(QThread):
    progress = Signal(int)
    finished = Signal(str, str, bool)  

    def __init__(self, conversion_func, *args):
        super().__init__()
        self.conversion_func = conversion_func
        self.args = args

    def run(self):
        try:
            self.conversion_func(*self.args)
            self.progress.emit(100)
            self.finished.emit(self.args[0], self.args[1], True)
        except Exception as e:
            self.finished.emit(self.args[0], self.args[1], False)

class FileConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter & Resizer")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()

        self.file_type_selection_widget = QWidget()
        self.file_type_layout = QVBoxLayout()

        self.file_type_label = QLabel("Seleccione el tipo de archivo a modificar:")
        self.file_type_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        self.image_button = QPushButton("Imagen")
        self.video_button = QPushButton("Video")
        self.audio_button = QPushButton("Audio")

        self.image_button.clicked.connect(self.show_image_options)
        self.video_button.clicked.connect(self.show_video_options)
        self.audio_button.clicked.connect(self.show_audio_options)

        self.file_type_layout.addWidget(self.file_type_label)
        self.file_type_layout.addWidget(self.image_button)
        self.file_type_layout.addWidget(self.video_button)
        self.file_type_layout.addWidget(self.audio_button)
        
        self.file_type_selection_widget.setLayout(self.file_type_layout)
        
        self.file_options_widget = QWidget()
        self.file_options_layout = QVBoxLayout()

        self.back_button = QPushButton("Atrás")
        self.back_button.clicked.connect(self.show_file_type_selection)
        self.back_button.setStyleSheet("font-size: 14px;")

        self.select_file_label = QLabel("Archivo seleccionado:")
        self.selected_file_text = QLineEdit()
        self.selected_file_text.setReadOnly(True)

        self.select_file_button = QPushButton("Seleccionar archivo")
        self.select_file_button.clicked.connect(self.select_file)

        self.format_label = QLabel("Formato de destino:")
        self.format_combo = QComboBox()

        self.actions_groupbox = QGroupBox("Acciones adicionales")
        self.actions_layout = QGridLayout()
        self.resize_checkbox = QCheckBox("Redimensionar imagen")
        self.resize_checkbox.stateChanged.connect(self.toggle_resize_options)
        self.width_label = QLabel("Ancho:")
        self.width_edit = QLineEdit()
        self.height_label = QLabel("Alto:")
        self.height_edit = QLineEdit()

        self.replace_checkbox = QCheckBox("Reemplazar archivo original")
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("height: 20px;")

        self.convert_button = QPushButton("Convertir")
        self.convert_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.convert_button.clicked.connect(self.convert_file)

        self.actions_layout.addWidget(self.resize_checkbox, 0, 0, 1, 2)
        self.actions_layout.addWidget(self.width_label, 1, 0)
        self.actions_layout.addWidget(self.width_edit, 1, 1)
        self.actions_layout.addWidget(self.height_label, 2, 0)
        self.actions_layout.addWidget(self.height_edit, 2, 1)
        self.actions_groupbox.setLayout(self.actions_layout)

        self.file_options_layout.addWidget(self.back_button)
        self.file_options_layout.addWidget(self.select_file_label)
        self.file_options_layout.addWidget(self.selected_file_text)
        self.file_options_layout.addWidget(self.select_file_button)
        self.file_options_layout.addWidget(self.format_label)
        self.file_options_layout.addWidget(self.format_combo)
        self.file_options_layout.addWidget(self.actions_groupbox)
        self.file_options_layout.addWidget(self.replace_checkbox)
        self.file_options_layout.addWidget(self.convert_button)
        self.file_options_layout.addWidget(self.progress_bar)

        self.file_options_widget.setLayout(self.file_options_layout)

        self.stacked_widget.addWidget(self.file_type_selection_widget)
        self.stacked_widget.addWidget(self.file_options_widget)

        self.disable_resize_options()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.reset_fields()

        self.threads = []

    def closeEvent(self, event):
        for thread in self.threads:
            thread.wait() 
        event.accept()

    def show_file_type_selection(self):
        self.reset_fields()
        self.stacked_widget.setCurrentWidget(self.file_type_selection_widget)

    def show_image_options(self):
        self.resize_checkbox.setVisible(True)
        self.resize_checkbox.setEnabled(True)
        self.resize_checkbox.setChecked(False)
        self.actions_groupbox.setVisible(True)
        self.width_label.setVisible(True)
        self.height_label.setVisible(True)
        self.width_edit.setVisible(True)
        self.height_edit.setVisible(True)
        self.disable_resize_options()
        self.populate_formats(["jpg", "png", "gif", "bmp", "tif", "webp", "heic", "svg", "pdf", "ico"])
        self.stacked_widget.setCurrentWidget(self.file_options_widget)

    def show_video_options(self):
        self.resize_checkbox.setVisible(False)
        self.actions_groupbox.setVisible(False)
        self.width_label.setVisible(False)
        self.height_label.setVisible(False)
        self.width_edit.setVisible(False)
        self.height_edit.setVisible(False)
        self.disable_resize_options()
        self.populate_formats(["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm", "h264", "h265"])
        self.stacked_widget.setCurrentWidget(self.file_options_widget)

    def show_audio_options(self):
        self.resize_checkbox.setVisible(False)
        self.actions_groupbox.setVisible(False)
        self.width_label.setVisible(False)
        self.height_label.setVisible(False)
        self.width_edit.setVisible(False)
        self.height_edit.setVisible(False)
        self.disable_resize_options()
        self.populate_formats(["mp3", "wav", "aac", "flac", "ogg", "aiff", "alac", "midi"])
        self.stacked_widget.setCurrentWidget(self.file_options_widget)

    def toggle_resize_options(self, state):
        if Qt.CheckState(state) == Qt.Checked:
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
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Archivos (*.jpg *.png *.gif *.bmp *.tif *.webp *.heic *.svg *.pdf *.ico *.mp4 *.mov *.avi *.wmv *.flv *.mkv *.webm *.h264 *.h265 *.mp3 *.wav *.aac *.flac *.ogg *.aiff *.alac *.midi)")
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            self.selected_file_paths = file_paths
            self.selected_file_text.setText("; ".join(file_paths))

    def convert_file(self):
        if not self.selected_file_paths:
            QMessageBox.warning(self, "Error", "Por favor seleccione un archivo válido.")
            return

        dest_format = self.format_combo.currentText().lower()
        if dest_format == "seleccionar formato":
            QMessageBox.warning(self, "Error", "Por favor seleccione un formato de destino.")
            return

        for file_path in self.selected_file_paths:
            if not os.path.isfile(file_path):
                QMessageBox.warning(self, "Error", f"Archivo no válido: {file_path}")
                continue

            file_type = ""
            if self.resize_checkbox.isVisible() and self.resize_checkbox.isEnabled():
                file_type = "Imagen"
            elif dest_format in ["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm", "h264", "h265"]:
                file_type = "Video"
            elif dest_format in ["mp3", "wav", "aac", "flac", "ogg", "aiff", "alac", "midi"]:
                file_type = "Audio"
            
            if file_type == "Imagen":
                conversion_thread = ConversionThread(self.convert_image, file_path, dest_format)
            elif file_type == "Video":
                conversion_thread = ConversionThread(self.convert_video, file_path, dest_format)
            elif file_type == "Audio":
                conversion_thread = ConversionThread(self.convert_audio, file_path, dest_format)
            else:
                QMessageBox.warning(self, "Error", "Formato no soportado.")
                continue

            conversion_thread.progress.connect(self.update_progress)
            conversion_thread.finished.connect(self.conversion_finished)
            self.threads.append(conversion_thread)
            conversion_thread.start()

    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    @Slot(str, str, bool)
    def conversion_finished(self, file_path, dest_format, success):
        if success:
            QMessageBox.information(self, "Convertido", f"Archivo convertido a {dest_format} exitosamente: {file_path}")
        else:
            QMessageBox.critical(self, "Error", f"Error al convertir archivo: {file_path}")

    def convert_image(self, file_path, dest_format):
        img = Image.open(file_path)
        if self.resize_checkbox.isChecked():
            width = int(self.width_edit.text())
            height = int(self.height_edit.text())
            img = img.resize((width, height), Image.LANCZOS)
        output_path = file_path if self.replace_checkbox.isChecked() else f"{os.path.splitext(file_path)[0]}_converted.{dest_format}"
        img.save(output_path)

    def convert_video(self, file_path, dest_format):
        video = mp.VideoFileClip(file_path)
        output_path = file_path if self.replace_checkbox.isChecked() else f"{os.path.splitext(file_path)[0]}_converted.{dest_format}"
        video.write_videofile(output_path)

    def convert_audio(self, file_path, dest_format):
        audio = mp.AudioFileClip(file_path)
        output_path = file_path if self.replace_checkbox.isChecked() else f"{os.path.splitext(file_path)[0]}_converted.{dest_format}"
        audio.write_audiofile(output_path)

    def reset_fields(self):
        self.selected_file_text.clear()
        self.format_combo.setCurrentIndex(0)
        self.resize_checkbox.setChecked(False)
        self.replace_checkbox.setChecked(False)
        self.progress_bar.setValue(0)
        self.disable_resize_options()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileConverterApp()
    window.show()
    sys.exit(app.exec())
