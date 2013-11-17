from PyQt4 import QtGui,QtCore
import sys
import os
import time

class SlideShowPics(QtGui.QWidget):
	"""docstring for SlideShowPics"""
	def __init__(self, path):
		super(SlideShowPics, self).__init__()
		# Centre UI
		screen = QtGui.QDesktopWidget().screenGeometry(self)
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
		QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
		self._path = path
		self.animFlag = True
		self.buildUi()
		self.count = 0
		self.showFullScreen()
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.updateTimer.start(2500)  

	def allImages(self):
		return  tuple(os.path.join(self._path,each) for each in os.listdir(self._path) 
			if os.path.isfile(os.path.join(self._path,each)) and each.endswith('png') or each.endswith('jpg'))

	def nextImage(self):
		if self.allImages():
			if self.count != len(self.allImages()):
				image = QtGui.QImage(self.allImages()[self.count])
				pp = QtGui.QPixmap.fromImage(image)
				self.label.setPixmap(pp.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
			else:
				self.count = 0
			if self.animFlag:
				self.count += 1
			else:
				self.count -= 1
		else:
			message = "No Image found in %s" % os.getcwd()
			print message
			self.close()

	def keyPressEvent(self, keyevent):
		"""	Capture key to execute and exit 
			on Enter and Escape respectively.
		"""
		if keyevent.key() == QtCore.Qt.Key_Escape:
			self.close()
		if keyevent.key() == QtCore.Qt.Key_Left:
			self.animFlag = False
		if keyevent.key() == QtCore.Qt.Key_Right:
			self.animFlag = True

	def _openFolder(self):
		selectedDir = str(QtGui.QFileDialog.getExistingDirectory(
			self,"Select Directory to SlideShow",os.path.expanduser("~")))
		if selectedDir:
			return selectedDir

	def buildUi(self):
		filename = self._path
		self.layout = QtGui.QHBoxLayout()
		self.label = QtGui.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.layout.addWidget(self.label)
		self.setLayout(self.layout)


def main():
	curntPath = os.getcwd()
	if any(each.endswith('png') or each.endswith('jpg') for each in os.listdir(curntPath)):	
		app = QtGui.QApplication(sys.argv)
		window =  SlideShowPics(curntPath)
		window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
		window.activateWindow()
		window.show()
		app.exec_()
	else:
		print "No Image found in %s" % os.getcwd()

if __name__ == '__main__':
	main()
