from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt, QPoint, pyqtSignal


class FloatingIcon(QWidget):
    icon_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 100, 100)

        self.icon_label = QLabel(self)

        # Load assets from the assets folder
        self.normal_icon = QPixmap("idle_state.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.movie = QMovie("xonitron-disco.gif")
        self.movie.setScaledSize(self.size())  # Adjust to widget size

        self.icon_label.setPixmap(self.normal_icon)
        self.icon_label.setGeometry(0, 0, 100, 100)

        self.old_position = None
        self.is_dragging = False

        self.show()

    def switch_to_gif(self):
        """Switch the icon to GIF animation."""
        self.icon_label.setMovie(self.movie)
        self.movie.start()

    def switch_to_normal(self):
        """Switch the icon back to normal idle state."""
        self.movie.stop()
        self.icon_label.setPixmap(self.normal_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_position = event.globalPos()
            self.is_dragging = True

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = event.globalPos() - self.old_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_position = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
