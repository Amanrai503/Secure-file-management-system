import sys
from cryptography.fernet import Fernet
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from inset_user_to_database import insert_user_info
from login_logic import get_key, verify
import resource_1





class CreateWindow(QMainWindow):
    def __init__(self):
        super(CreateWindow, self).__init__()
        uic.loadUi("ui_files\\input_user.ui", self)  
        self.setWindowIcon(QIcon("resources\\logo.png"))
        self.setWindowTitle("FortiFile")
        self.resize(1000, 653)
        self.fade_in_animation()
        self.widget_2.setVisible(False)
        self.error_text.setVisible(False)
        self.error_icon.setVisible(False)
        self.error_text_2.setVisible(False)
        self.error_icon_2.setVisible(False)
        self.next_btn.clicked.connect(self.show_ver)
        self.lofin_btn.clicked.connect(self.login_to_account)
        self.verify_btn.clicked.connect(self.verify_and_save)
        self.name.setFocus()
    
    def fade_in_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)  # Duration in milliseconds (1 sec)
        self.animation.setStartValue(0)  # Fully transparent
        self.animation.setEndValue(1)  # Fully visible
        self.animation.start()

    def fade_out_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)  # Duration in milliseconds (1 sec)
        self.animation.setStartValue(1)  # Fully transparent
        self.animation.setEndValue(0)  # Fully visible
        self.animation.finished.connect(self.close)
        self.animation.start()

    
    def shake_window(self):
        """Shakes the window to indicate an error."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setKeyValueAt(0, self.geometry())
        self.animation.setKeyValueAt(0.25, self.geometry().adjusted(-10, 0, -10, 0))
        self.animation.setKeyValueAt(0.50, self.geometry().adjusted(10, 0, 10, 0))
        self.animation.setKeyValueAt(0.75, self.geometry().adjusted(-10, 0, -10, 0))
        self.animation.setKeyValueAt(1, self.geometry())  # Back to normal
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.start()

    def login_to_account(self):
        self.fade_out_animation()
        from user_login import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
    
    def show_ver(self):
            self.key,qr = get_key(self.email.text())
            self.name_val = self.name.text()
            self.email_val = self.email.text()
            self.password_val = self.password.text()
            self.key_va = self.key
            self.enc_key = Fernet.generate_key()
            if self.name_val.strip()=="" or self.email_val.strip()=="" or self.password_val.strip()=="":
                self.shake_window()
                self.error_text_2.setVisible(True)
                self.error_icon_2.setVisible(True)
            else:
                self.error_text_2.setVisible(False)
                self.error_icon_2.setVisible(False)
                self.widget_2.setVisible(True)
                self.widget_3.setVisible(False)
                self.qr_label.setPixmap(qr)

    def verify_and_save(self):
        totp = self.totp.text()

        if totp.strip()=="":
            self.shake_window()
            self.error_text.setText("Access Key can not be empty")
            self.error_text.setVisible(True)
            self.error_icon.setVisible(True)
            return
        if verify(self.key, totp):
            print("Verification successful, proceeding to insert user...")
            try:
                insert_user_info(self.name_val,self.email_val,self.password_val,self.key_va,self.enc_key)
                print("Insert function completed")
                self.fade_out_animation()
                self.close()
                from user_login import LoginWindow
                self.login_win = LoginWindow()
                self.login_win.show()
            except Exception as e:
                print(f"Error during insert: {e}")
        else:
            self.error_text.setText("Invalid access code. Please try again.")
            self.shake_window()
            self.error_text.setVisible(True)
            self.error_icon.setVisible(True)
            self.totp.clear()
            self.totp.setFocus()
            

def main():
    app = QApplication(sys.argv)  
    window = CreateWindow()        
    window.show()              
    #window.resize(1000, 653)     
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()