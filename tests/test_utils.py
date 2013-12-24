import unittest
import mox
import stubout
import sys
import os
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), 
                                               '../python/') ))

import utils


class TestUtils(unittest.TestCase):
	"""	docstring for Test_Utils
	"""

	def setUp(self):
		self._filePaths = ["/test/file/path"]
		self.__stubs = stubout.StubOutForTesting()
		self.imgLst = ['/folder/test/images/test1.jpg', '/folder/test/images/test2.JPG',
		'/folder/test/images/test3.png', '/folder/test/images/test4.PNG']
		self.mox = mox.Mox()

	def tearDown(self):
		self.mox.UnsetStubs()
		self.mox.ResetAll()

	def test_ingestData_string(self):
		# monkeypatch
		self.__stubs.Set(utils, 'imageFilePaths', lambda x: self.imgLst[0])
		listData = utils.ingestData(self.imgLst[0])
		self.assertEquals(self.imgLst[0], listData)

	def test_ingestData_list(self):
		# monkeypatch
		self.__stubs.Set(utils, 'imageFilePaths', lambda x: self.imgLst)
		listData = utils.ingestData(self.imgLst)
		self.assertEquals(self.imgLst, listData)

	def test_imageFilePaths(self):
		filePaths = self._filePaths
		fileList = ['file1.bmp']
		self.mox.StubOutWithMock(utils, 'getDirContent')
		dirContent = utils.getDirContent(filePaths[0]).AndReturn(fileList)
		self.mox.StubOutWithMock(os.path,'exists')
		filePat = os.path.join(filePaths[0], dirContent[0])
		os.path.exists(filePat).AndReturn(True)
		self.mox.StubOutWithMock(utils, 'isExtensionSupported')
		utils.isExtensionSupported(filePat).AndReturn(True)
		self.mox.StubOutWithMock(utils,'getExifData')
		tempLst = utils.getExifData(filePat).AndReturn([filePat])
		self.mox.ReplayAll()
		self.assertEquals('/test/file/path/file1.bmp', utils.imageFilePaths(filePaths)[0][0])
		self.mox.VerifyAll()

	def test_getDirContent(self):
		self.assertRaises(OSError, utils.getDirContent, self._filePaths[0])


if __name__ == '__main__':
	unittest.main()


