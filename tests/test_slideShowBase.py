import unittest
import mox
import stubout
import sys
import os

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), 
                                               '../python/') ))
from slideShowBase import SlideShowBase as _slideShowBase
import slideShowBase
import utils


class TestSlideShow(unittest.TestCase):
	"""	docstring for TestSlideShow
	"""
	def setUp(self):
		self.mox = mox.Mox()
		self.__stubs = stubout.StubOutForTesting()
		self.imgLst = ['/folder/test/images/test1.jpg', '/folder/test/images/test2.JPG',
		'/folder/test/images/test3.png', '/folder/test/images/test4.PNG']

	def tearDown(self):
		self.mox.UnsetStubs()
		self.mox.ResetAll()

	def test_nextImage(self):
		self.show = _slideShowBase(imgLst=self.imgLst, ppState=False, count=0, animFlag=True)
		self.show.nextImage()
		self.assertEquals(1, self.show._count)
		self.assertEquals(self.imgLst[1], self.show._imagesInList[1])

	def test_nextImage_animFlag_False(self):
		self.show = _slideShowBase(imgLst=self.imgLst, ppState=False, count=2, animFlag=False)
		self.show.nextImage()		
		self.assertEquals(1, self.show._count)
		self.assertEquals(self.imgLst[2], self.show._imagesInList[2])

	def test_ingestData_list(self):
		# monkeypatch
		self.__stubs.Set(utils, 'imageFilePaths', lambda x: self.imgLst)
		listData = slideShowBase.ingestData(self.imgLst)
		self.assertEquals(self.imgLst, listData)

	def test_ingestData_string(self):
		# monkeypatch
		self.__stubs.Set(utils, 'imageFilePaths', lambda x: self.imgLst[0])
		listData = slideShowBase.ingestData(self.imgLst[0])
		self.assertEquals(self.imgLst[0], listData)

if __name__ == '__main__':
	unittest.main()
