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
from controlBar import ControlBar as _ControlBar
from PyQt4 import QtGui, QtCore
import slideShowBase
import gallery


class SlideShowPics(QtGui.QMainWindow, slideShowBase.SlideShowBase):

	"""	SlideShowPics class defines the methods for UI and
		working logic
	"""
	def __init__(self, imgLst, num=0, exifFlag=False, flag=True, parent=None):
		super(SlideShowPics, self).__init__(parent)

		self.__animRate = 1200
		self.__imgLst = imgLst

		self.bar = _ControlBar()

		self._connections()

		slideShowBase.SlideShowBase.__init__(self, 
										imgLst=imgLst, 
										ppState=False, 
										count=num, 
										exifFlag=exifFlag, 
										animFlag=flag
											)
		self._sw = QtGui.QDesktopWidget().screenGeometry(self).width()
		self._sh = QtGui.QDesktopWidget().screenGeometry(self).height()

		self._prepairWindow()
		# hides the exif data of image by default
		self.overlayExifText.hide()

	def _connections(self):
		self.bar.backBtn.clicked.connect(self._backwardPlay)
		self.bar.nextBtn.clicked.connect(self._forwardPlay)
		self.bar.pausBtn.clicked.connect(self.playPause)
		self.bar.galrBtn.clicked[bool].connect(self._openGallery)
		self.bar.exitBtn.clicked.connect(self._exit)
		self.bar.openBtn.clicked.connect(self.__changeSlideShow)

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

	def __changeSlideShow(self):
		"""	this methdd is used to select a different folder to view
			slideshow, and updates the list which also updates gallery images
		"""
		# pause the slide show 
		self.playPause()
		curntPaths = utils._browseDir("Select Directory to SlideShow")
		if curntPaths:
			self.populateImagestoSlideShow(curntPaths)
			self.playPause()
			# always set to go forward when new path is set
			self._forwardPlay()
			if hasattr(self, 'galleryWin'):
				self.galleryWin.close()
			# updating the imgLst will update the gallery as well.
			self.__imgLst = utils.ingestData([curntPaths])

	def closeEvent(self, event):
		self.bar.close()
		self.close()
		if hasattr(self, 'galleryWin'):
			self.galleryWin.close()


	def _prepairWindow(self):
		if not self._imagesInList:
			msgBox = QtGui.QMessageBox()
			msgBox.setText("No Image found." )
			msgBox.setStandardButtons(msgBox.Cancel | msgBox.Open)
			if msgBox.exec_() == msgBox.Open:
				self.__changeSlideShow()
			else:
				sys.exit()
		self.bar.show()
		# Centre the sUI
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
		# self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self._buildUi()
		self.createActions()
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.showFullScreen()
		self.playPause()
		# Shows the first image
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
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setBackgroundRole(QtGui.QPalette.Base)
		self.label.setSizePolicy(QtGui.QSizePolicy.Ignored,
			QtGui.QSizePolicy.Ignored)
		sizePolicy = QtGui.QSizePolicy()
		sizePolicy.setHorizontalStretch(QtGui.QSizePolicy.Minimum)
		self.overlayExifText = QtGui.QLabel(self.label)
		self.overlayExifText.setScaledContents(True)
		self.overlayExifText.setSizePolicy(sizePolicy)
		self.overlayExifText.setStyleSheet("""
			QLabel {
				 color : blue;
				 background-color: rgba(0,0,0,30%);
				 border-radius: 6px;
				 padding: 10px;
					}
							""")
		self.overlayExifText.setAlignment(QtCore.Qt.AlignTop)
		layout = QtGui.QVBoxLayout(self.label)
		layout.setContentsMargins(0, 10, 0, 10)
		layout.addWidget(self.overlayExifText)
		self.setCentralWidget(self.label)

	def nextImage(self):
		"""	method to show next or previous image
			by overloading I don't have to mock showImageByPath
		"""
		super(SlideShowPics, self).nextImage()
		try:
			self.showImageByPath(self._imagesInList[self._count])
		except:
			self._count = len(self._imagesInList)
		# sets the direction
		self.setDirection()

	def showImageByPath(self, item):
		"""	shows image by path
		"""
		if item:
			image = QtGui.QImage(item[0])

			pp = QtGui.QPixmap.fromImage(image)
			self.label.setPixmap(pp.scaled(
					self.label.size(),
					QtCore.Qt.KeepAspectRatio,
					QtCore.Qt.SmoothTransformation))
			exif = "\n".join(item[1:])
			if not item[1:]:
				exif = "No Exif Data Available"
			self.overlayExifText.setText(exif)

	def keyPressEvent(self, keyevent):
		"""	Capture key to exit, next image, previous image,
			on Escape, Key Right and key left respectively.
		"""
		event = keyevent.key()
		if event == QtCore.Qt.Key_Escape:
			self._exit()
		if event == QtCore.Qt.Key_Left:
			self._backwardPlay()
		if event == QtCore.Qt.Key_Right:
			self._forwardPlay()
		if event == QtCore.Qt.Key_E:
			self.overlayExifText.show() if self.exifFlag  else self.overlayExifText.hide()
			self.showExifData()
		if event == 32:
			self._pause = self.playPause()
		if event == QtCore.Qt.Key_Up:
			self.galleryWin.raise_()
		if event == QtCore.Qt.Key_Down:
			self._animateUp()

	def _exit(self):
		"""	closes slideshow and gallery if open
		"""
		self.closeEvent(event=None)
		if hasattr(self, 'galleryWin'):
			self.galleryWin.close()

	def _animateUp(self):
		"""	shows gallery by animating up
		"""
		self.animateDownOpen()
		self.animateDowSlideShow()
		
	def _openGallery(self, pressed):
		""" method called to toggle slideshow/gallery
		"""
		if pressed:
			self._animateUp()

	def _backwardPlay(self):
		"""	plays the slideshow backward or go to previous image
		"""
		self.animFlag = False
		self.nextImage()

	def _forwardPlay(self):
		""" plays the slideshow forward or go to the next image
		"""
		self.animFlag = True
		self.nextImage()

	def animateDownOpen(self):
		"""	creates the gallery window and aniamtes it down
		"""
		self.galleryWin = gallery.GalleryUi(self, self.__imgLst)
		self.animGallery = QtCore.QPropertyAnimation(self.galleryWin, "geometry")
		self.animGallery.setDuration(self.__animRate)
		self.animGallery.setStartValue(QtCore.QRect(0, -(self._sh), self._sw, self._sh))
		self.animGallery.setEndValue(self.geometry())
		self.galleryWin.show()
		self.animGallery.start()

	def animateDowSlideShow(self):
		"""	animates down the slideshow window
		"""
		self.playPause()
		self.animation = QtCore.QPropertyAnimation(self, "geometry")
		self.animation.setDuration(self.__animRate)
		self.animation.setStartValue(self.geometry())
		self.animation.setEndValue(QtCore.QRect(0, self._sh, self._sw, self._sh))
		self.animation.start()
		# update the icon on galrBtn to slideshowBtnIcon
		self.bar.galrBtn.setIcon(QtGui.QIcon(':/images/slideShowBtnIcon.png'))

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
	main(utils.ingestData(curntPaths))
