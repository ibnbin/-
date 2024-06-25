import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDesktopWidget, QMessageBox
from tetrise2 import Tetrise
from 界面end import E_Widget
from my_btn import my_btn

class T_Widget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.startWidget()

    def startWidget(self):
        title_le = QLabel(self)
        title_le.setPixmap(QPixmap('resource/img/tetris.png'))

        start_le = my_btn('start.png',self)
        start_le.move(150, 150)
        start_le.click_signal.connect(self.game)

        end_le = my_btn('end.png',self)
        end_le.move(160, 200)
        end_le.click_signal.connect(self.close_Widegt)


        self.setFixedSize(380, 270)
        self.setWindowTitle('tetrise')
        self.setStyleSheet('background-color:rgb(255,255,255)')
        self.show()

    def game(self):
        t = Tetrise()
        self.close()
        t.main()
        e = E_Widget()


    def center(self):
        # 获取窗口
        qr = self.frameGeometry()
        # 获取屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中间
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def close_Widegt(self):
        reply = QMessageBox.question(self, '提示','是否退出游戏', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = T_Widget()
    # e = EndWidget()
    sys.exit(app.exec_())