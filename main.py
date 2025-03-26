import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QMovie

class GifPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GIF Player")
        self.setGeometry(100, 100, 50, 50)

        # Create a QLabel to display the GIF
        self.label = QLabel(self)
        self.label.setScaledContents(True)  # Scale the GIF to fit the label

        # Load the GIF
        self.movie = QMovie("resources\icons8-loading.gif")  # Replace with your GIF file path
        self.label.setMovie(self.movie)

        # Start the GIF animation
        self.movie.start()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifPlayer()
    window.show()
    sys.exit(app.exec_())
