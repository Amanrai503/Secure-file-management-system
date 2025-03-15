from PyQt5.QtWidgets import QApplication, QTreeView
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel
import qdarkstyle
import sys

class FileManager(QTreeView):
    def __init__(self):
        super().__init__()

        # Create a file system model
        self.model = QFileSystemModel()
        self.model.setRootPath("")  # Start from the root directory

        # Set the model to the tree view
        self.setModel(self.model)

        # Set the root directory (Change to a specific directory if needed)
        self.setRootIndex(self.model.index("D:\\python\\Secure File Management System\\Drive"))  # Change to desired root path

        # Expand folders by default
        self.expandAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = FileManager()
    window.setWindowTitle("File Manager")
    window.show()
    sys.exit(app.exec_())
