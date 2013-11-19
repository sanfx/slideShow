import os
import sys

def isExtensionSupported(filename):
	"""	Supported extensions viewable in SlideShow
	"""
	if filename.endswith('.PNG') or filename.endswith('.png') or\
	 filename.endswith('.JPG') or filename.endswith('.jpg'):
		return True

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

