import sys
import os
import shutil
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QTreeView, QFileSystemModel, QWidget, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.QtCore import Qt, QDir
import resource_1

import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\main_window.ui", self)
        self.setWindowIcon(QIcon("resources\\logo.png"))
        self.setWindowTitle("FortiFile")

        
        self.treeWidget.clear()


        #variables holding the path of the file and current selectted file
        self.start_directory = "D:/python/Secure File Management System/Drive"
        self.current_directory = self.start_directory
        self.current_selected_file_path = ""



        if os.path.exists(self.start_directory):  

            self.populate_tree(self.start_directory)
        else:
            print(f"Directory '{self.start_directory}' does not exist.")
        self.treeWidget.itemClicked.connect(self.get_folder_path)
        self.get_file()

        self.actionNew.triggered.connect(self.new_file)
        self.actionCut.triggered.connect(self.cut_f)
        self.actionCopy.triggered.connect(self.copy_f)
        self.actionPaste.triggered.connect(self.paste_f)
        self.actionRename.triggered.connect(self.rename_f)
        self.actionDelete.triggered.connect(self.delete_f)
        self.actionDetails.triggered.connect(self.details_f)

        self.actionLock.triggered.connect(self.lock_f)
        self.actionUnlock.triggered.connect(self.unlock_f)



    def get_file(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(self.current_directory)
        self.model.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(self.current_directory))
        self.treeView.clicked.connect(self.display_file_path)
    def display_file_path(self, index):
        self.activate_buttons()
        self.current_selected_file_path = self.model.filePath(index)  # Get file path from index


    def activate_buttons(self):
        self.actionCut.setEnabled(True)
        self.actionCopy.setEnabled(True)
        self.actionRename.setEnabled(True)
        self.actionDelete.setEnabled(True)
        self.actionDetails.setEnabled(True)
        self.actionLock.setEnabled(True)
        self.actionUnlock.setEnabled(True)


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
        #print("current folder  = ", self.current_directory)
        self.get_file()






    def new_file(self):
        print("New file")
        pass

    def cut_f(self):
        print("Cut")
        pass

    def copy_f(self):
        print("Copy")
        if not hasattr(self, 'current_selected_file_path') or not self.current_selected_file_path:
            QMessageBox.warning(self, "No File Selected", "Please select a file to copy.")
            return
        self.copied_file_path = self.current_selected_file_path  # Store file path for later use
        self.actionPaste.setEnabled(True)
        QMessageBox.information(self, "Copied", "File copied to clipboard (not yet pasted).")
        pass

    def paste_f(self):
        print("Paste")
        if not hasattr(self, 'copied_file_path') or not self.copied_file_path:
            QMessageBox.warning(self, "No File Copied", "Please copy a file before pasting.")
            return
        destination_folder = self.current_directory
        if destination_folder:  # If user selected a folder
            file_name = os.path.basename(self.copied_file_path)  # Extract filename
            destination_path = os.path.join(destination_folder, file_name)  # Create full path
            try:
                shutil.copy(self.copied_file_path, destination_path)  # Perform copy
                QMessageBox.information(self, "Success", f"File pasted to: {destination_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to paste file:\n{str(e)}")

    def rename_f(self):
        print("Rename")
        pass

    def delete_f(self):
        print("Delete")
        pass

    def details_f(self):
        print("Details")
        pass

    def lock_f(self):
        print("Lock")
        pass

    def unlock_f(self):
        print("Unlock")
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
