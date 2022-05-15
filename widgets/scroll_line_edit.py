"""
Created on Thu Mar 26 16:18:54 2020.

@author: Eddie
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class ScrollLineEdit(QtWidgets.QLineEdit):
    """A line edit with scrolling capabilities.

    This class is similar to a regular line edit box, except scrolling
    with a mouse wheel increases or decreases the value of the number.
    """

    #: Signal emitted when the mouse wheel is scrolled.
    wheel_scrolled = QtCore.pyqtSignal(int)

    def __init__(self, parent: QtWidgets.QWidget, *args, **kwargs):
        """Initialize the scroll line edit.

        Initializes the scroll line edit.

        """
        super(ScrollLineEdit, self).__init__(*args, **kwargs)
        self._parent = parent
        self._is_key_pressed = False
        self._parent.shift_pressed.connect(self._set_scroll_amount)

    def focusInEvent(self, event: QtGui.QFocusEvent):
        """Select the text in the edit box when it is clicked.

        Parameters
        ----------
        event:
            The event object.

        """
        QtCore.QTimer.singleShot(0, self.selectAll)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        """Change the value in the line edit with the scroll wheel.

        Increase or decrease the value of the number in the line edit

        Parameters
        ----------
        event:
            The event object.
        """
        delta = 1 if event.angleDelta().y() > 0 else -1
        delta = delta * 10**int(self._is_key_pressed)

        self.wheel_scrolled.emit(delta)
        event.accept()

    def _set_scroll_amount(self, pressed: bool):
        """
        Set the scroll amount to a small step or a large step based on if
        the shift key is pressed.

        Parameters
        ----------
        pressed:
            Whether the shift key is pressed.
        """
        self._is_key_pressed = pressed
