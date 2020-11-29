import sys
import main as m
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QProgressBar, QPushButton

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('./newspaper.png'))
        main_label = QLabel("\n\n            ***** 무럭 뉴스 네비게이터 *****\n\n   시각화를 원하시는 년도와 월을 선택해주세요.", self)
        main_label.setAlignment(Qt.AlignVCenter)
        font1 = main_label.font()
        font1.setPointSize(10)
        font1.setBold(True)
        main_label.setFont(font1)

        self.lbl = QLabel('년도', self)
        self.lbl.move(120, 130)

        self.lbl = QLabel('월', self)
        self.lbl.move(270, 130)

        self.btn = QPushButton('시각화', self)
        self.btn.move(150, 220)

        cb = QComboBox(self)
        cb.addItem('2009년')
        cb.addItem('2010년')
        cb.addItem('2011년')
        cb.addItem('2012년')
        cb.addItem('2013년')
        cb.addItem('2014년')
        cb.addItem('2015년')
        cb.addItem('2016년')
        cb.addItem('2017년')
        cb.addItem('2018년')
        cb.addItem('2019년')
        cb.move(105, 160)

        cb1 = QComboBox(self)
        cb1.addItem('1월')
        cb1.addItem('2월')
        cb1.addItem('3월')
        cb1.addItem('4월')
        cb1.addItem('5월')
        cb1.addItem('6월')
        cb1.addItem('7월')
        cb1.addItem('8월')
        cb1.addItem('9월')
        cb1.addItem('10월')
        cb1.addItem('11월')
        cb1.addItem('12월')
        cb1.move(245, 160)

        self.setWindowTitle('Muruk News Navigator')
        self.setGeometry(400, 400, 400, 300)

        self.btn.clicked.connect(lambda:m.main(cb.currentText()[:-1]+cb1.currentText()[:-1]))

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
