import sys
from PyQt5 import uic
import global_var
import pymysql
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from create_account import CreateWindow
from login_logic import verify
import resource_1
from main_window import MainWindow




class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi("ui_files\\login_page.ui", self)  
        self.setWindowIcon(QIcon("resources\\logo.png"))
        self.setWindowTitle("FortiFile")
        self.resize(1000, 653)
        self.email_input.setFocus()



        self.create_acc_btn.clicked.connect(self.create_acc)
        self.sign_in_btn.clicked.connect(self.sign_in)
        self.forgot_pass_btn.clicked.connect(self.forgot_pass)

        self.error_icon.setVisible(False)
        self.error_text.setVisible(False)


        self.setWindowOpacity(0)
        self.fade_in_animation()

    def fade_in_animation(self):
        """Applies a fade-in effect to the window."""
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
        
    
    def create_acc(self):
        self.fade_out_animation()
        self.create_window = CreateWindow()
        self.create_window.show()
        



    def forgot_pass(self):
        pass


    def sign_in(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        totp = self.acces_code.text().strip()
        flag = False

        if not email or not password or not totp:
            self.shake_window()
            self.error_text.setText("All fields are required")
            self.error_text.move(218, 510)  
            self.error_icon.move(190,507)
            self.error_icon.setVisible(True)
            self.error_text.setVisible(True)
            return

        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",  
                password="Jaishreeram@1000",  
                database="login_info"
            )

            cursor = connection.cursor()

            # Query to check if email exists
            cursor.execute("SELECT U_id, Name, Email, password2, totp_secret, encryption_key FROM users WHERE Email = %s", (email,))
            result = cursor.fetchone()  

            if result:
                U_id , name, db_email, db_password, db_totp_secret, encryption_key = result
                global_var.current_User_ID = U_id
                global_var.current_key = encryption_key
                global_var.current_user = name
                access = verify(db_totp_secret, totp)

                if password == db_password and access:  
                    flag =  True
                else:
                    flag =  False
            else:
                flag = False

            cursor.close()
            connection.close()
            if flag == True:
                self.main_window = MainWindow()  
                self.main_window.show()
                self.close()
            else:
                self.shake_window()
                self.error_text.setText("Incorrect authentication credentials")
                self.error_text.move(170, 510)  
                self.error_icon.move(142,507)
                self.error_icon.setVisible(True)
                self.error_text.setVisible(True)
                self.password_input.clear()
                self.acces_code.clear()
                self.acces_code.setFocus()

                #QMessageBox.warning(self, "Error", "Invalid Email or Password")
                
                
        except :
            QMessageBox.critical(self, "Database Error")

def main():
    app = QApplication(sys.argv)  
    window = LoginWindow()        
    window.show()                 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()