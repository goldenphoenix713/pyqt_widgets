"""
Created on Thu Mar 26 16:18:40 2020.

@author: Eddie
"""

from PyQt5 import QtWidgets, QtGui, QtCore


class RangeSlider(QtWidgets.QSlider):
    """A slider for ranges.

    This class provides a dual-slider for ranges, where there is a defined
    maximum and minimum, as is a normal slider, but instead of having a
    single slider value, there are 2 slider values.

    This class emits the same signals as the QSlider base class, as well as
    the sliderMoved signal.
    """

    #: Signal emitted when the slider is moved.
    sliderMoved = QtCore.pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        """Initialize the slider.

        Initializes the range slide, adding a second slider and defining
        how it works.

        """
        super(RangeSlider, self).__init__(*args, **kwargs)

        self._low = self.minimum()
        self._high = self.maximum()

        self.pressed_control = QtWidgets.QStyle.SC_None
        self.hover_control = QtWidgets.QStyle.SC_None
        self.click_offset = 0

        # 0 for the low, 1 for the high, -1 for both
        self.active_slider = 0

    def low(self) -> int:
        """Get the value of the low slider.

        Gets the value of the lower slider.

        Returns
        -------
        int
            The value of the low slider.

        """
        return self._low

    def set_low(self, low: int):
        """Set the value of the low slider.

        Sets the value of the lower slider.

        Parameters
        ----------
        low:
            The value the low slider will be set to.

        """
        self._low = low
        self.update()

    def high(self) -> int:
        """Get the value of the high slider.

        Gets the value of the higher slider.

        Returns
        -------
        int
            The value of the high slider.

        """
        return self._high

    def set_high(self, high: int):
        """Set the value of the high slider.

        Sets the value of the higher slider.

        Parameters
        ----------
        high:
            The value the high slider will be set to.

        """
        self._high = high
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent):
        """Paint the slider object.

        Runs when the object is drawn.

        Parameters
        ----------
        event:
            The event object.

        """
        painter = QtGui.QPainter(self)
        style = QtWidgets.QApplication.style()

        for i, value in enumerate([self._low, self._high]):
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            # Only draw the groove for the first slider, so it doesn't get
            # drawn on top of the existing ones every time
            if i == 0:
                opt.subControls = (QtWidgets.QStyle.SC_SliderGroove
                                   | QtWidgets.QStyle.SC_SliderHandle)
            else:
                opt.subControls = QtWidgets.QStyle.SC_SliderHandle

            if self.tickPosition() != self.NoTicks:
                opt.subControls |= QtWidgets.QStyle.SC_SliderTickmarks

            if self.pressed_control:
                opt.activeSubControls = self.pressed_control
                opt.state |= QtWidgets.QStyle.State_Sunken
            else:
                opt.activeSubControls = self.hover_control

            opt.sliderPosition = value
            opt.sliderValue = value
            style.drawComplexControl(
                    QtWidgets.QStyle.CC_Slider, opt, painter, self
                    )

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """Add new interactions on mouse clicks.

        Add new interactions for the range slider based on where the user
        clicks on the slider.

        Parameters
        ----------
        event:
            The event object.

        """
        event.accept()

        style = QtWidgets.QApplication.style()
        button = event.button()

        # In a normal slider control, when the user clicks on a point in the
        # slider's total range, but not on the slider part of the
        # control would jump the slider value to where the user clicked.
        # For this control, clicks which are not direct hits will slide both
        # slider parts

        if button:
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            self.active_slider = -1

            for i, value in enumerate([self._low, self._high]):
                opt.sliderPosition = value
                hit = style.hitTestComplexControl(
                        style.CC_Slider, opt, event.pos(), self
                        )
                if hit == style.SC_SliderHandle:
                    self.active_slider = i
                    self.pressed_control = hit

                    self.triggerAction(self.SliderMove)
                    self.setRepeatAction(self.SliderNoAction)
                    self.setSliderDown(True)
                    break

            if self.active_slider < 0:
                self.pressed_control = QtWidgets.QStyle.SC_SliderHandle
                self.click_offset = self._pixel_pos_to_range_value(
                        self._pick(event.pos())
                        )
                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
        else:
            event.ignore()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        """Add new interactions on mouse moves for click and drag.

        Add new interactions for the range slider based on where the user
        clicked on the slider and drags.

        Parameters
        ----------
        event:
            The event object.

        """
        if self.pressed_control != QtWidgets.QStyle.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
        new_pos = self._pixel_pos_to_range_value(self._pick(event.pos()))
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)

        if self.active_slider < 0:
            offset = new_pos - self.click_offset
            self._high += offset
            self._low += offset
            if self._low < self.minimum():
                diff = self.minimum() - self._low
                self._low += diff
                self._high += diff
            if self._high > self.maximum():
                diff = self.maximum() - self._high
                self._low += diff
                self._high += diff
        elif self.active_slider == 0:
            if new_pos >= self._high:
                new_pos = self._high - 1
            self._low = new_pos
        else:
            if new_pos <= self._low:
                new_pos = self._low + 1
            self._high = new_pos

        self.click_offset = new_pos

        self.update()

        self.sliderMoved.emit(self._low, self._high)

    def _pick(self, pt: QtCore.QPoint) -> int:
        if self.orientation() == QtCore.Qt.Horizontal:
            return pt.x()
        else:
            return pt.y()

    def _pixel_pos_to_range_value(self, pos: int):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        style = QtWidgets.QApplication.style()

        gr = style.subControlRect(
                style.CC_Slider, opt, style.SC_SliderGroove, self
                )
        sr = style.subControlRect(
                style.CC_Slider, opt, style.SC_SliderHandle, self
                )

        if self.orientation() == QtCore.Qt.Horizontal:
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
        else:
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1

        return style.sliderValueFromPosition(
                self.minimum(),
                self.maximum(),
                pos-slider_min,
                slider_max-slider_min,
                opt.upsideDown
                )


if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    slider = RangeSlider(QtCore.Qt.Horizontal)

    slider.setMinimum(0)
    slider.setMaximum(86400)
    slider.set_low(0)
    slider.set_high(86400)
    slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
    slider.setTickInterval(int(86400/12))
    slider.sliderMoved.connect(print)
    slider.show()
    app.exec()
