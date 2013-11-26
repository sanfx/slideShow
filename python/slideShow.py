"""	This program is licensed under the BSD license.

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
import utils
from PyQt4 import QtGui,QtCore
import slideShowBase


class SlideShowPics(QtGui.QMainWindow, slideShowBase.SlideShowBase):

	"""	SlideShowPics class defines the methods for UI and
		working logic
	"""
	def __init__(self, imgLst, num=0, flag=True, parent=None):
		super(SlideShowPics, self).__init__(parent)
		slideShowBase.SlideShowBase.__init__(self, imgLst=imgLst, ppState=False, count=num, animFlag=flag)
		self.prepairWindow()

	def prepairWindow(self):
		if not self._imagesInList:
			msgBox = QtGui.QMessageBox()
			msgBox.setText("No Image found." )
			msgBox.setStandardButtons(msgBox.Cancel | msgBox.Open);
			if msgBox.exec_() == msgBox.Open:
				self.populateImagestoSlideShow(self._browseDir())
			else:
				sys.exit()
		# Centre UI
		screen = QtGui.QDesktopWidget().screenGeometry(self)
		size = self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
		self.setStyleSheet("QWidget{background-color: #000000;}")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self._buildUi()
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.showFullScreen()
		self.playPause()
		#Shows the first image
		self.showImageByPath(self._imagesInList[0])

	def _buildUi(self):
		self.label = QtGui.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.setCentralWidget(self.label)

	def _browseDir(self):
		selectedDir = str(QtGui.QFileDialog.getExistingDirectory(None, 
				"Select Directory to SlideShow",
				os.getcwd()))
		if selectedDir:
			return selectedDir
		else:
			sys.exit()

	def nextImage(self):
		super(SlideShowPics, self).nextImage()
		self.showImageByPath(self._imagesInList[self._count])

	def showImageByPath(self, path):
		if path:
			image = QtGui.QImage(path)
			pp = QtGui.QPixmap.fromImage(image)
			self.label.setPixmap(pp.scaled(
					self.label.size(),
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation))

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

def main(imgLst=None):
	app = QtGui.QApplication(sys.argv)
	window =  SlideShowPics(imgLst)
	window.show()
	window.raise_()
	sys.exit(app.exec_())

if __name__ == '__main__':
	curntPaths = os.getcwd()
	if len(sys.argv) > 1:
		curntPaths = sys.argv[1:]
	main(slideShowBase.ingestData(curntPaths))
