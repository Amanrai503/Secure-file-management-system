import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class UserForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Registration")
        self.setGeometry(200, 200, 300, 200)

        # Create layout
        layout = QVBoxLayout()

        # Name Input
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Email Input
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        # Password Input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Insert Button
        self.insert_button = QPushButton("Insert")
        self.insert_button.clicked.connect(self.insert_user)
        layout.addWidget(self.insert_button)

        self.setLayout(layout)

    def insert_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Change this if you have a different MySQL username
                password="1234",  # Change this to your MySQL password
                database="test"
            )
            cursor = connection.cursor()

            # Insert query
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            connection.commit()

            QMessageBox.information(self, "Success", "User inserted successfully!")
            
            # Clear input fields
            self.name_input.clear()
            self.email_input.clear()
            self.password_input.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserForm()
    window.show()
    sys.exit(app.exec_())
