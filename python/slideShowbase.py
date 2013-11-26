import utils

class SlideShowBase(object):
	"""	SlideShowBase class contains methods that defines the 
		logic for SlideShow to plate forward or backword and 
		pause.
	"""
	def __init__(self, imgLst, ppState, count, animFlag):
		self._imagesInList = imgLst
		self._pause = ppState
		self._count = count
		self.animFlag = animFlag

	def populateImagestoSlideShow(self, path):
		"""	helper method to populate the list with paths 
			of images from path argument.
		"""
		self._imagesInList = utils.imageFilePaths([path])

	def nextImage(self):
		"""	switch to next image or previous image
		"""

		if self._imagesInList:
			if self._count == len(self._imagesInList):
				self._count = 0
		# set direction of slideshow
		if self.animFlag:
			self._count += 1
		else:
			self._count -= 1

	def playPause(self):
		"""	toggle to play and pause the slideshow
		"""
		if not self._pause:
			self._pause = True
			self.updateTimer.start(2500)
			return self._pause
		else:
			self._pause = False
			self.updateTimer.stop()

def ingestData(paths):
	"""	This method is used to create a list containing
		images path to slideshow.
	"""
	if isinstance(paths, list):
		imgLst = utils.imageFilePaths(paths)

	elif isinstance(paths, str):
		imgLst =  utils.imageFilePaths([paths])
	else:
		print " You can either enter a list of paths or single path"
	return imgLst
