from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from unet import unet_predict as up



class Work(QThread):
    signal = pyqtSignal(str)
    def __init__(self,filepath,mod):
        super(Work,self).__init__()
        self.filepath = filepath
        self.mod = mod
        # self.textbox = massage
    def __del__(self):
        self.wait()
    def run(self):
        up.predict(self.filepath,self.mod)
        # self.textbox.append('complete!!!')
        self.signal.emit('complete!!!')
class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.title = 'building detection'
        self.left = 30
        self.top = 30
        self.width = 500
        self.height = 200
        self.setupUi(self)
        # self.retranslateUi(self)
        self.image_path = None
        self.model_path = None
        self.step = 0


    def setupUi(self, MainWindow):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.pushButton1 = QtWidgets.QPushButton("openimage",self)
        self.pushButton1.setGeometry(QtCore.QRect(100, 120, 75, 23))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.clicked.connect(self.openimage)

        self.pushButton2 = QtWidgets.QPushButton("openmodel",self)
        self.pushButton2.setGeometry(QtCore.QRect(190, 120, 75, 23))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.clicked.connect(self.openmodel)

        self.pushButton3 = QtWidgets.QPushButton("predict",self)
        self.pushButton3.setGeometry(QtCore.QRect(280, 120, 75, 23))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton3.clicked.connect(self.pred)

        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(400, 100)
        # self.textbox.setText("hello")
        # self.textbox.setGeometry(QtCore.QRect(10, 10, 200, 40))

        # self.pbar = QProgressBar(self)
        # self.pbar.setGeometry(20, 160, 400, 25)



        self.show()

    def openimage(self):
        self.image_path = QFileDialog.getOpenFileName(self,'choose','','Excel files(*.png , *.tif)')
        self.textbox.append("data:"+str(self.image_path[0]))

    def openmodel(self):
        self.model_path = QFileDialog.getOpenFileName(self,'choose','','Excel files(*.h5)')
        self.textbox.append("model:"+str(self.model_path[0]))


    def pred(self):
        print(str(self.image_path[0]),str(self.model_path[0]))
        if self.image_path and self.model_path:
            # self.textbox.append('wait......')
            self.thread = Work(str(self.image_path[0]),str(self.model_path[0]))
            self.thread.signal.connect(self.textbox.append)
            # self.thread = Work(str(self.image_path[0]),str(self.model_path[0]),self.textbox)
            self.thread.start()
            # up.predict(str(self.image_path[0]),str(self.model_path[0]))
            # # for i in self.step:
            # #     self.pbar.setValue(i)
            # self.textbox.append('complete!!!')
            # self.pbar.setValue(0)
        else:
            QMessageBox.question(self, "Message", 'error',
                                 QMessageBox.Ok, QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    # MainWindow.show()
    sys.exit(app.exec_())
