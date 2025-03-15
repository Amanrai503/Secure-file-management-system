import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Create multiple buttons
        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")

        # Install event filter on both buttons
        self.button1.installEventFilter(self)
        self.button2.installEventFilter(self)

        # Add buttons to layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.setLayout(layout)

    def eventFilter(self, obj, event):
        # Check if the event is a double-click and which button was clicked
        if event.type() == event.MouseButtonDblClick:
            if isinstance(obj, QPushButton):  # Ensure the object is a button
                button_name = obj.text()  # Get the button text
                QMessageBox.information(self, "Double Click", f"{button_name} was double-clicked!")
                return True  # Event is handled

        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
