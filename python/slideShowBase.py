import utils
<<<<<<< HEAD
=======
from PyQt4 import QtGui
>>>>>>> codeReview

class SlideShowBase(object):
	"""	SlideShowBase class contains methods that defines the 
		logic for SlideShow to plate forward or backword and 
		pause.
	"""
	def __init__(self, imgLst, ppState, count, exifFlag, animFlag):
		self._imagesInList = imgLst
		self._pause = ppState
		self._count = count
		self.exifFlag = exifFlag 
		self.animFlag = animFlag

	def populateImagestoSlideShow(self, path):
		"""	helper method to populate the list with paths 
			of images from path argument.
		"""
		self._imagesInList = utils.imageFilePaths([path])

	def showExifData(self):
		if self.exifFlag:
			self.exifFlag = False
			return True
		else:
			self.exifFlag = True
			return False

	def nextImage(self):
		"""	switch to next image or previous image
		"""
		if self._imagesInList:
			if self._count == len(self._imagesInList):
				self._count = 0

	def setDirection(self):
		"""	set direction of slideshow
		"""
		# forward
		if self.animFlag:
			self._count += 1
		# backward
		else:
			self._count -= 1

	def playPause(self):
		"""	toggle to play and pause the slideshow
		"""
		if not self._pause:
			self._pause = True
<<<<<<< HEAD
=======
			self.bar.pausBtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaStop))
>>>>>>> codeReview
			self.updateTimer.start(2500)
			return self._pause
		else:
			self._pause = False
			self.updateTimer.stop()
<<<<<<< HEAD
=======
			self.bar.pausBtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
>>>>>>> codeReview

