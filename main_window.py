import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QTreeView, QFileSystemModel, QWidget, QSizePolicy, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir
import resource_1

import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\main_window.ui", self)
        self.setWindowIcon(QIcon("resources\\logo.png"))

        
        self.treeWidget.clear()
        self.start_directory = "D:/python/Secure File Management System/Drive"
        self.current_directory = self.start_directory
        if os.path.exists(self.start_directory):  

            self.populate_tree(self.start_directory)
        else:
            print(f"Directory '{self.start_directory}' does not exist.")
        self.treeWidget.itemClicked.connect(self.get_folder_path)
        self.get_file()


    def get_file(self):
        model = QFileSystemModel()
        model.setRootPath(self.current_directory)
        model.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(self.current_directory))
        
        
        pass


    def populate_tree(self, root_folder):
        folder_icon = QIcon("resources/icons8-folder-96.png")
        root_item = QTreeWidgetItem(self.treeWidget, [os.path.basename(root_folder)])
        root_item.setIcon(0, folder_icon)
        root_item.setData(0, Qt.UserRole, root_folder)  # Store full path
        self.treeWidget.addTopLevelItem(root_item)
        self.add_folders(root_item, root_folder, folder_icon)

    def add_folders(self, parent_item, folder_path, folder_icon):
        """Recursively add subfolders with icons"""
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):  
                    folder_item = QTreeWidgetItem(parent_item, [item])
                    folder_item.setIcon(0, folder_icon)  
                    folder_item.setData(0, Qt.UserRole, item_path)  # Store path
                    parent_item.addChild(folder_item)
                    self.add_folders(folder_item, item_path, folder_icon)  
        except PermissionError:
            pass  



    def get_folder_path(self, item):
        """Print the full folder path when clicked"""
        folder_path = item.data(0, Qt.UserRole)  # Retrieve stored path
        self.current_directory = folder_path
        self.get_file()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
