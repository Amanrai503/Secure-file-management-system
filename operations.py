from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFileIconProvider
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QPixmap
import os 
import shutil



def paste_funtion(self):
        print("Paste")
        if not hasattr(self, 'copied_file_path') or not self.copied_file_path:
            QMessageBox.warning(self, "No File Copied", "Please copy or cut a file before pasting.")
            return

        destination_folder = self.current_directory
        if destination_folder:
            file_name = os.path.basename(self.copied_file_path)  
            destination_path = os.path.join(destination_folder, file_name)

            # Check if file already exists
            if os.path.exists(destination_path):
                reply = QMessageBox.question(
                    self, "File Exists",
                    f"The file '{file_name}' already exists. Do you want to replace it?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return  # Cancel the operation

            try:
                if self.is_cut_operation:
                    shutil.move(self.copied_file_path, destination_path)  
                    QMessageBox.information(self, "Success", f"File moved to: {destination_path}")
                    self.copied_file_path = None  
                else:
                    shutil.copy(self.copied_file_path, destination_path)  
                    QMessageBox.information(self, "Success", f"File pasted to: {destination_path}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to paste file:\n{str(e)}")

            if self.is_cut_operation:
                self.actionPaste.setEnabled(False)

def cut_funtion(self):
        print("Cut")
        if not hasattr(self, 'current_selected_file_path') or not self.current_selected_file_path:
            QMessageBox.warning(self, "No File Selected", "Please select a file to cut.")
            return
        self.copied_file_path = self.current_selected_file_path  # Store file path for later use
        self.is_cut_operation = True  # This is a cut operation
        self.actionPaste.setEnabled(True)
        QMessageBox.information(self, "Cut", "File cut (not yet pasted).")
        pass

def delete_funtion(self):
    """Deletes the selected file or, if no file is selected, deletes the selected folder."""
    
    if self.current_selected_file_path:  
        target_path = self.current_selected_file_path  # Delete the selected file
    elif self.current_directory:  
        target_path = self.current_directory  # Delete the selected folder
    else:
        QMessageBox.warning(self, "No Selection", "Please select a file or folder to delete.")
        return  # Exit if nothing is selected

    # Confirm deletion
    reply = QMessageBox.question(
        self, "Confirm Deletion",
        f"Are you sure you want to delete '{os.path.basename(target_path)}'?",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )

    if reply == QMessageBox.No:
        return  # User canceled

    try:
        if os.path.isdir(target_path):  
            shutil.rmtree(target_path)  # Delete folder and its contents
        else:  
            os.remove(target_path)  # Delete file

        QMessageBox.information(self, "Deleted", f"'{os.path.basename(target_path)}' has been deleted.")
        
        # Clear the deleted selection
        if target_path == self.current_selected_file_path:
            self.current_selected_file_path = None
        elif target_path == self.current_directory:
            self.current_directory = None
            self.refresh_tree()




    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to delete:\n{str(e)}")
            
def rename_funtion(self):
        print("Rename")
        if not hasattr(self, 'current_selected_file_path') or not self.current_selected_file_path:
            QMessageBox.warning(self, "No File Selected", "Please select a file or folder to rename.")
            return

        file_path = self.current_selected_file_path
        file_dir = os.path.dirname(file_path)
        old_name = os.path.basename(file_path)

        new_name, ok = QInputDialog.getText(self, "Rename", f"Enter a new name for '{old_name}':")


        if not ok or not new_name.strip():
            return

        new_name = new_name.strip()
        new_path = os.path.join(file_dir, new_name)


        if os.path.exists(new_path):
            QMessageBox.warning(self, "File Exists", "A file with this name already exists. Please choose a different name.")
            return

        try:
            os.rename(file_path, new_path)  
            QMessageBox.information(self, "Renamed", f"'{old_name}' has been renamed to '{new_name}'.")
            
        
            self.current_selected_file_path = new_path

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename file:\n{str(e)}")

def copy_funtion(self):
        print("Copy")
        if not hasattr(self, 'current_selected_file_path') or not self.current_selected_file_path:
            QMessageBox.warning(self, "No File Selected", "Please select a file to copy.")
            return
        self.copied_file_path = self.current_selected_file_path  # Store file path for later use
        self.is_cut_operation = False  # This is a copy operation
        self.actionPaste.setEnabled(True)
        QMessageBox.information(self, "Copied", "File copied to clipboard (not yet pasted).")
        pass

def details_funtion(self):
        if self.details_on:
            self.details_widget.setVisible(False)
            self.details_on = False
        else:
            self.details_on = True
            print("Details")
            self.details_widget.setVisible(True)
            file_info = QFileInfo(self.current_selected_file_path)
            if not file_info.exists():
                print("File does not exist!")
                return

def set_details(self):
            file_info = QFileInfo(self.current_selected_file_path)
            file_size = file_info.size()  # Size in bytes
            file_location = file_info.absoluteFilePath()  # Full path
            created_time = file_info.birthTime().toString("yyyy-MM-dd HH:mm:ss")  # Creation time
            modified_time = file_info.lastModified().toString("yyyy-MM-dd HH:mm:ss")  # Modification time
            accessed_time = file_info.lastRead().toString("yyyy-MM-dd HH:mm:ss")  # Last access time
            permissions = file_info.permissions()  # Returns permissions as PyQt enum

            icon_provider = QFileIconProvider()
            icon = icon_provider.icon(file_info)
            pixmap = icon.pixmap(56,56)
            self.label.setPixmap(pixmap)

            self.name.setText(file_info.fileName())
            self.size_d.setText(str(file_size))
            self.location.setText(file_location)
            self.created.setText(created_time)
            self.modified.setText(modified_time)
            self.access.setText(accessed_time)
            self.permission.setText(str(int(permissions)))

def new_file_funtion(self):
    target_directory = self.current_directory
    file_name, ok = QInputDialog.getText(self, "New File", "Enter file name:")
    
    if not ok or not file_name.strip():
        QMessageBox.warning(self, "Warning", "File name cannot be empty!")
        return None

   
    os.makedirs(target_directory, exist_ok=True)
    if '.' not in file_name:
        file_name += ".txt"

    file_path = os.path.join(target_directory, file_name)

    name, ext = os.path.splitext(file_name)
    counter = 1
    while os.path.exists(file_path):
        new_filename = f"{name}_{counter}{ext}"
        file_path = os.path.join(target_directory, new_filename)
        counter += 1
    with open(file_path, "w") as file:
        file.write("")

    QMessageBox.information(self, "Success", f"File created: {file_path}")