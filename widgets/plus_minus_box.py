"""
Created on May 7, 2020

@author: eddie
A LineEdit class with a button on left/right side.
"""
from typing import Optional

from PyQt5 import QtWidgets, QtCore, QtGui


class PlusMinusBox(QtWidgets.QLineEdit):
    """
    A QLineEdit with a built-in icon button to toggle the echo state.

    """

    value_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent: QtWidgets.QWidget = None, minimum: int = 0,
                 maximum: Optional[int] = None, default: int = 0):
        super(PlusMinusBox, self).__init__(parent)

        # Create the action to toggle the echo state of the QLineEdit
        # connect the triggered signal, and add it to the QLineEdit.
        self._leftAction = QtWidgets.QAction('-')
        self._leftAction.triggered.connect(self._decrease)
        self._rightAction = QtWidgets.QAction('+')
        self._rightAction.triggered.connect(self._increase)
        self.addAction(self._rightAction)

        self._validator = QtGui.QIntValidator()
        self.set_range(bottom=minimum, top=maximum)

        self.setValidator(self._validator)

        self._value = default if minimum is None else minimum

        self.setText(str(self.value))
        self.setAlignment(QtCore.Qt.AlignCenter)

        # Create the buttons to trigger the actions
        self._leftButton = QtWidgets.QToolButton(self)
        self._leftButton.setDefaultAction(self._leftAction)
        self._leftButton.setStyleSheet('border: none')
        self._leftButton.show()
        self._leftButton.setCursor(QtCore.Qt.ArrowCursor)

        self._rightButton = QtWidgets.QToolButton(self)
        self._rightButton.setDefaultAction(self._rightAction)
        self._rightButton.setStyleSheet('border: none')
        self._rightButton.show()
        self._rightButton.setCursor(QtCore.Qt.ArrowCursor)

        # Fix any sizing issues
        if not self.testAttribute(QtCore.Qt.WA_Resized):
            self.adjustSize()

        # Set the layout of the button in the QLineEdit
        self._set_layout()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        """
        Overwrite parent method to add resetting the layout after a resize.
        """
        super(PlusMinusBox, self).resizeEvent(event)
        self._set_layout()

    def _decrease(self):
        """Decrease the value of the box."""
        valid = self._validator.validate(str(self.value - 1), 0)
        if valid[0] == self._validator.Acceptable:
            self._value -= 1
            self.setText(str(self.value))
            self.value_changed.emit(self._value)

    def _increase(self):
        """Increase the value of the box."""
        valid = self._validator.validate(str(self.value + 1), 0)
        if valid[0] == self._validator.Acceptable:
            self._value += 1
            self.setText(str(self.value))
            self.value_changed.emit(self._value)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        super(PlusMinusBox, self).keyPressEvent(event)
        text = self.text()
        self._value = int(text)

    @property
    def value(self) -> int:
        """Get the value of the box."""
        return self._value

    @value.setter
    def value(self, new_value: int):
        """Set the value of the box."""
        if (self._validator.validate(str(new_value), 0)[0]
                == self._validator.Acceptable):
            self._value = new_value
            self.setText(str(new_value))

    def set_range(self, bottom: Optional[int] = None,
                  top: Optional[int] = None):
        """
        Set the range of possible values for the box.

        Parameters
        ----------
        bottom:
            The new bottom value for the box.
        top:
            The new top value for the box.
        """
        self.set_bottom(bottom)
        self.set_top(top)

    def set_bottom(self, bottom: Optional[int]):
        """
        Set the minimum bottom value.

        Parameters
        ----------
        bottom:
            The new bottom value.

        """
        if bottom is not None:
            self._validator.setBottom(bottom)
        else:
            self._validator.setBottom(-2147483648)

    def set_top(self, top: Optional[int]):
        """
        Set the maximum top value.

        Parameters
        ----------
        top:
            THe new top value.
        """
        if top is not None:
            self._validator.setTop(top)
        else:
            self._validator.setTop(2147483647)

    def _set_layout(self):
        """
        Set the layout of the QLineEdit with the toggle button on the right
        """
        # Get the contents geometry
        contents = self.contentsRect()

        # Set button size to be a square based on the height of the contents
        button_size = QtCore.QSize(contents.height(), contents.height())

        margins = self.textMargins()
        geom = QtCore.QRect(contents.topLeft(), button_size)
        self._leftButton.setGeometry(geom)
        margins.setLeft(button_size.width())

        geom = QtCore.QRect(contents.topRight(), button_size)
        self._rightButton.setGeometry(
            geom.translated(-button_size.width(), 0))
        margins.setRight(button_size.width())

        self.setTextMargins(margins)


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    box = PlusMinusBox()

    layout = QtWidgets.QHBoxLayout()
    layout.addStretch()
    layout.addWidget(box)
    layout.addStretch()
    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.show()

    app.exec()
