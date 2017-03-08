from PySide import QtGui, QtCore


class ScaledPixmapLabel(QtGui.QLabel):
    """The ScaledPixmapLabel contains a pixmap, which is correctly resized
    with the label itself.

    """
    def __init__(self, pixmap, *args, **kwargs):
        QtGui.QLabel.__init__(self)
        self._pixmap = pixmap
        self.setSizePolicy(QtGui.QSizePolicy.Ignored,
                           QtGui.QSizePolicy.Ignored)
        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

    def resizeEvent(self, event):
        self._update()

    def change_pixmap(self, pixmap):
        self._pixmap = pixmap
        self._update()

    def _update(self):
        self.setPixmap(self._pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio))