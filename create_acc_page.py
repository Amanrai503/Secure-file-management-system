import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from login_logic import get_key, verify
import resource_1

class Verify(QWidget):
    def __init__(self):
        super(Verify, self).__init__()
        uic.loadUi("verify.ui", self)  # Loading the UI file
        self.setWindowTitle("Verify Account")
        


class CreateWindow(QMainWindow):
    def __init__(self):
        super(CreateWindow, self).__init__()
        uic.loadUi("create_acc.ui", self)  # Loading the UI file
        self.setWindowTitle("Create Account")
        self.layout = self.horizontalLayout_2
        self.next_btn.clicked.connect(self.open_qr)

    def open_qr(self):
        self.key,qr = get_key(self.name.text(), self.password.text())
        if self.widget_2:
            self.layout.removeWidget(self.widget_2)
            self.widget_2.deleteLater()
        self.widget_verify = Verify()   #making the verify widget 
        self.widget_verify.verify_btn.clicked.connect(self.verify_and_save)
        self.layout.addWidget(self.widget_verify)
        self.qr_label.setPixmap(qr)
        self.qr_label.setScaledContents(True)  #setting the qr 
        
        # getting the values tand adding to the data base 

    def verify_and_save(self):
        totp_secret = self.widget_verify.acces_code.text()
        print(totp_secret)
        if verify(self.key, totp_secret):
            QMessageBox.information(None, "Information", "Account Created Successfully")
            self.close()
        else:
            print("Invalid Access Code")
def main():
    app = QApplication(sys.argv)  
    window = CreateWindow()        
    window.show()                 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()