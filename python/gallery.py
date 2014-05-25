import os
import sys
import time
import utils
import gc
from PyQt4 import QtGui, QtCore
import icons
import controlBar

class DataModel(QtCore.QAbstractTableModel):
	def __init__(self, datain, col, thumbRes, parent=None):
		"""	Methods in this class sets up data/images to be
			visible in the table.
			Args:
				datain(list): 2D list where each item is a row
				col(int): number of columns to show in table
				thumbRes(tuple): resolution of the thumbnail
		"""
		QtCore.QAbstractListModel.__init__(self, parent)
		QtGui.QPixmapCache.setCacheLimit(100 * 1024)
		self._thumbRes = thumbRes
		self._listdata = datain
		self._col = col

	def colData(self, section, orientation, role):
		"""	makes the table column header display
			nothing.
		"""
		if role == QtCore.Qt.DisplayRole:
			return None
		return None

	def headerData(self, section, orientation, role):
		"""	Makes the header display nothing, if
			headerData is not defined numbers show up.
		"""
		if role == QtCore.Qt.DisplayRole:
			if orientation in [QtCore.Qt.Vertical, QtCore.Qt.Horizontal]:
				return None
		return None

	def rowCount(self, parent=QtCore.QModelIndex()):
		"""	Method sets the number of rows
		"""
		return len(self._listdata)

	def columnCount(self, parent):
		"""	sets the number of columsns
		"""
		return self._col

	def data(self, index, role):
		""" method sets the data/images to visible in table
		"""
		if not index.isValid():
			return None

		if role == QtCore.Qt.SizeHintRole:
			return  QtCore.QSize(*self._thumbRes)

		if role == QtCore.Qt.TextAlignmentRole:
			return QtCore.Qt.AlignCenter

		if role == QtCore.Qt.EditRole:
			row = index.row()
			column = index.column()
			try:
				fileName = os.path.split(self._listdata[row][column][0])[-1]
			except IndexError:
				return
			return fileName

		if role == QtCore.Qt.ToolTipRole:
			row = index.row()
			column = index.column()
			try:
				fileName = os.path.split(self._listdata[row][column][0])[-1]
			except IndexError:
				return
			exifData = "\n".join(self._listdata[row][column][1:])
			return QtCore.QString(exifData if exifData else fileName)

		if role == QtCore.Qt.DecorationRole:
			row = index.row()
			column = index.column()
			try:
				imageVal = self._listdata[row][column][0]
			# except IndexError:
			# 	return
			except TypeError:
				return

			pixmap = QtGui.QPixmapCache.find(imageVal)
			if not pixmap:
				pixmap = QtGui.QPixmap(imageVal).scaled(self._thumbRes[0], self._thumbRes[1], 
					QtCore.Qt.KeepAspectRatio | QtCore.Qt.SmoothTransformation)
				QtGui.QPixmapCache.insert(imageVal, pixmap)
			pixmap = QtGui.QPixmapCache.find(imageVal)
			return QtGui.QImage(pixmap)

	def flags(self, index):
		"""	This method sets the text in the cell editor selected
			and editable and enabled.
		"""
		return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

	def setData(self, index, value, role=QtCore.Qt.EditRole):
		"""	Sets teh data of each cell, double click to rename 
			the selected image.
		"""
		if role == QtCore.Qt.EditRole:
			row = index.row()
			column = index.column()
			try:
				newName = os.path.join(str(os.path.split(self._listdata[row][column][0])[0]),
				 str(value.toString()))
			except IndexError:
				return
			utils._renameFile(self._listdata[row][column][0], newName)
			self._listdata[row][column][0] = newName
			self.dataChanged.emit(index, index)
			return True
		return False

class GalleryUi(QtGui.QTableView):
	"""	methods that forms the UI of Image galery
	"""
	def __init__(self, window, imagesPathLst=None, parent=None):
		super(GalleryUi, self).__init__(parent)
		self._slideShowWin = window
		self.__sw = QtGui.QDesktopWidget().screenGeometry(self).width()
		self.__sh = QtGui.QDesktopWidget().screenGeometry(self).height()
		self.__animRate = 1200
		self._imagesPathLst = imagesPathLst
		self._thumb_width = 200
		self._thumb_height = self._thumb_width + 20
		uiSetupComplete = self._setUpWindow(initiate=True)

		if uiSetupComplete:
			self._startControlBar()
			self._connections()

	def closeEvent(self,event):
		# in case gallery is launched by Slideshow this is not needed
		if hasattr(self, 'bar'):
			self.bar.close()

	def _startControlBar(self):
		if not self._slideShowWin:
			self.bar = controlBar.ControlBar()
			self.bar.show()
			self.bar.galrBtn.hide()
			self.bar.pausBtn.hide()
			self.bar.backBtn.hide()
			self.bar.nextBtn.hide()
			self.bar.exitBtn.clicked.connect(self._exitGallery)
			self.bar.openBtn.clicked.connect(self.selectSetNewPath)

	def _exitGallery(self):
		if self._slideShowWin:
			self._slideShowWin.close()
			self._slideShowWin.bar.close()
		if not self._slideShowWin:
			self.bar.close()
		self.close()

	def _connections(self):
		# TODO: http://stackoverflow.com/questions/7782071/how-can-i-get-right-click-context-menus-for-clicks-in-qtableview-header
		# self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# self.connect(self, QtCore.SIGNAL(self.customContextMenuRequested(QtCore.QPoint)), self, QtCore.SLOT(displayMenu(QtCore.QPoint)))
		if self._slideShowWin:
			self._slideShowWin.bar.galrBtn.clicked[bool].connect(self._openSlideShow)

	def displayMenu(self, pos):
		self.menu = QtGui.QMenu()
		self.menu.addAction(self.close)
		self.menu.exec_(self.mapToGlobal(event.pos()))

	def selectSetNewPath(self):

		path = utils._browseDir("Select the directory that contains images")
		self._imagesPathLst = utils.ingestData(path)
		# sets model when new folder is choosen
		self.updateModel()

	def _setUpWindow(self, initiate=False):
		"""	Method to setup window frameless and fullscreen,
			setting up thumbnaul size and animation rate
		"""

		if not self._imagesPathLst:
			self.selectSetNewPath()
		# sets model once at startup when window is being drawn!
		if initiate:
			self.updateModel()
		self.setGeometry(0, 0, self.__sw, self.__sh)
		self.setColumnWidth(self._thumb_width, self._thumb_height)
		self.setShowGrid(False)
		self.setWordWrap(True)
		if self._slideShowWin:
			self.setWindowFlags(
					QtCore.Qt.Widget |
					QtCore.Qt.FramelessWindowHint | 
					QtCore.Qt.X11BypassWindowManagerHint
								)
			self.showFullScreen()
		else:
			self.show()

		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		self.selectionModel().selectionChanged.connect(self.selChanged)
		return True

	def updateModel(self):
		col = self.__sw/self._thumb_width 
		self._twoDLst = utils.convertToTwoDList(self._imagesPathLst, col)
		lm = DataModel(self._twoDLst, col,
			(self._thumb_width, self._thumb_height), self)
		self.setModel(lm)

	def selChanged(self):
		"""	Show selected image in gallery in SlideShow window.
		"""
		if self._slideShowWin:
			row = self.selectionModel().currentIndex().row()
			column = self.selectionModel().currentIndex().column()
			# if specific image is selected the slideshow opens paused.
			self._slideShowWin.playPause()
			self._slideShowWin.showImageByPath(self._twoDLst[row][column])

	def animateUpSlideShow(self):
		""" animate the slideshow window back up to view mode
			and starts the slideShowBase where it was paused.
		"""
		if self._slideShowWin:
			self.animateUpGallery()
			self.animation = QtCore.QPropertyAnimation(self._slideShowWin, "geometry")
			self._slideShowWin.bar.show()
			self._slideShowWin.bar.galrBtn.setIcon(QtGui.QIcon(':/images/galryIcon.png'))
			self.animation.setDuration(self.__animRate)
			self.animation.setStartValue(QtCore.QRect(0, self.__sh,
			 self.__sw, self.__sh))
			self.animation.setEndValue(QtCore.QRect(0, 0, self.__sw, self.__sh))
			self.animation.start()
			self._slideShowWin.activateWindow()
			self._slideShowWin.raise_()
			self._slideShowWin.playPause()

	def animateUpGallery(self):
		"""	animate the gallery window up to make slideshow visible
		"""
		self.animGallery = QtCore.QPropertyAnimation(self, "geometry")
		self.animGallery.setDuration(self.__animRate)
		self.animGallery.setStartValue(QtCore.QRect(0, 0, self.__sw, self.__sh))
		self.animGallery.setEndValue(QtCore.QRect(0, -(self.__sh), 
			self.__sw, self.__sh))
		self.animGallery.start()

	def keyPressEvent(self, keyevent):
		"""	Capture key to exit, next image, previous image,
			on Escape , Key Right and key left respectively.
		"""
		event = keyevent.key()
		if event == QtCore.Qt.Key_Escape:
			self._exitGallery()
		if event == QtCore.Qt.Key_Up:
			self._animateUpOpen()

	def _animateUpOpen(self):
		"""	this method calls the method that animate the windows,
			helps in separating toggle button call from keyboard
			key press calls
		"""
		self.workThread = WorkThread()
		self.connect( self.workThread, QtCore.SIGNAL("update(QString)"), self.animateUpSlideShow)
 		self.workThread.start()
		# self.animateUpSlideShow()

	def _openSlideShow(self, pressed):
		"""	use gallery/slideshow toggle button
		"""
		if not pressed:
			self._animateUpOpen()

class WorkThread(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

	def __del__(self):
		self.wait()

	def run(self):
		for i in range(1):
			time.sleep(0.3) # artificial time delay
			self.emit( QtCore.SIGNAL('update(QString)'), "from work thread " + str(i) )
			self.terminate()
		return

		
def main(imgLst=None):
	"""	method to start gallery standalone
	"""
	app = QtGui.QApplication(sys.argv)
	window =  GalleryUi(None, imgLst)
	window.raise_()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	current_path = os.getcwd()
	if len(sys.argv) > 1:
		current_path = sys.argv[1:]
	main(utils.ingestData(current_path))

