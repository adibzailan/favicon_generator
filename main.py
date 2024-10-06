import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QMessageBox, QProgressBar, QFrame, QCheckBox, QScrollArea)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QTimer
from PIL import Image

class FaviconGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Favicon Generator')
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
            QCheckBox {
                font-size: 14px;
            }
        """)

        main_layout = QVBoxLayout()

        # Header
        header_label = QLabel('Favicon Generator', self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont('Arial', 20, QFont.Bold))
        main_layout.addWidget(header_label)

        # Upload button
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.setIcon(QIcon('upload_icon.png'))  
        self.upload_button.clicked.connect(self.upload_image)
        main_layout.addWidget(self.upload_button)

        # Checkbox for save location
        self.save_original_checkbox = QCheckBox('Save in original location', self)
        self.save_original_checkbox.setChecked(True)
        main_layout.addWidget(self.save_original_checkbox)

        # Image display
        self.image_frame = QFrame(self)
        self.image_frame.setFrameShape(QFrame.StyledPanel)
        self.image_frame.setStyleSheet("background-color: white;")
        self.image_layout = QVBoxLayout(self.image_frame)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.image_label)
        main_layout.addWidget(self.image_frame)

        # Preview area
        self.preview_scroll = QScrollArea(self)
        self.preview_scroll.setWidgetResizable(True)
        self.preview_widget = QWidget()
        self.preview_layout = QHBoxLayout(self.preview_widget)
        self.preview_scroll.setWidget(self.preview_widget)
        main_layout.addWidget(self.preview_scroll)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel('Ready to generate favicons', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Enable drag and drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.process_image(file_path)
                break

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.process_image(file_name)

    def process_image(self, image_path):
        try:
            self.progress_bar.show()
            self.status_label.setText('Generating favicons...')
            QApplication.processEvents()

            if self.save_original_checkbox.isChecked():
                output_folder = os.path.dirname(image_path)
            else:
                output_folder = os.path.join(os.path.dirname(image_path), 'generated_favicons')
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

            sizes_and_names = [
                ((512, 512), 'Icon-512{}'),
                ((512, 512), 'Icon-maskable-512{}'),
                ((192, 192), 'Icon-192{}'),
                ((192, 192), 'Icon-maskable-192{}')
            ]

            original_format = os.path.splitext(image_path)[1]
            processed_images = []

            with Image.open(image_path) as img:
                for i, (size, name_template) in enumerate(sizes_and_names):
                    img_resized = img.resize(size, Image.LANCZOS)
                    new_name = name_template.format(original_format)
                    output_path = os.path.join(output_folder, new_name)
                    img_resized.save(output_path)
                    processed_images.append(output_path)
                    self.progress_bar.setValue((i + 1) * 25)
                    QApplication.processEvents()

            self.update_preview(processed_images)

            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.status_label.setText('Favicons generated successfully!')
            QMessageBox.information(self, "Success", f"Favicons generated and saved in {output_folder}!")
        except Exception as e:
            self.status_label.setText('Error occurred during favicon generation')
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_bar.hide()
            self.progress_bar.setValue(0)

    def update_preview(self, image_paths):
        # Clear existing previews
        for i in reversed(range(self.preview_layout.count())): 
            self.preview_layout.itemAt(i).widget().setParent(None)

        # Add new previews
        for path in image_paths:
            preview_label = QLabel()
            pixmap = QPixmap(path)
            preview_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            preview_label.setToolTip(os.path.basename(path))
            self.preview_layout.addWidget(preview_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaviconGeneratorApp()
    ex.show()
    sys.exit(app.exec_())