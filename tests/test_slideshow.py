import unittest
import mox
import sys
import os
from PyQt4 import QtGui
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), 
                                               '../python/') ))
import slideShow
import utils

class TestSlideShow(unittest.TestCase):
	"""	docstring for TestSlideShow
	"""
	def setUp(self):
		self.mox = mox.Mox()
		self.imgLst = ['/folder/test/images/test1.jpg', '/folder/test/images/test2.JPG',
		'/folder/test/images/test3.png', '/folder/test/images/test4.PNG']

	def tearDown(self):
		self.mox.UnsetStubs()
		self.mox.ResetAll()

	def test_nextImage(self):
		app = QtGui.QApplication([])
		self.show = slideShow.SlideShowPics(imgLst=self.imgLst, ui=False)
		self.mox.StubOutWithMock(self.show, 'prepairWindow')
		self.show.prepairWindow()
		self.mox.StubOutWithMock(self.show, 'showImageByPath')
		self.show.showImageByPath(self.imgLst[1])
		self.show.nextImage()
		# self.mox.ReplayAll()
		self.assertEquals(1, self.show._count)
		self.assertEquals(self.imgLst[1], self.show._imagesInList[1])
		# self.mox.VerifyAll()

	def test_nextImage_animFlag_False(self):
		app = QtGui.QApplication([])
		self.show = slideShow.SlideShowPics(num=2, flag=False, imgLst=self.imgLst, ui=False)
		self.mox.StubOutWithMock(self.show, 'prepairWindow')
		self.show.prepairWindow()
		self.mox.StubOutWithMock(self.show, 'showImageByPath')
		self.show.showImageByPath(self.imgLst[2])
		self.show.nextImage()		
		self.assertEquals(1, self.show._count)
		self.assertEquals(self.imgLst[2], self.show._imagesInList[2])


if __name__ == '__main__':
	unittest.main()
