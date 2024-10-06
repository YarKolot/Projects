import sys
from screeninfo import get_monitors
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QPixmap, QPainter, QPen, QCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
                             QSlider, QColorDialog, QWidget)

class ScreenshotTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(0, 0, 200, 50)
        self.setWindowTitle('NedoSnippingTool')
        self.screenshot_button = QPushButton('Make screenshot', self)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        layout = QVBoxLayout()
        layout.addWidget(self.screenshot_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def take_screenshot(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        self.canvas_window = CanvasWindow()
        self.canvas_window.set_canvas(screenshot)
        self.canvas_window.showMaximized()
        self.settings_window = SettingsWindow(self.canvas_window)
        self.settings_window.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def closeEvent(self, event):
        if hasattr(self, 'canvas_window'):
            self.canvas_window.close()
        if hasattr(self, 'settings_window'):
            self.settings_window.close()
        event.accept()

class CanvasWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Canvas')
        self.setWindowFlags(Qt.Window)
        self.drawing = False
        self.brush_size = 5
        self.brush_color = Qt.black
        self.eraser_mode = False
        self.original_canvas = None
        self.setCursor(QCursor(Qt.CrossCursor))
        self.canvas_label = QLabel(self)
        self.canvas_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.canvas_label.setPixmap(self.canvas)

    def set_canvas(self, pixmap):
        self.original_canvas = pixmap
        self.canvas = pixmap.copy()
        self.canvas_label.setPixmap(self.canvas)

    def mousePressEvent(self, event):
        offset = QPoint(6, 6)
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos() - offset
        elif event.button() == Qt.RightButton:
            self.draw_point(event.pos() - offset)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.canvas)
            offset = QPoint(6, 6)
            if self.eraser_mode and self.original_canvas:
                eraser_rect = QRect(event.pos() - offset - QPoint(self.brush_size // 2, self.brush_size // 2),
                                    QSize(self.brush_size, self.brush_size))
                original_part = self.original_canvas.copy(eraser_rect)
                painter.drawPixmap(eraser_rect, original_part)
            else:
                pen = QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setPen(pen)
                painter.drawLine(self.last_point - QPoint(self.brush_size // 2, self.brush_size // 2),
                                 event.pos() - offset - QPoint(self.brush_size // 2, self.brush_size // 2))
            self.last_point = event.pos() - offset
            self.canvas_label.setPixmap(self.canvas)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def draw_point(self, pos):
        painter = QPainter(self.canvas)
        pen = QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        center_correction = QPoint(self.brush_size // 2, self.brush_size // 2)
        painter.drawPoint(pos - center_correction)
        self.canvas_label.setPixmap(self.canvas)

    def clear_canvas(self):
        if self.original_canvas:
            self.canvas = self.original_canvas.copy()
        else:
            self.canvas.fill(Qt.white)
        self.canvas_label.setPixmap(self.canvas)

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode

    def change_color(self, color):
        self.brush_color = color

    def change_brush_size(self, size):
        self.brush_size = size


class SettingsWindow(QMainWindow):
    def __init__(self, canvas_window):
        super().__init__()
        self.canvas_window = canvas_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(0, h-200, 200, 150)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.brush_button = QPushButton("Eraser", self)
        self.brush_button.clicked.connect(self.toggle_eraser)
        self.color_button = QPushButton("Color", self)
        self.color_button.clicked.connect(self.change_color)
        self.brush_slider = QSlider(Qt.Horizontal, self)
        self.brush_slider.setRange(1, 100)
        self.brush_slider.setValue(self.canvas_window.brush_size)
        self.brush_slider.valueChanged.connect(self.change_brush_size)
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.canvas_window.clear_canvas)
        layout = QVBoxLayout()
        layout.addWidget(self.brush_button)
        layout.addWidget(self.color_button)
        layout.addWidget(self.brush_slider)
        layout.addWidget(self.clear_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self.drag_start_position
            self.move(self.pos() + delta)
            self.drag_start_position = event.globalPos()

    def toggle_eraser(self):
        self.canvas_window.toggle_eraser()
        if self.canvas_window.eraser_mode:
            self.brush_button.setText("Brush")
        else:
            self.brush_button.setText("Eraser")

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas_window.change_color(color)

    def change_brush_size(self):
        size = self.brush_slider.value()
        self.canvas_window.change_brush_size(size)

if __name__ == '__main__':
    for m in get_monitors():
        w = m.width
        h = m.height
    app = QApplication(sys.argv)
    screenshot_tool = ScreenshotTool()
    screenshot_tool.show()
    sys.exit(app.exec_())