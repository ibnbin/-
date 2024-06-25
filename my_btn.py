from IPython.external.qt_for_kernel import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class my_btn(QLabel):
    click_signal = QtCore.pyqtSignal()
    def __init__(self,n,parent=None):
        super().__init__(parent)
        self.n1 = QPixmap(n)
        self.setPixmap(self.n1)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        self.setPixmap(self.n1)
        # 发射信号
        self.click_signal.emit()

