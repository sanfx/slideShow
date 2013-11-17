from PyQt4 import QtGui, QtCore
import sys
import icons

		
class ControlBar(QtGui.QWidget):
	"""	docstring for ControlBar"""
	def __init__(self, parent=None):
		super(ControlBar, self).__init__(parent)
		self.resize(360, 70)
		screen = QtGui.QDesktopWidget().screenGeometry(self)
		size = self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/1.1)
		self.setStyleSheet("""
			QWidget{
			opacity: 50;
			background-color: rgba(204,204,204,10);
			}
			""")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.buildUi()

	def mousePressEvent(self, event):
		self.offset = event.pos()

	def mouseMoveEvent(self, event):
		try:
			x=event.globalX()
			y=event.globalY()
			x_w = self.offset.x()
			y_w = self.offset.y()
			self.move(x-x_w, y-y_w)
		except: pass   

	def paintEvent(self, ev):
		painter = QtGui.QPainter(self)
		gradient = QtGui.QLinearGradient(QtCore.QRectF(self.rect()).topLeft(),QtCore.QRectF(self.rect()).bottomLeft())
		gradient.setColorAt(0.0, QtCore.Qt.black)
		gradient.setColorAt(0.4, QtCore.Qt.gray)
		gradient.setColorAt(0.8, QtCore.Qt.black)
		painter.setBrush(gradient)
		painter.drawRoundedRect(0, 0, 360, 70, 20.0, 20.0)
		
	def buildUi(self):
		self.hoelayout = QtGui.QHBoxLayout()
		self.openBtn = RoundEdgeButton()
		self.openBtn.setIcon(QtGui.QIcon(':/images/openBtnIcon.png'))
		self.backBtn = RoundEdgeButton()
		self.backBtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaSeekBackward))
		self.pausBtn = RoundEdgeButton()
		self.pausBtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaStop))
		self.nextBtn = RoundEdgeButton()
		self.nextBtn.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaSeekForward))
		self.galrBtn = RoundEdgeButton()
		self.galrBtn.setCheckable(True)
		self.galrBtn.setIcon(QtGui.QIcon(':/images/galryIcon.png'))
		self.exitBtn = RoundEdgeButton()
		self.exitBtn.setIcon(QtGui.QIcon(':/images/exitBtnIcon.png'))

		self.hoelayout.addStretch(1)
		self.hoelayout.addWidget(self.openBtn)
		self.hoelayout.addStretch(1)
		self.hoelayout.addWidget(self.backBtn)
		self.hoelayout.addStretch(1)
		self.hoelayout.addWidget(self.pausBtn)
		self.hoelayout.addStretch(1)
		self.hoelayout.addWidget(self.nextBtn)
		self.hoelayout.addStretch(1)
		self.hoelayout.addWidget(self.galrBtn)
		self.hoelayout.addStretch(1)
		self.hoelayout.addWidget(self.exitBtn)
		self.hoelayout.addStretch(1)
		self.setLayout(self.hoelayout)

class RoundEdgeButton(QtGui.QPushButton):
	""" docstring for RoundEdgeButton"""
	def __init__(self, parent=None):
		super(RoundEdgeButton, self).__init__(parent)
		self.setIconSize(QtCore.QSize(22,22))
		self.setStyleSheet("""
		QPushButton{
		opacity: 50;            
		background-color: rgba(204,204,204,10);
		}
		""")
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	win = ControlBar()
	win.show()
	win.raise_()
	sys.exit(app.exec_())