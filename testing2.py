import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QMainWindow
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class GifPlayer(QMainWindow):
    def __init__(self):
        super(GifPlayer, self).__init__()
        uic.loadUi(r"ui_files\window_animation.ui", self)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowOpacity(1)
        

        self.movie = QMovie(r"resources\search320.gif")  # Replace with your GIF file path
        self.lab.setMovie(self.movie)
        self.movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifPlayer()
    window.show()
    sys.exit(app.exec_())