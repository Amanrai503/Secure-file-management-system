import sys
import os
import mysql.connector as sqlt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from create_acc_page import CreateWindow
import resource_1


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui_files\main_window.ui", self)  # Loading the UI file
        self.setWindowTitle("FortFile")
        self.toolBar.setStyleSheet("QToolBar { spacing: 20px; height: 50px; border: none; border-bottom: 1px solid black; }")

        root_folder = "D:/python/Secure File Management System/Drive"
        self.populate_tree(root_folder)
    

    def populate_tree(self, root_folder):
        self.treeWidget.clear()  # Clear any existing items
        root_item = QTreeWidgetItem(self.treeWidget, [os.path.basename(root_folder)])
        root_item.setIcon(0, QIcon("resources\icons8-folder-96.png"))
        self.treeWidget.addTopLevelItem(root_item)
        self.add_folders(root_item, root_folder)  # Recursively add folders

    def add_folders(self, parent_item, folder_path):
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):  # Only process folders
                    folder_item = QTreeWidgetItem(parent_item, [item])
                    folder_item.setIcon(0, QIcon("resources\icons8-folder-96.png"))
                    self.add_folders(folder_item, item_path)  
        except PermissionError:
            pass  

def main():
    app = QApplication(sys.argv)  
    window = MainWindow()        
    window.show()                 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()