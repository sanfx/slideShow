import os
import sys
from PyQt4 import QtGui,QtCore

def isExtensionSupported(filename):
	"""	Supported extensions viewable in SlideShow
	"""
	reader = QtGui.QImageReader()
	ALLOWABLE = [str(each) for each in reader.supportedImageFormats()]
	return filename.lower()[-3:] in ALLOWABLE

def imageFilePaths(paths):
	imagesWithPath = []
	for _path in paths:
		dirContent = getDirContent(_path)
		for each in dirContent:
			selFile = os.path.join(_path, each)
			if ifFilePathExists(selFile) and isExtensionSupported(selFile):
				imagesWithPath.append(selFile)
	return list(set(imagesWithPath))

def ifFilePathExists(selFile):
	return os.path.isfile(selFile)

def getDirContent(path):
	try:
		return os.listdir(path)
	except OSError:
		raise OSError("Provided path '%s' doesn't exists." % path)


def animateDownOpen(window, startPos, endPos, sh, sw):
	animGallery = QtCore.QPropertyAnimation(window, "geometry")
	animGallery.setDuration(500);
	animGallery.setStartValue(QtCore.QRect(0, startPos, sw, sh))
	animGallery.setEndValue(QtCore.QRect(0, endPos, sw, sh))
	window.show()
	window.activateWindow()
	window.raise_()
	animGallery.start()