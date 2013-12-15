import os
import sys
import exifread
from PyQt4 import QtGui

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

def getExifData(filePath):
	"""	Gets exif data from image
	"""
	try:
		f = open(filePath, 'rb')
	except OSError:
		return
	tags = exifread.process_file(f)
	exifData = {}
	if tags:
		for tag, data in tags.iteritems():
			yield "%s: %s" % (tag, data)

def convertToTwoDList(l, n):
	"""	Method to convert a list to two
		dimensional list for QTableView
	"""
	return [l[i:i+n] for i in range(0, len(l), n)]

def _renameFile(fileToRename, newName):
	"""	method to rename a image name when double click
	"""
	try:
		os.rename(str(fileToRename), newName)
	except Exception, err:
		print err

def _browseDir(label):
	"""	method to browse path you want to
		view in gallery
	"""
	selectedDir = str(QtGui.QFileDialog.getExistingDirectory(None, 
			label,
			os.getcwd()))
	if selectedDir:
		return selectedDir
	else:
		sys.exit()

def generatePixmap(value):
	"""	generates a pixmap if already not incache
	"""
	pixmap=QtGui.QPixmap()
	pixmap.load(value)
	return pixmap
