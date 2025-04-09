import sys
import qdarkstyle
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class ProfilePopup(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.Popup)  # makes it behave like a popup
        uic.loadUi("ui_files\\acc_popup.ui", self)
        self.toggle_btn.clicked.connect(self.toggle_theme)
        self.logout_btn.clicked.connect(self.logout)


    def toggle_theme(self):
        if self.parent.theme == "light":
            self.parent.theme = "dark"
            self.toggle_btn.setText("Light Mode")
            self.toggle_btn.setChecked(False)
            self.parent.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            
        else:
            self.parent.theme = "light"
            self.toggle_btn.setChecked(True)
            self.parent.setStyleSheet("")
            self.toggle_btn.setText("Dark Mode")
            self.setStyleSheet('''QPushButton {
                                background-color: transparent;
                                border: 1px;
                                height:50px;
                            }

                            QPushButton:hover {
                                background-color: rgba(255, 255, 255, 0.1);
                                border-radius: 5px;
                            }

                            QPushButton:pressed {
                                background-color: rgba(255, 255, 255, 0.2);
                            }
                            ''')
    
    def logout(self):
        self.parent.logout()
