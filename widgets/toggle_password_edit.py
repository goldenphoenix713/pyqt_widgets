"""
Created on May 1, 2020

@author: Eddie

Module that contains a QLineEdit subclass with a built-in icon button to
toggle the echo state.
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class TogglePasswordEdit(QtWidgets.QLineEdit):
    """A QLineEdit with a built-in icon button to toggle the echo state."""

    def __init__(self, *args, **kwargs):
        super(TogglePasswordEdit, self).__init__(*args, **kwargs)

        # Create two icons, one for hidden mode, and one for shown mode.
        self._hidden = QtGui.QIcon('icons/no_eye.png')
        self._shown = QtGui.QIcon('icons/eye.png')

        # Create the action to toggle the echo state of the QLineEdit
        # connect the triggered signal, and add it to the QLineEdit.
        self._action = QtWidgets.QAction(self._hidden, 'Show')
        self._action.triggered.connect(self._toggle_echo)
        self.addAction(self._action)

#         # Create the button to trigger the action
        self._button = QtWidgets.QToolButton(self)
        self._button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self._button.setDefaultAction(self._action)
        self._button.setStyleSheet('border: none')
        self._button.setIconSize(self._button.size())
        self._button.show()
        self._button.setCursor(QtCore.Qt.ArrowCursor)

        # Default state of the QLineEdit echo is Password mode
        self.setEchoMode(QtWidgets.QLineEdit.Password)

        # Fix any sizing issues
        if not self.testAttribute(QtCore.Qt.WA_Resized):
            self.adjustSize()

        # Set the layout of the button in the QLineEdit
        self._set_layout()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super(TogglePasswordEdit, self).resizeEvent(event)
        self._set_layout()

    def _toggle_echo(self):
        """
        Toggle the state of the echo mode.
        """
        if self.echoMode() == self.Normal:
            self.setEchoMode(self.Password)
            self._action.setText('Show')
            self._action.setIcon(self._hidden)
        else:
            self.setEchoMode(self.Normal)
            self._action.setText('Hide')
            self._action.setIcon(self._shown)

    def _set_layout(self):
        """
        Set the layout of the QLineEdit with the toggle button on the right
        """
        # Get the contents geometry
        contents = self.contentsRect()

        # Set button size to be a square based on the height of the contents
        button_size = QtCore.QSize(contents.height(), contents.height())

        margins = self.textMargins()
        geom = QtCore.QRect(contents.topRight(), button_size)
        self._button.setGeometry(geom.translated(
            int(-button_size.width() * 1.1), 0)
        )
        margins.setRight(int(button_size.width() * 1.1))

        self.setTextMargins(margins)


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    passwordEdit = TogglePasswordEdit()
    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(passwordEdit)
    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.show()

    app.exec()
