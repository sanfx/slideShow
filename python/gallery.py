import sys
import os
import slideShowBase

from PyQt4 import QtGui, QtCore

class MyListModel(QtCore.QAbstractTableModel): 
	def __init__(self, window, datain, col, thumbRes, parent=None): 
		""" Methods in this class sets up data/images to be
			visible in the table.
			Args:
				datain(list): 2D list where each item is a row
				col(int): number of columns to show in table
				thumbRes(tuple): resolution of the thumbnail 
		"""
		QtCore.QAbstractListModel.__init__(self, parent) 
		self._slideShowWin = window
		self._thumbRes = thumbRes
		self._listdata = datain
		self.pixmap_cache = {}
		self._col = col

	def colData(self, section, orientation, role):
		if role == QtCore.Qt.DisplayRole:
			return None

	def headerData(self, section, orientation, role):
		if role == QtCore.Qt.DisplayRole:
			if orientation in [QtCore.Qt.Vertical, QtCore.Qt.Horizontal]:
				return None

	def rowCount(self, parent=QtCore.QModelIndex()): 
		return len(self._listdata) 

	def columnCount(self, parent):
		return self._col

	def data(self, index, role):
		""" method sets the data/images to visible in table
		"""
		if index.isValid() and role == QtCore.Qt.SizeHintRole:
			return  QtCore.QSize(*self._thumbRes)

		if index.isValid() and role == QtCore.Qt.TextAlignmentRole:
		 	return QtCore.Qt.AlignCenter

		if index.isValid() and role == QtCore.Qt.EditRole:
			row = index.row()
			column = index.column()
			try:
				fileName = os.path.split(self._listdata[row][column])[-1]
			except IndexError:
				return
			return fileName

		if index.isValid() and role == QtCore.Qt.ToolTipRole:
			row = index.row()
			column = index.column()
			try:
				# self.selectonChanged(row, column)
				fileName = os.path.split(self._listdata[row][column])[-1]
			except IndexError:
				return
			return QtCore.QString(fileName)

		if index.isValid() and role == QtCore.Qt.DecorationRole:
			row = index.row()
			column = index.column()
			try:
				value = self._listdata[row][column]
			except IndexError:
				return

			pixmap = None
			# value is image path as key
  			if self.pixmap_cache.has_key(value) == False:
				pixmap=self.generatePixmap(value)
				self.pixmap_cache[value] =  pixmap
			else:
				pixmap = self.pixmap_cache[value]
			return QtGui.QImage(pixmap).scaled(self._thumbRes[0],self._thumbRes[1], 
				QtCore.Qt.KeepAspectRatio)

	def generatePixmap(self, value):
		"""	generates a pixmap if already not incache
		"""
		pixmap=QtGui.QPixmap()
		pixmap.load(value)
		return pixmap

	def flags(self, index):
		return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if role == QtCore.Qt.EditRole:
			row = index.row()
			column = index.column()
			try:
				newName = os.path.join(str(os.path.split(self._listdata[row][column])[0]), str(value.toString()))
			except IndexError:
				return
			self.__renameFile(self._listdata[row][column], newName)
			self._listdata[row][column] = newName
			self.dataChanged.emit(index, index)
			return True
		return False

	# def selectonChanged(self, row, col):
	# 	print "Hello"
	# 	self._slideShowWin.showImageByPath(self._listdata[row][col])


	def __renameFile(self, fileToRename, newName):
		"""	method to rename a image name when double click
		"""
		try:
			os.rename(str(fileToRename), newName)
		except Exception, err:
			print err


class GalleryUi(QtGui.QTableView):
	"""	Class contains the methods that forms the
		UI of Image galery
	"""
	def __init__(self, window, imgagesPathLst=None):
		super(GalleryUi, self).__init__()
		self._slideShowWin = window
		self.__sw = QtGui.QDesktopWidget().screenGeometry(self).width()
		self.__sh = QtGui.QDesktopWidget().screenGeometry(self).height()
		self.__animRate = 1200
		self.setUpWindow(imgagesPathLst)

	def setUpWindow(self, images=None):
		"""	method to setup window frameless and fullscreen,
			setting up thumbnaul size and animation rate
		"""
		if not images:
			path = self._browseDir()
			images = slideShowBase.ingestData(path)
		thumbWidth = 200
		thumbheight = thumbWidth + 20
		self.setWindowFlags(
			QtCore.Qt.Widget |
			 QtCore.Qt.FramelessWindowHint | 
			 QtCore.Qt.X11BypassWindowManagerHint
			 )
		col = self.__sw/thumbWidth 
		self._twoDLst = convertToTwoDList(images, col)
		self.setGeometry(0, 0, self.__sw, self.__sh)
		self.showFullScreen()
		self.setColumnWidth(thumbWidth, thumbheight)
		self._lm = MyListModel(self._slideShowWin, self._twoDLst, col, (thumbWidth, thumbheight), self)
		self.setShowGrid(False)
		self.setWordWrap(True)
		self.setModel(self._lm)
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		self.selectionModel().selectionChanged.connect(self.selChanged)

	def selChanged(self):
		row = self.selectionModel().currentIndex().row()
		column = self.selectionModel().currentIndex().column()
		# if specific image is selected the slideshow opens paused.
		self._slideShowWin.playPause()
		self._slideShowWin.showImageByPath(self._twoDLst[row][column])

	def _browseDir(self):
		"""	method to browse path you want to
			view in gallery
		"""
		selectedDir = str(QtGui.QFileDialog.getExistingDirectory(None, 
				"Select Directory to SlideShow",
				os.getcwd()))
		if selectedDir:
			return selectedDir
		else:
			sys.exit()

	def animateUpSlideShow(self):
		""" animate the slideshow window back up
			to view mode and starts the slideShowBase
			where it was paused.
		"""
		self.animateUpGallery()
		self.animation = QtCore.QPropertyAnimation(self._slideShowWin, "geometry")
		self.animation.setDuration(self.__animRate);
		self.animation.setStartValue(QtCore.QRect(0, self.__sh, self.__sw, self.__sh))
		self.animation.setEndValue(QtCore.QRect(0, 0, self.__sw, self.__sh))
		self.animation.start()
		self._slideShowWin.activateWindow()
		self._slideShowWin.raise_()
		self._slideShowWin.playPause()


	def animateUpGallery(self):
		"""	animate the gallery window up to make slideshow visible
		"""
		self.animGallery = QtCore.QPropertyAnimation(self, "geometry")
		self.animGallery.setDuration(self.__animRate);
		self.animGallery.setStartValue(QtCore.QRect(0, 0, self.__sw, self.__sh))
		self.animGallery.setEndValue(QtCore.QRect(0, -(self.__sh), self.__sw, self.__sh))
		self.animGallery.start()

	def keyPressEvent(self, keyevent):
		"""	Capture key to exit, next image, previous image,
			on Escape , Key Right and key left respectively.
		"""
		event = keyevent.key()
		if event == QtCore.Qt.Key_Escape:
			self.close()
		if event == QtCore.Qt.Key_Up:
			self.animateUpSlideShow()

def convertToTwoDList(l, n):
	"""	Method to convert a list to two
		dimensional list for QTableView
	"""
	return [l[i:i+n] for i in range(0, len(l), n)]

def main():
	"""	method to start gallery standalone
	"""
	app = QtGui.QApplication(sys.argv)
	window =  GalleryUi(None)
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()