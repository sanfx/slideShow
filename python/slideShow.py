"""
This program is licensed under the BSD license.

Copyright (c) 2013, Sanjeev Kumar
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

	* Redistributions of source code must retain the above copyright notice, 
	  this list of conditions and the following disclaimer.
	* Redistributions in binary form must reproduce the above copyright notice, 
	  this list of conditions and the following disclaimer in the documentation 
	  and/or other materials provided with the distribution.
	* Neither the name of the Dino Interactive nor the names of its contributors 
	  may be used to endorse or promote products derived from this software 
	  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import os


from PyQt4 import QtGui,QtCore


class SlideShowPics(QtGui.QMainWindow):

	"""	SlideShowPics class defines the methods for UI and
		working logic
	"""
	def __init__(self, path, imgLst):
		super(SlideShowPics, self).__init__()
		self._path = path
		self._imageCache = []
		self._imagesInList = imgLst
		self._pause = False
		self._count = 0
		self.animFlag = True
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.prepairWindow()
		self.nextImage()

	def prepairWindow(self):
		# Centre UI
		screen = QtGui.QDesktopWidget().screenGeometry(self)
		size = self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
		self.setStyleSheet("QWidget{background-color: #000000;}")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.buildUi()
		self.showFullScreen()
		self.playPause()

	def buildUi(self):
		self.label = QtGui.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.setCentralWidget(self.label)

	def getAllImages(self):
		return  tuple(os.path.join(self._path,each) for each in self._imagesInList)

	def nextImage(self):
		if not self._imageCache:
			self._imageCache = self.getAllImages()

		if self._imageCache:
			if self._count == len(self._imageCache):
				self._count = 0

			self.showImageByPath(
					self._imageCache[self._count])

			if self.animFlag:
				self._count += 1
			else:
				self._count -= 1


	def showImageByPath(self, path):
		if path:
			image = QtGui.QImage(path)
			pp = QtGui.QPixmap.fromImage(image)
			self.label.setPixmap(pp.scaled(
					self.label.size(),
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation))

	def playPause(self):
			if not self._pause:
				self._pause = True
				self.updateTimer.start(2500)
				return self._pause
			else:
				self._pause = False
				self.updateTimer.stop()

	def keyPressEvent(self, keyevent):
		"""	Capture key to exit, next image, previous image,
			on Escape , Key Right and key left respectively.
		"""
		event = keyevent.key()
		if event == QtCore.Qt.Key_Escape:
			self.close()
		if event == QtCore.Qt.Key_Left:
			self.animFlag = False
			self.nextImage()
		if event == QtCore.Qt.Key_Right:
			self.animFlag = True
			self.nextImage()
		if event == 32:
			self._pause = self.playPause()

	def _openFolder(self):
		selectedDir = str(QtGui.QFileDialog.getExistingDirectory(
			self,
			"Select Directory to SlideShow",
			os.getcwd()))
		if selectedDir:
			return selectedDir

def isExtensionSupported(filename):
	"""	Supported extensions viewable in SlideShow
	"""
	if filename.endswith('PNG') or filename.endswith('png') or\
	 filename.endswith('JPG') or filename.endswith('jpg'):
		return True

def main(curntPath):
	imgLst =  os.listdir(curntPath)
	_allowdImages = []
	for image in imgLst:
		if isExtensionSupported(image):
			_allowdImages.append(image)
	if any(imageSel for imageSel in _allowdImages if os.path.isfile(os.path.join(curntPath, imageSel))):
		app = QtGui.QApplication(sys.argv)
		window =  SlideShowPics(curntPath, _allowdImages)
		window.show()
		window.raise_()
		app.exec_()
	else:
		print "No Image found in %s" % curntPath

if __name__ == '__main__':
	curntPath = os.getcwd()
	if len(sys.argv) > 1:
		if os.path.exists(sys.argv[1]):
			curntPath = sys.argv[1]

	main(curntPath)
