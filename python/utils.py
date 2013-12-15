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
	try:
		f = open(filePath, 'rb')
	except OSError:
		return
	tags = exifread.process_file(f)
	exifData = {}
	if tags:
		# print "Showing exif data for image '%s':" % os.path.basename(filePath)
		for tag, data in tags.iteritems():
			yield "%s: %s" % (tag, data)

# print str(getExifData('/Users/sanjeevkumar/Pictures/tempting/yjytjh.jpg'))
