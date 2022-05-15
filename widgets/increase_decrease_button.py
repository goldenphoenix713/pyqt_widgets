"""
A double push button that increases and decreases a value.

@author: Eddie Ruiz

"""
from typing import Optional

from PyQt5 import QtWidgets, QtCore, QtGui


class _SingleButton(QtWidgets.QAbstractButton):

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None,
                 left: bool = True):
        super(_SingleButton, self).__init__(parent)

        self._left_button = left

        self._button_clicked_top = {
            True: self.palette().midlight().color(),
            False: self.palette().light().color(),
        }

        self._button_clicked_bottom = {
            True: self.palette().midlight().color(),
            False: self.palette().button().color(),
        }

        self.setMinimumSize(25, 25)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super(_SingleButton, self).mousePressEvent(event)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing, True)

        width = self.size().width()
        height = self.size().height()

        path = QtGui.QPainterPath()
        path.moveTo(height / 2, 0)
        path.lineTo(width, 0)
        path.lineTo(width, height)
        path.lineTo(height / 2, height)
        path.arcTo(0, 0, height, height, -90, -180)

        if not self._left_button:
            mirror = QtGui.QTransform(-1, 0, 0, 0, 1, 0, 0, 0, 1)
            p.setTransform(mirror)
            p.translate(-width, 0)

        if self.isEnabled():
            gradient = QtGui.QLinearGradient(0, 0, 0, height)
            gradient.setColorAt(0, self._button_clicked_top[self.isDown()])
            gradient.setColorAt(1, self._button_clicked_bottom[self.isDown()])
            brush = QtGui.QBrush(gradient)
            brush.setStyle(QtCore.Qt.LinearGradientPattern)
            p.setBrush(brush)
            p.setPen(QtGui.QPen(self.palette().shadow(), 1))
        else:
            p.setBrush(self.palette().light())
            p.setPen(QtGui.QPen(self.palette().shadow(), 1))

        p.drawPath(path)

        p.setPen(QtGui.QPen(self.palette().buttonText(), 1))
        p.setFont(self.font())

        font_width = width/2 - QtGui.QFontMetrics(p.font()).size(
            QtCore.Qt.TextSingleLine, self.text()
        ).width()/2

        font_height = height/2 + QtGui.QFontMetrics(p.font()).size(
            QtCore.Qt.TextSingleLine, self.text()
        ).height()/4
        p.drawText(QtCore.QPointF(font_width, font_height), self.text())

    def enterEvent(self, event: QtCore.QEvent) -> None:
        super(_SingleButton, self).enterEvent(event)

        self._button_clicked_bottom = {
            True: self.palette().midlight().color(),
            False: self.palette().light().color(),
        }

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        super(_SingleButton, self).leaveEvent(event)

        self._button_clicked_bottom = {
            True: self.palette().midlight().color(),
            False: self.palette().button().color(),
        }


class IncreaseDecreaseButton(QtWidgets.QWidget):
    left_clicked = QtCore.pyqtSignal()
    right_clicked = QtCore.pyqtSignal()

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(IncreaseDecreaseButton, self).__init__(parent)

        self._left_button = _SingleButton(self)
        self._left_button.setText('-')
        self._left_button.clicked.connect(lambda: self.left_clicked.emit())
        self._right_button = _SingleButton(self, left=False)
        self._right_button.setText('+')
        self._right_button.clicked.connect(lambda: self.right_clicked.emit())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._left_button)
        layout.addWidget(self._right_button)
        layout.setSpacing(0)
        self.setLayout(layout)

    def set_size(self, w: int, h: int) -> None:
        self._left_button.setFixedSize(int(w/2), h)
        self._right_button.setFixedSize(int(w/2), h)

    def set_left_enabled(self, enabled: bool):
        self._left_button.setEnabled(enabled)

    def set_right_enabled(self, enabled: bool):
        self._right_button.setEnabled(enabled)


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    panel = QtWidgets.QWidget()

    button = IncreaseDecreaseButton()
    button.setEnabled(True)
    button.left_clicked.connect(lambda: print('Left Clicked'))
    button.right_clicked.connect(lambda: print('Right Clicked'))
    # button.set_size(50, 25)

    ref_button = QtWidgets.QPushButton('Test')
    ref_button.setEnabled(False)

    ref_button_2 = QtWidgets.QPushButton('Test 2')
    ref_button_2.setEnabled(True)

    main_layout = QtWidgets.QHBoxLayout()
    main_layout.addWidget(button)
    main_layout.addStretch()
    main_layout.addWidget(ref_button)
    main_layout.addStretch()
    main_layout.addWidget(ref_button_2)
    panel.setLayout(main_layout)
    panel.show()

    app.exec()
