"""
Created on May 4, 2020

@author: Eddie
"""

from typing import Optional

from PyQt5 import QtWidgets, QtCore, QtGui


class ToggleSwitch(QtWidgets.QAbstractButton):

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None,
                 track_radius: int = 8, thumb_radius: int = 11):
        super(ToggleSwitch, self).__init__(parent)

        # Set the new button to be checkable and a fixed size.
        self.setCheckable(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                           QtWidgets.QSizePolicy.Fixed)

        # Set the size of the track and thumb
        self._trackRadius = track_radius
        self._thumbRadius = thumb_radius

        # Set animation duration
        self._anim = 100

        # Define some parameters based on the sizes.
        self._margin = max(0, self._thumbRadius - self._trackRadius)
        self._baseOffset = max(self._thumbRadius, self._trackRadius)
        self._endOffset = {
            True: lambda: self.width() - self._baseOffset,
            False: lambda: self._baseOffset,
        }
        self._offset = self._baseOffset

        # Define the look (colors and opacity) of the button
        palette = self.palette()

        if self._thumbRadius > self._trackRadius:
            self._trackColor = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumbColor = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._trackOpacity = 0.5
        else:
            self._thumbColor = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._trackColor = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._trackOpacity = 1

        # Set the cursor for the button to be a pointing hand
        self.setCursor(QtCore.Qt.PointingHandCursor)

    # Set the offset property and additional rules for setting.
    # Used to determine the position of the thumb (circle) part of the button.

    @QtCore.pyqtProperty(int)
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, value: int):
        self._offset = value
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        """
        Return the sizeHint of the button.

        Returns
        -------
        QtCore.QSize
            The sizeHint of the button.
        """
        return QtCore.QSize(
            4 * self._trackRadius + 2 * self._margin,
            2 * self._trackRadius + 2 * self._margin,
        )

    def setChecked(self, checked: bool):
        """
        Set the checked state of the button and update the offset of the thumb.

        Parameters
        ----------
        checked:
            Whether the button is to be set to checked or unchecked.
        """
        super(ToggleSwitch, self).setChecked(checked)
        self.offset = self._endOffset[checked]()

    def set_animation_duration(self, value: int):
        """
        Set the animation duration.

        Parameters
        ----------
        value:
            The duration of the animation (seconds)
        """
        self._anim = value

    def animation_duration(self) -> int:
        """
        Get the animation duration.
        Returns
        -------
        int
            The animation duration (seconds).

        """
        return self._anim

    def resizeEvent(self, event: QtGui.QResizeEvent):
        """
        Determine how the offset it affected during a resizeEvent

        Parameters
        ----------
        event:
            The event object.
        """
        super(ToggleSwitch, self).resizeEvent(event)
        self.offset = self._endOffset[self.isChecked()]()

    def paintEvent(self, _):
        """
        Update the look of the button. Runs whenever the button changes.
        """

        # Create the painter object
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing, True)
        p.setPen(QtCore.Qt.NoPen)
        track_opacity = self._trackOpacity
        thumb_opacity = 1.0

        # Change the look of the button based on if it's enabled or not.
        if self.isEnabled():
            track_brush = self._trackColor[self.isChecked()]
            thumb_brush = self._thumbColor[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()

        # Draw the track
        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._trackRadius,
            self._trackRadius,
        )

        # Draw the thumb
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        # noinspection PyPropertyAccess
        p.drawEllipse(
            self.offset - self._thumbRadius,
            self._baseOffset - self._thumbRadius,
            2 * self._thumbRadius,
            2 * self._thumbRadius,
        )

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        super(ToggleSwitch, self).mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self._animate_toggle()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        super(ToggleSwitch, self).keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Space:
            self._animate_toggle()

    def _animate_toggle(self):
        """
        Animate the button when the toggle state is changed.
        """
        anim = QtCore.QPropertyAnimation(self, b'offset', self)
        anim.setDuration(self._anim)
        # noinspection PyPropertyAccess
        anim.setStartValue(self.offset)
        anim.setEndValue(self._endOffset[self.isChecked()]())
        anim.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    toggle1 = ToggleSwitch(track_radius=8, thumb_radius=11)
    toggle1.toggled.connect(print)
    toggle2 = ToggleSwitch(track_radius=11, thumb_radius=8)
    toggle2.toggled.connect(print)

    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(toggle1)
    layout.addWidget(toggle2)
    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.show()

    app.exec()
