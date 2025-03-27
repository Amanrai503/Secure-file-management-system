from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scan import scan_file_virustotal

class ScanThread(QThread):
    finished = pyqtSignal(object)  # Signal to send scan result when done

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        result = scan_file_virustotal(self.file_path)  # Run the scan
        self.finished.emit(result)  # Emit the result when done

class GifPlayer(QWidget):
    def __init__(self, main_window):
        super(GifPlayer, self).__init__()
        self.mainwindow = main_window
        uic.loadUi(r"ui_files\animation.ui", self)
        self.setWindowTitle("Scanning the file")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.setWindowOpacity(1)

        # Load and start GIF animation
        self.movie = QMovie(r"resources\search.gif")
        self.lab.setMovie(self.movie)
        self.movie.start()

        self.pushButton_2.clicked.connect(self.abort_scan)

        # Start the scan in a separate thread
        self.scan_thread = ScanThread(self.mainwindow.current_selected_file_path)
        self.scan_thread.finished.connect(self.scan_complete)
        self.scan_thread.start()

    def scan_complete(self, result):
        """Called when scanning is complete"""
        if result:
            print("Scan completed successfully.")
        else:
            print("Scan failed.")

    
        self.pushButton_2.setText("Close")
        self.pushButton_2.setStyleSheet(
            """
            QPushButton {
                background-color: #2ECC71; /* Green for success */
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """
            )
        self.movie.stop()
        self.movie = QMovie("resources/safe-ezgif.com-resize.gif",loopCount=1)
        self.lab.setMovie(self.movie)
        self.movie.setCacheMode(QMovie.CacheAll)  # Cache the frames for smooth play
        self.movie.setSpeed(100)  # Set speed to normal (100%)
        self.movie.finished.connect(self.movie.stop)
        self.movie.start()
        self.movie.finished.connect(self.close)
        
        #self.close()  # Close GIF window
        #self.mainwindow.setDisabled(False)  # Re-enable main window

    def abort_scan(self):
        """User aborts scanning"""
        self.scan_thread.terminate()  # Unsafe, but quick fix (better to use a flag)
        self.close()
        self.mainwindow.setDisabled(False)
