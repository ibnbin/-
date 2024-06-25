import sys

from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from my_btn import my_btn


class E_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.endWidget()

    def endWidget(self):
        title_le = QLabel(self)
        title_le.setPixmap(QPixmap('resource/img/gameover.png'))
        title_le.move(0, 50)

        restart_le = my_btn('resource/img/restart.png', self)
        restart_le.move(50, 150)
        # restart_le.click_signal.connect(self.start_game)

        end_le = my_btn('resource/img/over.png', self)
        end_le.move(250, 150)
        # end_le.click_signal.connect(self.close_Widegt)

        self.setFixedSize(380, 220)
        self.setWindowTitle('tetrise')
        self.setStyleSheet('background-color:rgb(255,255,255)')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = E_Widget()
    sys.exit(app.exec_())