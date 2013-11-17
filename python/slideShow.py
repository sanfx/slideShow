import sys
import os
import time

from PyQt4 import QtGui,QtCore


class SlideShowPics(QtGui.QWidget):
    """docstring for SlideShowPics"""
    def __init__(self, path):
        super(SlideShowPics, self).__init__()
        self._path = path
        self._img_cache = []
        self.animFlag = True
        self.count = 0
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.start(2500)
        self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.next_image)
        self.prepair_qt()

    def prepair_qt(self):
        # Centre UI
        screen = QtGui.QDesktopWidget().screenGeometry(self)
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.build_ui()
        self.showFullScreen()

    def build_ui(self):
        filename = self._path
        self.layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def get_all_images(self):
        return  tuple(os.path.join(self._path,each) for each in os.listdir(self._path)
            if os.path.isfile(os.path.join(self._path,each)) and each.endswith('png') or each.endswith('jpg'))

    def next_image(self):
        if not self._img_cache:
            self._img_cache = self.get_all_images()

        if self._img_cache:
            if self.count == len(self._img_cache):
                self.count = 0

            self.show_image_by_path(
                    self._img_cache[self.count])

            if self.animFlag:
                self.count += 1
            else:
                self.count -= 1
        else:
            message = "No Image found in %s" % os.getcwd()
            print message
            self.close()

    def show_image_by_path(self, path):
        if path:
            image = QtGui.QImage(path)
            pp = QtGui.QPixmap.fromImage(image)
            self.label.setPixmap(pp.scaled(
                    self.label.size(),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))

    def keyPressEvent(self, keyevent):
        """
            Capture key to execute and exit
            on Enter and Escape respectively.
        """
        if keyevent.key() == QtCore.Qt.Key_Escape:
            self.close()
        if keyevent.key() == QtCore.Qt.Key_Left:
            self.animFlag = False
        if keyevent.key() == QtCore.Qt.Key_Right:
            self.animFlag = True

    def _open_folder(self):
        selectedDir = str(QtGui.QFileDialog.getExistingDirectory(
            self,
            "Select Directory to SlideShow",
            os.path.expanduser("~")))
        if selectedDir:
            return selectedDir


def main(cur_path):
    if any(each.endswith('png') or each.endswith('jpg') for each in os.listdir(cur_path)):
        app = QtGui.QApplication(sys.argv)
        window =  SlideShowPics(cur_path)
        window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        window.activateWindow()
        window.show()
        app.exec_()
    else:
        print "No Image found in %s" % cur_path

if __name__ == '__main__':
    cur_path = os.getcwd()
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            cur_path = sys.argv[1]

    main(cur_path)
