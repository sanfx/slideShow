import os
import sys
import exifread
from PyQt4 import QtGui, QtCore


class InvalidArgmentException(Exception):
	pass


ALLOWABLE = frozenset(str(f) for f in QtGui.QImageReader.supportedImageFormats())

def isExtensionSupported(filename):
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
				if os.path.exists(selFile) and isExtensionSupported(selFile):
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

def deleteFile(path):
	if os.path.exists(path):
            os.system('osascript -e \'tell app "Finder" '
                      + 'to move the POSIX file "'
                      + os.path.abspath(path) + '" to trash\'')
        else:
            print "Error:", os.path.abspath(path), "does not exist"

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
