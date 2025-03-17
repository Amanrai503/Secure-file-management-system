import sys
import mysql.connector as sqlt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from create_account import LoginWindow
from login_logic import verify
import resource_1
from main_window import MainWindow




class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi("ui_files\\login_page.ui", self)  
        self.setWindowIcon(QIcon("resources\\logo.png"))
        self.setWindowTitle("Sign in Page")


        self.create_acc_btn.clicked.connect(self.create_acc)
        self.sign_in_btn.clicked.connect(self.sign_in)
        self.forgot_pass_btn.clicked.connect(self.forgot_pass)

        
    
    def create_acc(self):
        self.create_window = LoginWindow()
        self.create_window.show()
        self.close()



    def forgot_pass(self):
        pass


    def sign_in(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        totp = self.acces_code.text().strip()
        flag = False

        if not email or not password and not totp:
            QMessageBox.warning(self, "Error", "Email and Password cannot be empty!")
            return

        try:
            connection = sqlt.connect(
                host="localhost",
                user="root",  
                password="1234",  
                database="login_info"
            )

            cursor = connection.cursor()

            # Query to check if email exists
            cursor.execute("SELECT Email, password2, totp_secret FROM users WHERE Email = %s", (email,))
            result = cursor.fetchone()  

            if result:
                db_email, db_password, db_totp_secret = result  
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
                self.main_window = MainWindow()  # Store in `self` to persist
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid Email or Password")
        except sqlt.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

def main():
    app = QApplication(sys.argv)  
    window = LoginWindow()        
    window.show()                 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()