"""
Created on May 1, 2020

@author: Eddie

Module that contains a QLineEdit subclass with a built-in icon button to
toggle the echo state.
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class LabeledLineEdit(QtWidgets.QLineEdit):

    def __init__(self, *args, left_label: str = '', right_label: str = '',
                 **kwargs):
        super(LabeledLineEdit, self).__init__(*args, **kwargs)
        self._left_label = QtWidgets.QLabel(left_label, parent=self)
        self._left_label.setCursor(QtCore.Qt.ArrowCursor)
        self._left_label.show()

        self._right_label = QtWidgets.QLabel(right_label, parent=self)
        self._right_label.setCursor(QtCore.Qt.ArrowCursor)
        self._right_label.show()

        self._set_layout()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(LabeledLineEdit, self).resizeEvent(event)
        self._set_layout()

    def set_left(self, label_text: str):
        self._left_label.setText(label_text)
        self._set_layout()

    def set_right(self, label_text: str):
        self._right_label.setText(label_text)
        self._set_layout()

    def setText(self, a0: str) -> None:
        super(LabeledLineEdit, self).setText(a0)
        self._set_layout()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        super(LabeledLineEdit, self).keyPressEvent(a0)
        self._set_layout()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        super(LabeledLineEdit, self).mousePressEvent(a0)
        self._set_layout()

    def _set_layout(self):
        """
        Set the layout of the QLineEdit with the label on the left
        """
        # Get the contents geometry
        contents = self.contentsRect()

        # Set the label width to the text width
        left_label_width = self._left_label.fontMetrics().width(
            self._left_label.text()
        )

        right_label_width = self._left_label.fontMetrics().width(
            self._right_label.text()
        )

        if self.text():
            text_width = self.fontMetrics().width(self.text())

            # Set label size and position within the line edit
            left_label_size = QtCore.QSize(left_label_width,
                                           contents.height())
            right_label_size = QtCore.QSize(right_label_width,
                                            contents.height())

            geom_left = QtCore.QRect(QtCore.QPoint(3, 0), left_label_size)
            geom_right = QtCore.QRect(
                QtCore.QPoint(left_label_width + text_width + 3, 0),
                right_label_size
            )
            self._left_label.setGeometry(geom_left)
            self._left_label.show()
            self._right_label.setGeometry(geom_right)
            self._right_label.show()

            # Set the line edit text margins to not overlap the label
            margins = self.textMargins()
            margins.setLeft(left_label_width)
            self.setTextMargins(margins)

        else:
            self._left_label.hide()
            self._right_label.hide()
            margins = self.textMargins()
            margins.setLeft(0)
            self.setTextMargins(margins)
