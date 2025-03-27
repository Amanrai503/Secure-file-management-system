import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QTreeView, QFileSystemModel, QWidget, QSizePolicy, QPushButton, QMessageBox, QInputDialog, QHeaderView
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon, QClipboard
from PyQt5.QtCore import Qt, QDir, QSize,QFileInfo, QDateTime, QPropertyAnimation, QEasingCurve
import resource_1

from testing_animation import GifPlayer
from operations import cut_funtion, delete_funtion, rename_funtion, paste_funtion, copy_funtion, details_funtion, set_details, new_file_funtion

import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files\\main_window.ui", self)
        self.setWindowIcon(QIcon("resources\\logo.png"))
        self.setWindowTitle("FortiFile")
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.fade_in_animation()
        self.toolBar.setIconSize(QSize(36, 36))
        self.details_widget.setVisible(False)

        
        self.treeWidget.clear()
        self.treeWidget.setIconSize(QSize(28, 28))

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
        self.actionScan_file.triggered.connect(self.scan_file)

        self.actionLockAll.triggered.connect(self.lock_f)
        self.actionUnlockFile.triggered.connect(self.unlock_f)
        self.details_on = False

    def fade_in_animation(self):
        """Applies a fade-in effect to the window."""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)  # Duration in milliseconds (1 sec)
        self.animation.setStartValue(0)  # Fully transparent
        self.animation.setEndValue(1)  # Fully visible
        self.animation.start()



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
        if self.details_on:
            set_details(self)


    def activate_buttons(self):
        self.actionCut.setEnabled(True)
        self.actionCopy.setEnabled(True)
        self.actionRename.setEnabled(True)
        self.actionDelete.setEnabled(True)
        self.actionDetails.setEnabled(True)
        self.actionLockAll.setEnabled(True)
        self.actionUnlockFile.setEnabled(True)
        self.actionScan_file.setEnabled(True)

    def deactivate_buttons(self):
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionRename.setEnabled(False)
        self.actionScan_file.setEnabled(False)
        self.actionDetails.setEnabled(False)
        self.actionLockAll.setEnabled(False)
        self.actionUnlockFile.setEnabled(False)

    def populate_tree(self, root_folder):
        root_folder_path_list = [r"D:\python\Secure File Management System\Documents",r"D:\python\Secure File Management System\Downloads",r"D:\python\Secure File Management System\Music",r"D:\python\Secure File Management System\Pictures"]
        root_folder_icon_list = [r"D:\python\Secure File Management System\resources\doc.png",r"D:\python\Secure File Management System\resources\download.png",r"D:\python\Secure File Management System\resources\music.png",r"D:\python\Secure File Management System\resources\picture.png"]
        for folder,icon in zip(root_folder_path_list,root_folder_icon_list):
            item = QTreeWidgetItem([os.path.basename(folder)])
            item_icon =QIcon(icon)
            item.setIcon(0, item_icon)
            item.setData(0, Qt.UserRole, folder)
            self.treeWidget.addTopLevelItem(item)
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
        self.current_selected_file_path = None
        self.deactivate_buttons()
    
    def refresh_tree(self):
        self.treeWidget.clear()     
        self.populate_tree(self.start_directory)

    def new_file(self):
        print("New file")
        new_file_funtion(self)
        pass

    def cut_f(self):
        print("Cut")
        cut_funtion(self)

    def copy_f(self):
        print("Copy")
        copy_funtion(self)
        
    def paste_f(self):
        print("Paste")
        paste_funtion(self)

    def rename_f(self):
        print("Rename")
        rename_funtion(self)

    def delete_f(self):
        print("Delete")
        delete_funtion(self)

    def details_f(self):
        details_funtion(self)
        set_details(self)

    def lock_f(self):
        print("Lock")
        pass

    def unlock_f(self):
        print("Unlock")
        pass

    def scan_file(self):
        self.scan_window = GifPlayer(self)
        self.scan_window.show()
        self.setDisabled(True)
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply dark theme
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())