import unittest
import mox
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
		self.mox = mox.Mox()

	def tearDown(self):
		self.mox.UnsetStubs()
		self.mox.ResetAll()

	def test_isExtensionSupported(self):
		self.assertTrue(utils.isExtensionSupported("testFile.PNG"))
		self.assertTrue(utils.isExtensionSupported("testFile.jpg"))
		self.assertFalse(utils.isExtensionSupported("testFile.kkg"))


	def test_imageFilePaths(self):
		filePaths = self._filePaths
		fileList = ['file1.bmp']
		self.mox.StubOutWithMock(utils, 'getDirContent')
		dirContent = utils.getDirContent(filePaths[0]).AndReturn(fileList)
		self.mox.StubOutWithMock(utils,'ifFilePathExists')
		filePat = os.path.join(filePaths[0], dirContent[0])
		utils.ifFilePathExists(filePat).AndReturn(True)
		self.mox.StubOutWithMock(utils, 'isExtensionSupported')
		utils.isExtensionSupported(filePat).AndReturn(True)
		self.mox.ReplayAll()
		self.assertEquals(['/test/file/path/file1.bmp'], utils.imageFilePaths(filePaths))
		self.mox.VerifyAll()

	def test_getDirContent(self):
		self.assertRaises(OSError, utils.getDirContent, self._filePaths[0])

	def test_ifFilePathExists(self):
		self.assertFalse(utils.ifFilePathExists(self._filePaths[0]))
		self.assertTrue(utils.ifFilePathExists(__file__))


if __name__ == '__main__':
	unittest.main()


