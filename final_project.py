import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from matplotlib import pyplot as plt
import math
from scipy.stats import norm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
#       App frame
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color:#444444;")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

#       Drawing frame
        self.splitter_fig = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_fig.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.splitter_fig.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.splitter_fig.setOrientation(QtCore.Qt.Vertical)
        self.splitter_fig.setObjectName("splitter_fig")
        self.splitter_fig.setStyleSheet(" background-image: url(); background-color: white; border-style: solid; border-width: 3px; border-radius: 5px; border-color: black; padding: 10px; margin-bottom: 30px; ")
        self.gridLayout.addWidget(self.splitter_fig,0,0,3,9)
        self.fig,self.ax = plt.subplots(figsize=(15, 5))
        self.ax.set(title='Ball Movement')
        self.projectile_fig = FigureCanvasQTAgg(self.fig)
        self.splitter_fig.addWidget(self.projectile_fig)

#       Distance Dial
        self.dial_distance = QtWidgets.QDial(self.centralwidget)
        self.dial_distance.setGeometry(QtCore.QRect(10, 10, 91, 101))
        self.dial_distance.setObjectName("dial_distance")
        self.dial_distance.setMaximum(9900)
        self.gridLayout.addWidget(self.dial_distance,3,0,3,3)
        self.dial_distance.valueChanged.connect(lambda: self.distanceChange())
        self.dial_distance.setNotchesVisible(True)
        self.dial_distance.setStyleSheet("background-color:#450101; color:#BA4A00;")

#       Angle Dial
        self.dial_angle = QtWidgets.QDial(self.centralwidget)
        self.dial_angle.setGeometry(QtCore.QRect(130, 10, 91, 101))
        self.dial_angle.setObjectName("dial_angle")
        self.gridLayout.addWidget(self.dial_angle,3,3,3,3)
        self.dial_angle.setMaximum(9900)
        self.dial_angle.valueChanged.connect(lambda: self.angleChange())
        self.dial_angle.setNotchesVisible(True)
        self.dial_angle.setStyleSheet("background-color:#450101; color: #BA4A00;")

#       Velocity Dial
        self.dial_velocity = QtWidgets.QDial(self.centralwidget)
        self.dial_velocity.setGeometry(QtCore.QRect(250, 10, 91, 101))
        self.dial_velocity.setObjectName("dial_velocity")
        self.dial_velocity.setMaximum(9900)
        self.gridLayout.addWidget(self.dial_velocity,3,6,3,3)
        self.dial_velocity.valueChanged.connect(lambda: self.velocityChange())
        self.dial_velocity.setNotchesVisible(True)
        self.dial_velocity.setStyleSheet("background-color:#450101; color: #BA4A00;")

#       Distance label
        self.label_distance = QtWidgets.QLabel(self.centralwidget)
        self.label_distance.setGeometry(QtCore.QRect(20, 110, 51, 16))
        self.label_distance.setObjectName("label_distance")
        self.gridLayout.addWidget(self.label_distance,6,1,1,1)
        self.label_distance.setStyleSheet("background-color: #bc5656; border-style: solid; border-color: black; border-width: 1px; border-radius: 10px; font: 16px; color: white; min-width: 8em; padding: 6px;")

#       Angle label
        self.label_angle = QtWidgets.QLabel(self.centralwidget)
        self.label_angle.setGeometry(QtCore.QRect(140, 110, 47, 13))
        self.label_angle.setObjectName("label_angle")
        self.label_angle.setStyleSheet("background-color: #bc5656; border-style: solid; border-color: black; border-width: 1px; border-radius: 10px; font: 16px; color: white; min-width: 8em; padding: 6px;")
        self.gridLayout.addWidget(self.label_angle,6,4,1,1)

#       Velocity label
        self.label_velocity = QtWidgets.QLabel(self.centralwidget)
        self.label_velocity.setGeometry(QtCore.QRect(260, 110, 47, 13))
        self.label_velocity.setObjectName("label_velocity")
        self.label_velocity.setStyleSheet("background-color: #bc5656; border-style: solid; border-color: black; border-width: 1px; border-radius: 10px; font: 16px; color: white; min-width: 8em; padding: 6px;")
        
        self.gridLayout.addWidget(self.label_velocity,6,7,1,1)

#       Calculate Button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 140, 321, 23))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton,7,4,1,1)
        self.pushButton.clicked.connect(lambda: self.calculate())
        self.pushButton.setStyleSheet("")
        self.pushButton.setStyleSheet("QPushButton{""font: bold 20px; color: white; background-color: #0e1013; border-style: solid; border-width: 0px; border-radius: 12px; border-color: black; margin: 15px 10px 0px 10px; padding-bottom: 0.5em; padding-top: 0.5em;""} QPushButton::hover{""font: bold 18px;""}")
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

#       results
        self.label_results = QtWidgets.QLabel(self.centralwidget)
        self.label_results.setGeometry(QtCore.QRect(20, 200, 301, 16))
        self.label_results.setObjectName("label_results")
        self.gridLayout.addWidget(self.label_results,9,3,1,3)
        self.label_results.setStyleSheet("font: bold 18px; color: black; background-color: white; border-style: solid; border-width: 2px; border-radius: 8px; border-color: black; padding: 0.5em; margin-top: 20px")


#       Calculations
        self.Goal_Height = 0
        self.angle = 0
        self.Initial_Velocity = 0
        self.T1 = 0
        self.T2 = 0

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 358, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.label_distance.setText(_translate("MainWindow", "Distance: "))
        self.label_velocity.setText(_translate("MainWindow", "Velocity: "))
        self.label_angle.setText(_translate("MainWindow", "Angle: "))

        self.pushButton.setText(_translate("MainWindow", "Calculate "))
        self.label_results.setText(_translate("MainWindow", "Maximum Height Reached = 0 m\n\nHeight of ball at goal plane = 0 m"))

#   Functions
    def distanceChange (self):
        self.Goal_Height = self.dial_distance.value()/100.0
        self.label_distance.setText(f'Distance: {str(self.Goal_Height)}')

    def angleChange(self):
        self.angle = self.dial_angle.value()/100.0
        self.label_angle.setText(f'Angle: {str(self.angle)}')

    def velocityChange(self):
        self.Initial_Velocity = self.dial_velocity.value()/100.0
        self.label_velocity.setText(f'Velocity: {str(self.Initial_Velocity)}')

    def calculate(self):
        Goal_Height = self.Goal_Height
        # in radians
        Initial_Angle = self.angle * math.pi / 180
        Initial_Velocity = self.Initial_Velocity
        if(Initial_Velocity == 0):
            self.label_results.setText(f"Ball does not move because its initial velocity was zero")
            self.ax.clear()
            self.ax.set(title='Ball Movement')
            self.projectile_fig.draw()
            return 
        Time = (Initial_Velocity * math.sin(Initial_Angle)) / 9.8
        Max_Height_Reached = Initial_Velocity * math.sin(Initial_Angle) * Time  - 0.5 * 9.8 * Time ** 2

        Half_distance = Initial_Velocity * math.cos(Initial_Angle) * Time
        Distance_remained = Goal_Height - Half_distance
        Time_last_half = Distance_remained / (Initial_Velocity * math.cos(Initial_Angle))
        Goal_Height = Max_Height_Reached - (0.5 * 9.8 * Time_last_half ** 2) 

        if (Goal_Height < 0):{
        self.label_results.setText(f"Maximum Height Reached = {Max_Height_Reached} m\n\nBall does not reach the goal plane")
        }
        else:{
        self.label_results.setText(f"Maximum Height Reached = {Max_Height_Reached} m\n\nBall hight at the goal plane arrival point = {Goal_Height} m")
        }
        self.goalheight=Goal_Height
        self.T1 = Time
        self.T2 = Time_last_half
        self.Draw()


    def Draw(self):

        Goal_Height = self.Goal_Height
        Initial_Velocity = self.Initial_Velocity
        Initial_Angle = self.angle
        T1 = self.T1
        T2 = self.T2

        Time = np.linspace(0, T1, 100)
        Time2 = np.linspace(0, T2, 100)
        RisingX = Initial_Velocity * T1 * np.cos(np.radians(Initial_Angle))
        MaxHeight = Initial_Velocity * T1 * np.sin(np.radians(Initial_Angle)) - 0.5 * 9.8 * T1 ** 2
        x1 = Initial_Velocity * Time * np.cos(np.radians(Initial_Angle))
        y1 = Initial_Velocity * Time * np.sin(np.radians(Initial_Angle)) - 0.5 * 9.8 * Time ** 2
        x2 = RisingX + Initial_Velocity * Time2 * np.cos(np.radians(Initial_Angle))
        y2 = MaxHeight - 0.5 * 9.8 * Time2 ** 2

        self.ax.cla()
        self.ax.set(title='Ball Movement')
        self.ax.plot(x2, y2, color='r', label="Falling Path ")
        self.ax.axvline(x=Goal_Height, linestyle='--', label='Goal')
        self.ax.plot(RisingX, MaxHeight, color='b', marker='o', label="Max Ball Height")
        self.ax.plot(x1, y1, color='g', label="Rising Ball ")

        self.ax.set_xlim(left=0)
        self.ax.set_ylim(bottom=0)

        self.ax.legend(bbox_to_anchor=(1.0, 1), loc='upper left')
        self.projectile_fig.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
