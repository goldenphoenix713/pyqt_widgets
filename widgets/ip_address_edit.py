from typing import Optional

from PyQt5 import QtWidgets, QtCore, QtGui


class IPAddressEdit(QtWidgets.QLineEdit):

    def __init__(self, *args, **kwargs):
        """Initialize the IPAddressEdit"""
        super(IPAddressEdit, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setInputMask("000.000.000.000; ")
        validator = IP4Validator()
        self.setValidator(validator)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """
        Allow for tabbing and shift-tabbing between sections.

        Parameters
        ----------
        event
            The event.
        """
        if event.key() in [QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab]:
            dots = [pos for pos, char
                    in enumerate(self.displayText())
                    if char == '.']

            if event.key() == QtCore.Qt.Key_Tab:
                print(self.cursorPosition())
                if self.cursorPosition() <= dots[0]:
                    new_position = dots[0] + 1
                elif dots[0] < self.cursorPosition() <= dots[1]:
                    new_position = dots[1] + 1
                elif dots[1] < self.cursorPosition() <= dots[2]:
                    new_position = dots[2] + 1
                else:
                    new_position = None
            else:
                if self.cursorPosition() > dots[2]:
                    new_position = dots[1] + 1
                elif dots[1] < self.cursorPosition() <= dots[2]:
                    new_position = dots[0] + 1
                elif dots[0] < self.cursorPosition() <= dots[1]:
                    new_position = 0
                else:
                    new_position = None

            if new_position is not None:
                self.setCursorPosition(new_position)

        else:
            super(IPAddressEdit, self).keyPressEvent(event)


class IP4Validator(QtGui.QValidator):
    """
    Validator for IP Addresses. Use in conjunction with mask set to:
        '000.000.000.000; ' or '000.000.000.000;_'
    """
    def __init__(self, parent: Optional[QtCore.QObject] = None):
        """
        Initialize the validator wit the superclass.

        Parameters
        ----------
        parent:
            The parent QObject, if any.
        """
        super(IP4Validator, self).__init__(parent)

    def validate(self, address, pos):
        if not address:
            return QtGui.QValidator.Acceptable, address, pos
        octets = address.split(".")
        size = len(octets)
        if size > 4:
            return QtGui.QValidator.Invalid, address, pos
        empty_octet = False
        for octet in octets:
            # check for mask symbols
            if not octet or octet == "___" or octet == "   ":
                empty_octet = True
                continue
            try:
                value = int(str(octet).strip(' _'))  # strip mask symbols
            except ValueError:
                return QtGui.QValidator.Intermediate, address, pos
            if value < 0 or value > 255:
                return QtGui.QValidator.Invalid, address, pos
        if size < 4 or empty_octet:
            return QtGui.QValidator.Intermediate, address, pos
        return QtGui.QValidator.Acceptable, address, pos


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    window = QtWidgets.QWidget()
    ip_edit = IPAddressEdit()
    other_edit = QtWidgets.QLineEdit()

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(ip_edit)
    layout.addWidget(other_edit)
    window.setLayout(layout)

    window.show()

    app.exec()
