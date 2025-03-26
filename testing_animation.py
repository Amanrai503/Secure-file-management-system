import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QMovie

class GifPlayer(QWidget):
    def __init__(self):
        super(GifPlayer, self).__init__()
        uic.loadUi(r"ui_files\animation.ui", self)

        self.movie = QMovie(r"resources\icons8-portrait-mode-scanning.gif")  # Replace with your GIF file path
        self.label_2.setMovie(self.movie)
        self.movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifPlayer()
    window.show()
    sys.exit(app.exec_())