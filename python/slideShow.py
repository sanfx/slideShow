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
import gallery


class SlideShowPics(QtGui.QMainWindow, slideShowBase.SlideShowBase):

	"""	SlideShowPics class defines the methods for UI and
		working logic
	"""
	def __init__(self, imgLst, num=0, flag=True, parent=None):
		super(SlideShowPics, self).__init__(parent)
		qtstrImgLst = QtCore.QStringList(imgLst)
		self.__animRate = 1200
		slideShowBase.SlideShowBase.__init__(self, imgLst=qtstrImgLst, ppState=False, count=num, animFlag=flag)
		self._sw = QtGui.QDesktopWidget().screenGeometry(self).width()
		self._sh = QtGui.QDesktopWidget().screenGeometry(self).height()
		self.__imgLst = imgLst
		self.prepairWindow()


	# def resizeEvent(self, event):    
	# 	self.label.resize(event.size())
	# 	# self.overlayExifText.resize(event.size())
	# 	event.accept()

	def print_(self):
		dialog = QtGui.QPrintDialog(self.printer, self)
		if dialog.exec_():
			painter = QtGui.QPainter(self.printer)
			rect = painter.viewport()
			size = self.label.pixmap().size()
			size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
			painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
			painter.setWindow(self.label.pixmap().rect())
			painter.drawPixmap(0, 0, self.label.pixmap())

	def zoomIn(self):
		self.label.scaleImage(1.25)

	def zoomOut(self):
		self.label.scaleImage(0.8)

	def normalSize(self):
		self.label.adjustSize()
		self.scaleFactor = 1.0

	def fitToWindow(self):
		fitToWindow = self.fitToWindowAct.isChecked()
		self.scrollArea.setWidgetResizable(fitToWindow)
		if not fitToWindow:
			self.normalSize()

		self.updateActions()

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
		self.setStyleSheet("""
			QWidget{
			background-color: #000000;
			}
			QMenu { 
			font-size:12px;  
			color:white;  
			background-color:qlineargradient(x1:0, y1:0, x1:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);
			}
			""")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self._buildUi()
		self.createActions()
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.showFullScreen()
		self.playPause()
		#Shows the first image
		self.showImageByPath(self._imagesInList[0])

	def open(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
				QtCore.QDir.currentPath())
		if fileName:
			image = QtGui.QImage(fileName)
			if image.isNull():
				QtGui.QMessageBox.information(self, "Image Viewer",
						"Cannot load %s." % fileName)
				return

			self.label.setPixmap(QtGui.QPixmap.fromImage(image))
			self.scaleFactor = 1.0

			self.printAct.setEnabled(True)
			self.fitToWindowAct.setEnabled(True)
			self.updateActions()

			if not self.fitToWindowAct.isChecked():
				self.label.adjustSize()

	def contextMenuEvent(self, event):
		"""	Shows right click menu
		"""
		menu = self.createMenus()
		action = menu.exec_(self.mapToGlobal(event.pos()))

	def createMenus(self):
		menu = QtGui.QMenu(self)
		self.fileMenu = QtGui.QMenu("&File", self)
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.printAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		self.viewMenu = QtGui.QMenu("&View", self)
		self.viewMenu.addAction(self.zoomInAct)
		self.viewMenu.addAction(self.zoomOutAct)
		self.viewMenu.addAction(self.normalSizeAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.fitToWindowAct)

		self.menuBar().addMenu(self.fileMenu)
		self.menuBar().addMenu(self.viewMenu)
		menu.addMenu(self.fileMenu)
		menu.addMenu(self.viewMenu)
		return menu

	def createActions(self):
		self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
				triggered=self.open)

		self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
				enabled=False, triggered=self.print_)

		self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
				triggered=self.close)

		self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
				shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

		self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
				shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

		self.normalSizeAct = QtGui.QAction("&Normal Size", self,
				shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

		self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
				enabled=False, checkable=True, shortcut="Ctrl+F",
				triggered=self.fitToWindow)

	def _buildUi(self):
		self.label = QtGui.QLabel()
		self.overlayExifText = QtGui.QLabel(self.label)
		self.overlayExifText.setSizePolicy(QtGui.QSizePolicy.Ignored,
			QtGui.QSizePolicy.Ignored)
		self.overlayExifText.setStyleSheet("QLabel { color : blue; }")
		self.overlayExifText.setAlignment(QtCore.Qt.AlignTop)
		self.label.setBackgroundRole(QtGui.QPalette.Base)
		self.label.setSizePolicy(QtGui.QSizePolicy.Ignored,
			QtGui.QSizePolicy.Ignored)
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
		"""	 by overloading I don't have to mock showImageByPath
		"""
		super(SlideShowPics, self).nextImage()
		self.showImageByPath(self._imagesInList[self._count])
		self.setDirection()

	def showImageByPath(self, path):
		if path:
			image = QtGui.QImage(path)
			pp = QtGui.QPixmap.fromImage(image)
			self.label.setPixmap(pp.scaled(
					self.label.size(),
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation))
			self.overlayExifText.setText("\n".join(list(utils.getExifData((path)))))

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
		if event == QtCore.Qt.Key_Up:
			print "pressed up key"
		if event == QtCore.Qt.Key_Down:
			self.launchGallery()

	def launchGallery(self):
		self.animateDowSlideShow()
		self.animateDownOpen()


	def animateDownOpen(self):
		self.galleryWin = gallery.GalleryUi(self, self.__imgLst)
		self.animGallery = QtCore.QPropertyAnimation(self.galleryWin, "geometry")
		self.animGallery.setDuration(self.__animRate)
		self.animGallery.setStartValue(QtCore.QRect(0, -(self._sh), self._sw, self._sh))
		self.animGallery.setEndValue(self.geometry())
		self.galleryWin.show()
		self.animGallery.start()


	def animateDowSlideShow(self):
		self.playPause()
		self.animation = QtCore.QPropertyAnimation(self, "geometry")
		self.animation.setDuration(self.__animRate)
		self.animation.setStartValue(self.geometry())
		self.animation.setEndValue(QtCore.QRect(0, self._sh, self._sw, self._sh))
		self.animation.start()

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
