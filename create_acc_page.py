import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
import mysql.connector
from login_logic import get_key, verify
import resource_1

class Verify(QWidget):
    def __init__(self):
        super(Verify, self).__init__()
        uic.loadUi("ui_files\\verify.ui", self)  # Loading the UI file
        self.setWindowTitle("Verify Account")
        


class CreateWindow(QMainWindow):
    def __init__(self):
        super(CreateWindow, self).__init__()
        uic.loadUi("ui_files\create_acc.ui", self)  # Loading the UI file
        self.setWindowTitle("Create Account")
        self.layout = self.horizontalLayout_2  # to add the verify widget we need to get the layout
        self.next_btn.clicked.connect(self.open_qr)

    def open_qr(self):
        self.key,qr = get_key(self.email.text(), self.password.text())
        if self.widget_2:
            self.layout.removeWidget(self.widget_2)
            self.widget_2.deleteLater()
        self.widget_verify = Verify()   #making the verify widget 
        self.widget_verify.verify_btn.clicked.connect(self.verify_and_save)
        self.layout.addWidget(self.widget_verify)
        self.qr_label.setPixmap(qr)
        self.qr_label.setScaledContents(True)  #setting the qr 
        
        # getting the values tand adding to the data base 
        self.email_val = self.email.text()
        self.password_val = self.password.text()
        self.name_val = self.name.text()
        print(self.email_val)
        print(self.password_val)
        print(self.name_val)
        print(self.key)

    def verify_and_save(self):
        totp_secret = self.widget_verify.acces_code.text()
        print(totp_secret)
        if verify(self.key, totp_secret):
            QMessageBox.information(None, "Information", "Account Created Successfully")
            self.close()
        else:
            print("Invalid Access Code")

    def insert_user(name: str, email: str, password: str, key: str):
        try:
            # Establish a database connection
            connection = mysql.connector.connect(
                host="localhost",  # Change as needed
                user="your_username",  # Change as needed
                password="your_password",  # Change as needed
                database="login_info"
            )
            cursor = connection.cursor()

            # SQL query to insert user data
            insert_query = """
            INSERT INTO users (name, email, password, `totp_secret`) VALUES (%s, %s, %s, %s)
            """
            values = (name, email, password, key)
            
            # Execute query and commit changes
            cursor.execute(insert_query, values)
            connection.commit()
            print("User inserted successfully.")
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        finally:
            # Close resources
            if cursor:
                cursor.close()
            if connection:
                connection.close()
def main():
    app = QApplication(sys.argv)  
    window = CreateWindow()        
    window.show()                 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()