import sys
import mysql.connector as sqlt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from inset_user import insert_user_info
from login_logic import get_key, verify
import resource_1
from main_window import MainWindow




class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi("ui_files\\testing_incertion.ui", self)  
        self.setWindowIcon(QIcon("resources\\logo.png"))
        self.setWindowTitle("Ctreate Account")
        self.widget_2.setVisible(False)
        self.next_btn.clicked.connect(self.show_ver)
        self.verify_btn.clicked.connect(self.verify_and_save)
        self.name.setFocus()
    
    def show_ver(self):
            self.key,qr = get_key(self.email.text(), self.password.text())
            self.name_val = self.name.text()
            self.email_val = self.email.text()
            self.password_val = self.password.text()
            self.key_va = self.key
            self.qr_label.setPixmap(qr)
            self.qr_label.setScaledContents(True)

    def verify_and_save(self):
        totp = self.totp.text()
        if verify(self.key, totp):
            print("Verification successful, proceeding to insert user...")
            try:
                insert_user_info(self.name_val, self.email_val, self.password_val, self.key_va)
                print("Insert function completed")
            except Exception as e:
                print(f"Error during insert: {e}")
        print("done//////////////////////")
def main():
    app = QApplication(sys.argv)  
    window = LoginWindow()        
    window.show()              
    window.resize(1000, 653)     
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()