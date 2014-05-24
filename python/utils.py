import os
import sys
import exifread
from PyQt4 import QtGui, QtCore
from itertools import izip_longest


class InvalidArgmentException(Exception):
	pass


ALLOWABLE = frozenset(str(f) for f in QtGui.QImageReader.supportedImageFormats())

def _isExtensionSupported(filename):
	"""	Supported extensions viewable in SlideShow

		Args:
			filename(str): file path with extensions
	"""
	return os.path.splitext(filename)[-1].split('.')[-1].lower() in ALLOWABLE

def imageFilePaths(paths):
	if all(paths):
		imagesWithPath = []
		tempList = []

		for _path in paths:
			dirContent = os.listdir(_path)
			for each in dirContent:
				selFile = os.path.join(_path, each)
				if os.path.exists(selFile) and _isExtensionSupported(selFile):
					tempList = getExifData(selFile)
					tempList.insert(0, selFile)
					imagesWithPath.append(tempList)
		return imagesWithPath

def getExifData(filePath):
	"""	Gets exif data from image
	"""
	bad_tags = ('EXIF Tag 0x9009', 'MakerNote Tag 0x0099',
				'EXIF UserComment')
	try:
		with open(filePath, 'rb') as f:
			return ["%s: %s" % (tag, data) 
        for tag, data in exifread.process_file(f).iteritems() 
        if tag not in bad_tags]
	except OSError:
		return
	
def convertToTwoDList(iterable, n, fillvalue=None):
	"""	Method to convert a list to two
		dimensional list for QTableView

		Args:
			iterable(list): list of lists containing image paths
			n(int): number of columns
			fillvalue(list): a single list item containing the image path
	"""	
	return list(izip_longest(*[iter(iterable)]*n, fillvalue=fillvalue))


def _renameFile(fileToRename, newName):
	"""	method to rename a image name when double click
	"""
	try:
		os.rename(str(fileToRename), newName)
	except OSError as err:
		msgBox = QtGui.QMessageBox()
		msgBox.setText("Unable to rename file.\n Error: %s" % err)
		msgBox.exec_()

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
		msgRetVal = QtGui.QMessageBox.question(None, "SlideShow Viewer",
						"Do you want to quit ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if msgRetVal == 16384:
			# user cancelled it!
			sys.exit()

def ingestData(paths):
	"""	This method is used to create a list containing
		images path to slideshow.
	"""
	if isinstance(paths, list):
		return imageFilePaths(paths)
	elif isinstance(paths, str):
		return  imageFilePaths([paths])
	else:
		return None
