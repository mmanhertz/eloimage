from PySide import QtGui

from scaled_pixmap_label import ScaledPixmapLabel


class PictureArea(QtGui.QWidget):

    def __init__(self, left_image_path, right_image_path, parent=None):

        super(PictureArea, self).__init__(parent=parent)
        self.pic_left = None
        self.pic_right = None
        self.init_ui(left_image_path, right_image_path)

    def init_ui(self, left_image_path, right_image_path):

        hbox = QtGui.QHBoxLayout(self)

        self.set_pic_left(left_image_path)
        self.set_pic_right(right_image_path)

        hbox.addWidget(self.pic_left)
        hbox.addWidget(self.pic_right)
        self.setLayout(hbox)

    def set_pictures(self, left_image_path, right_image_path):
        self.set_pic_left(left_image_path)
        self.set_pic_right(right_image_path)

    def set_pic_left(self, image_path):
        self.pic_left = ScaledPixmapLabel(QtGui.QPixmap(image_path))

    def set_pic_right(self, image_path):
        self.pic_right = ScaledPixmapLabel(QtGui.QPixmap(image_path))
