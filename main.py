import sys
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTreeView, QListView, QPushButton, QLabel, QMessageBox, 
                             QFileSystemModel, QInputDialog, QLineEdit)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QModelIndex

class SecureFileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set up main window
        self.setWindowTitle('Secure File Manager')
        self.setGeometry(100, 100, 1000, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Create sidebar
        sidebar_layout = self.create_sidebar()
        
        # Create file view area
        file_view_layout = self.create_file_view()
        
        # Create action buttons
        action_buttons = self.create_action_buttons()
        
        # Combine layouts
        main_layout.addLayout(sidebar_layout, 1)
        main_layout.addLayout(file_view_layout, 4)
        main_layout.addLayout(action_buttons, 1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def create_sidebar(self):
        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        
        # Create a list of standard directories
        standard_dirs = [
            ('Documents', QIcon.fromTheme('folder-documents')),
            ('Downloads', QIcon.fromTheme('folder-downloads')),
            ('Music', QIcon.fromTheme('folder-music')),
            ('Pictures', QIcon.fromTheme('folder-pictures')),
            ('Drive', QIcon.fromTheme('folder-remote'))
        ]
        
        # Add standard directories
        for dir_name, icon in standard_dirs:
            full_path = os.path.join(QDir.homePath(), dir_name)
            
            # Create button with icon
            btn = QPushButton(dir_name)
            btn.setIcon(icon)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #d0d0d0;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            btn.clicked.connect(lambda checked, path=full_path: self.open_folder(path))
            sidebar_layout.addWidget(btn)
        
        # Add custom directories dynamically
        custom_dirs = [
            'Assistant',  # from the screenshot
            # You can add more custom directories here
        ]
        
        for dir_name in custom_dirs:
            full_path = os.path.join(QDir.homePath(), dir_name)
            
            # Create button for custom directory
            btn = QPushButton(dir_name)
            btn.setIcon(QIcon.fromTheme('folder'))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e6f2ff;
                    border: 1px solid #b3d9ff;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #cce6ff;
                }
            """)
            btn.clicked.connect(lambda checked, path=full_path: self.open_folder(path))
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch(1)
        return sidebar_layout
        
        def create_file_view(self):
            # File view layout
            file_view_layout = QVBoxLayout()
            
            # File system model
            self.file_model = QFileSystemModel()
            self.file_model.setRootPath(QDir.homePath())
            
            # List view for files
            self.file_list_view = QListView()
            self.file_list_view.setModel(self.file_model)
            
            file_view_layout.addWidget(self.file_list_view)
            return file_view_layout
    
    def create_action_buttons(self):
        # Action buttons layout
        action_layout = QVBoxLayout()
        
        # Define buttons
        buttons = [
            ('New Folder', self.create_new_folder),
            ('New File', self.create_new_file),
            ('Copy', self.copy_file),
            ('Paste', self.paste_file),
            ('Lock File', self.lock_file),
            ('Delete', self.delete_file)
        ]
        
        for btn_text, btn_method in buttons:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            btn.clicked.connect(btn_method)
            action_layout.addWidget(btn)
        
        action_layout.addStretch(1)
        return action_layout
    
    def open_folder(self, folder_path):
        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)
        
        # Set file list view to selected folder
        index = self.file_model.index(folder_path)
        self.file_list_view.setRootIndex(index)
    
    def create_new_folder(self):
        # Get current directory
        current_path = self.file_model.filePath(
            self.file_list_view.rootIndex()
        )
        
        # Prompt for folder name
        folder_name, ok = QInputDialog.getText(
            self, 'New Folder', 'Enter folder name:'
        )
        
        if ok and folder_name:
            try:
                new_folder_path = os.path.join(current_path, folder_name)
                os.makedirs(new_folder_path)
                QMessageBox.information(
                    self, 'Success', f'Folder {folder_name} created successfully!'
                )
            except Exception as e:
                QMessageBox.warning(
                    self, 'Error', f'Could not create folder: {str(e)}'
                )
    
    def create_new_file(self):
        # Get current directory
        current_path = self.file_model.filePath(
            self.file_list_view.rootIndex()
        )
        
        # Prompt for file name
        file_name, ok = QInputDialog.getText(
            self, 'New File', 'Enter file name:'
        )
        
        if ok and file_name:
            try:
                new_file_path = os.path.join(current_path, file_name)
                with open(new_file_path, 'w') as f:
                    pass  # Create empty file
                QMessageBox.information(
                    self, 'Success', f'File {file_name} created successfully!'
                )
            except Exception as e:
                QMessageBox.warning(
                    self, 'Error', f'Could not create file: {str(e)}'
                )
    
    def copy_file(self):
        # Get selected file
        indexes = self.file_list_view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, 'Error', 'No file selected to copy')
            return
        
        self.copied_file_path = self.file_model.filePath(indexes[0])
    
    def paste_file(self):
        # Get current directory
        current_path = self.file_model.filePath(
            self.file_list_view.rootIndex()
        )
        
        if not hasattr(self, 'copied_file_path'):
            QMessageBox.warning(self, 'Error', 'No file copied')
            return
        
        try:
            # Get filename from copied path
            filename = os.path.basename(self.copied_file_path)
            destination = os.path.join(current_path, filename)
            
            # Copy file
            shutil.copy2(self.copied_file_path, destination)
            QMessageBox.information(
                self, 'Success', f'File {filename} pasted successfully!'
            )
        except Exception as e:
            QMessageBox.warning(
                self, 'Error', f'Could not paste file: {str(e)}'
            )
    
    def lock_file(self):
        # Get selected file
        indexes = self.file_list_view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, 'Error', 'No file selected to lock')
            return
        
        file_path = self.file_model.filePath(indexes[0])
        
        # Prompt for password
        password, ok = QInputDialog.getText(
            self, 'Lock File', 'Enter password:', 
            QLineEdit.Password
        )
        
        if ok and password:
            try:
                # Rename file with .locked extension
                locked_path = file_path + '.locked'
                os.rename(file_path, locked_path)
                QMessageBox.information(
                    self, 'Success', f'File locked successfully!'
                )
            except Exception as e:
                QMessageBox.warning(
                    self, 'Error', f'Could not lock file: {str(e)}'
                )
    
    def delete_file(self):
        # Get selected file
        indexes = self.file_list_view.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, 'Error', 'No file selected to delete')
            return
        
        file_path = self.file_model.filePath(indexes[0])
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, 'Confirm Delete', 
            'Are you sure you want to delete this file?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    shutil.rmtree(file_path)
                QMessageBox.information(
                    self, 'Success', 'File/Folder deleted successfully!'
                )
            except Exception as e:
                QMessageBox.warning(
                    self, 'Error', f'Could not delete file: {str(e)}'
                )

def main():
    app = QApplication(sys.argv)
    file_manager = SecureFileManager()
    file_manager.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()