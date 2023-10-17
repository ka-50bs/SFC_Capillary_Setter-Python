# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerVMVeSI.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PyQt5 import QtCore
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import numpy as np
import AICam 
import cv2


class Ui_MainWindow(object):
    def __init__(self):
        self.RightCam = AICam.CapCam()
        self.LeftCam = AICam.CapCam()
        
        self.RightCam_Channel = 'r'
        self.LeftCam_Channel = 'r' 

        self.RightCam_Exposition = -3
        self.LeftCam_Exposition = -3

        self.LeftCam.init_cam(id_cam=1, exp=-0)
        self.RightCam.init_cam(id_cam=0, exp=-0)

        pass
    
    def LeftCam_Exposition_Update(self):
        self.LeftCam_Exposition = self.LeftCam_Exposition_Box.value()
        self.LeftCam.init_cam(id_cam=1, exp=self.LeftCam_Exposition)
        print('left' + str(self.LeftCam_Exposition))

    def RightCam_Exposition_Update(self):
        self.RightCam_Exposition = self.RightCam_Exposition_Box.value()
        self.RightCam.init_cam(id_cam=0, exp=self.RightCam_Exposition)
        print('right' + str(self.RightCam_Exposition))

    def LeftCam_Update_Edges(self):
        self.LeftCam.cap_init(channel=self.LeftCam_Channel, inverse=self.LeftCam_SlopeDown_CheckBox.isChecked(), treshold=self.LeftCam_STDTresholdDoubleSpinBox.value())

    def RightCam_Update_Edges(self):
        self.RightCam.cap_init(channel=self.RightCam_Channel, inverse=self.RightCam_SlopeDown_CheckBox.isChecked(),  treshold=self.RightCam_STDTresholdDoubleSpinBox.value())

    def LeftCam_Update_Channel(self):
        if self.LeftCam_R_Button.isChecked():
            self.LeftCam_Channel = 'r'
        if self.LeftCam_G_Button.isChecked():
            self.LeftCam_Channel = 'g'
        if self.LeftCam_B_Button.isChecked():
            self.LeftCam_Channel = 'b'
        if self.LeftCam_Gray_Button.isChecked():
            self.LeftCam_Channel = 'gray'

    def RightCam_Update_Channel(self):
        if self.RightCam_R_Button.isChecked():
            self.RightCam_Channel = 'r'
        if self.RightCam_G_Button.isChecked():
            self.RightCam_Channel = 'g'
        if self.RightCam_B_Button.isChecked():
            self.RightCam_Channel = 'b'
        if self.RightCam_Gray_Button.isChecked():
            self.RightCam_Channel = 'gray'

    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 1000, 600))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.gridLayout.setContentsMargins(0, 0, 0, 0)


        self.position_plot = pg.PlotWidget(self.gridLayoutWidget)
        self.position_plot.addLegend()

        self.pos1_curve = self.position_plot.plot(name='Left_Cam_Position', 
                                          pen = pg.mkPen(color=(255, 0, 0)))
        self.pos2_curve = self.position_plot.plot(name='Right_Cam_Position',
                                          pen = pg.mkPen(color=(0, 255, 0)))
        
        self.position_plot.setBackground('w')

        self.gridLayout.addWidget(self.position_plot, 0, 0, 1, 1)
        self.gridLayout.addLayout

        self.angle_plot = pg.PlotWidget(self.gridLayoutWidget)
        self.angle_plot.addLegend()
        
        self.angle1_curve = self.angle_plot.plot(name='Left_Cam_Angle', 
                                          pen = pg.mkPen(color=(255, 0, 0)))
        self.angle2_curve = self.angle_plot.plot(name='Right_Cam_Angle',
                                          pen = pg.mkPen(color=(0, 255, 0)))
        
        self.gridLayout.addWidget(self.angle_plot, 0, 1, 1, 1)

        self.LeftCamImg = pg.PlotWidget(self.gridLayoutWidget)
        self.LeftCamImg_back = pg.ImageItem()
        self.LeftCamImg.addItem(self.LeftCamImg_back)
        self.edgeup_1 = self.LeftCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 0)))
        self.edgedown_1 = self.LeftCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 0)))
        self.beam_1 = self.LeftCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 0)))
        self.center_1 = self.LeftCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 255)))
        self.beam_part_1 = self.LeftCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(0, 0, 255)))  
        self.gridLayout.addWidget(self.LeftCamImg, 1, 0, 1, 1)

        self.RightCamImg = pg.PlotWidget(self.gridLayoutWidget)
        self.RightCamImg_back = pg.ImageItem()
        self.RightCamImg.addItem(self.RightCamImg_back)
        self.edgeup_2 = self.RightCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 0)))
        self.edgedown_2 = self.RightCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 0)))
        self.beam_2 = self.RightCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 0)))
        self.center_2 = self.RightCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(255, 255, 255)))
        self.beam_part_2 = self.RightCamImg.plot(name='Line', 
                                          pen = pg.mkPen(color=(0, 0, 255)))   
        self.gridLayout.addWidget(self.RightCamImg, 1, 1, 1, 1)

#####################################################################################

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(250, 600, 200, 250))
        self.LeftCam_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.LeftCam_layout.setObjectName(u"LeftCam_layout")
        self.LeftCam_layout.setContentsMargins(0, 0, 0, 0)

        self.LeftCam_R_Button = QRadioButton(self.verticalLayoutWidget)
        self.LeftCam_R_Button.setObjectName(u"LeftCam_R_Button")
        self.LeftCam_R_Button.setChecked(True)
        self.LeftCam_R_Button.clicked.connect(self.LeftCam_Update_Channel)
        self.LeftCam_layout.addWidget(self.LeftCam_R_Button)

        self.LeftCam_G_Button = QRadioButton(self.verticalLayoutWidget)
        self.LeftCam_G_Button.setObjectName(u"LeftCam_G_Button")
        self.LeftCam_G_Button.clicked.connect(self.LeftCam_Update_Channel)
        self.LeftCam_layout.addWidget(self.LeftCam_G_Button)

        self.LeftCam_B_Button = QRadioButton(self.verticalLayoutWidget)
        self.LeftCam_B_Button.setObjectName(u"LeftCam_B_Button")
        self.LeftCam_B_Button.clicked.connect(self.LeftCam_Update_Channel)
        self.LeftCam_layout.addWidget(self.LeftCam_B_Button)

        self.LeftCam_Gray_Button = QRadioButton(self.verticalLayoutWidget)
        self.LeftCam_Gray_Button.setObjectName(u"LeftCam_Gray_Button")
        self.LeftCam_Gray_Button.clicked.connect(self.LeftCam_Update_Channel)
        self.LeftCam_layout.addWidget(self.LeftCam_Gray_Button)

        self.LeftCam_Update_Button = QPushButton(self.verticalLayoutWidget)
        self.LeftCam_Update_Button.setObjectName(u"LeftCam_Update_Button")
        self.LeftCam_Update_Button.clicked.connect(self.LeftCam_Update_Edges)
        self.LeftCam_layout.addWidget(self.LeftCam_Update_Button)

        self.LeftCam_layout_Horizontal = QHBoxLayout()
        self.LeftCam_layout_Horizontal.setObjectName(u"LeftCam_layout_Horizontal")
        self.LeftCamExpositionLabel = QLabel(self.verticalLayoutWidget)
        self.LeftCamExpositionLabel.setObjectName(u"label")

        self.LeftCam_layout_Horizontal.addWidget(self.LeftCamExpositionLabel)

        self.LeftCam_Exposition_Box = QSpinBox(self.verticalLayoutWidget)
        self.LeftCam_Exposition_Box.setObjectName(u"LeftCam_Exposition_Box")
        self.LeftCam_Exposition_Box.setMinimum(-9)
        self.LeftCam_Exposition_Box.setMaximum(0)
        self.LeftCam_Exposition_Box.valueChanged.connect(self.LeftCam_Exposition_Update)
        self.LeftCam_layout_Horizontal.addWidget(self.LeftCam_Exposition_Box)

        self.LeftCam_layout.addLayout(self.LeftCam_layout_Horizontal)

###########################################################################################

        self.LeftCam_layout_Horizontal_2 = QHBoxLayout()
        self.LeftCam_layout_Horizontal_2.setObjectName(u"LeftCam_layout_Horizontal")
        self.LeftCam_STDTresholdLabel = QLabel(self.verticalLayoutWidget)
        self.LeftCam_STDTresholdLabel.setObjectName(u"label")
        self.LeftCam_STDTresholdLabel.setText('Std Treshold')

        self.LeftCam_layout_Horizontal_2.addWidget(self.LeftCam_STDTresholdLabel)

        self.LeftCam_STDTresholdDoubleSpinBox = QDoubleSpinBox(self.verticalLayoutWidget)
        self.LeftCam_STDTresholdDoubleSpinBox.setObjectName(u"LeftCam_Exposition_Box")
        self.LeftCam_STDTresholdDoubleSpinBox.setMinimum(0)
        self.LeftCam_STDTresholdDoubleSpinBox.setMaximum(10)
        self.LeftCam_STDTresholdDoubleSpinBox.setValue(5)

        self.LeftCam_layout_Horizontal_2.addWidget(self.LeftCam_STDTresholdDoubleSpinBox)
        self.LeftCam_layout.addLayout(self.LeftCam_layout_Horizontal_2)

###########################################################################################



        self.Angle_State_label = QLabel(self.verticalLayoutWidget)
        self.Angle_State_label.setObjectName(u"Angle_State_label")
        self.LeftCam_layout.addWidget(self.Angle_State_label)

        self.LeftCam_SlopeDown_CheckBox = QCheckBox(self.verticalLayoutWidget)
        self.LeftCam_SlopeDown_CheckBox.setObjectName(u"LeftCam_SlopeDown_CheckBox")
        self.LeftCam_layout.addWidget(self.LeftCam_SlopeDown_CheckBox)
        

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(750, 600, 200, 250))
        self.RightCam_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.RightCam_layout.setObjectName(u"RightCam_layout")
        self.RightCam_layout.setContentsMargins(0, 0, 0, 0)

        self.RightCam_R_Button = QRadioButton(self.verticalLayoutWidget_2)
        self.RightCam_R_Button.setObjectName(u"RightCam_R_Button")
        self.RightCam_R_Button.setChecked(True)
        self.RightCam_R_Button.clicked.connect(self.RightCam_Update_Channel)
        self.RightCam_layout.addWidget(self.RightCam_R_Button)

        self.RightCam_G_Button = QRadioButton(self.verticalLayoutWidget_2)
        self.RightCam_G_Button.setObjectName(u"RightCam_G_Button")
        self.RightCam_G_Button.clicked.connect(self.RightCam_Update_Channel)
        self.RightCam_layout.addWidget(self.RightCam_G_Button)

        self.RightCam_B_Button = QRadioButton(self.verticalLayoutWidget_2)
        self.RightCam_B_Button.setObjectName(u"RightCam_B_Button")
        self.RightCam_B_Button.clicked.connect(self.RightCam_Update_Channel)
        self.RightCam_layout.addWidget(self.RightCam_B_Button)

        self.RightCam_Gray_Button = QRadioButton(self.verticalLayoutWidget_2)
        self.RightCam_Gray_Button.setObjectName(u"RightCam_Gray_Button")
        self.RightCam_Gray_Button.clicked.connect(self.RightCam_Update_Channel)
        self.RightCam_layout.addWidget(self.RightCam_Gray_Button)

        self.RightCam_Update_Button = QPushButton(self.verticalLayoutWidget_2)
        self.RightCam_Update_Button.setObjectName(u"RightCam_Update_Button")
        self.RightCam_Update_Button.clicked.connect(self.RightCam_Update_Edges)
        self.RightCam_layout.addWidget(self.RightCam_Update_Button)

        self.RightCam_layout_Horizontal = QHBoxLayout()
        self.RightCam_layout_Horizontal.setObjectName(u"RightCam_layout_Horizontal")
        self.RightCamExpositionLabel = QLabel(self.verticalLayoutWidget_2)
        self.RightCamExpositionLabel.setObjectName(u"label_2")

        self.RightCam_layout_Horizontal.addWidget(self.RightCamExpositionLabel)

        self.RightCam_Exposition_Box = QSpinBox(self.verticalLayoutWidget_2)
        self.RightCam_Exposition_Box.setObjectName(u"RightCam_Exposition_Box")
        self.RightCam_Exposition_Box.setMinimum(-9)
        self.RightCam_Exposition_Box.setMaximum(0)
        self.RightCam_Exposition_Box.valueChanged.connect(self.RightCam_Exposition_Update)
        self.RightCam_layout_Horizontal.addWidget(self.RightCam_Exposition_Box)
        self.RightCam_layout.addLayout(self.RightCam_layout_Horizontal)



        self.RightCam_layout_Horizontal_2 = QHBoxLayout()
        self.RightCam_layout_Horizontal_2.setObjectName(u"RightCam_layout_Horizontal")
        self.RightCam_STDTresholdLabel = QLabel(self.verticalLayoutWidget)
        self.RightCam_STDTresholdLabel.setObjectName(u"label")
        self.RightCam_STDTresholdLabel.setText('Std Treshold')

        self.RightCam_layout_Horizontal_2.addWidget(self.RightCam_STDTresholdLabel)

        self.RightCam_STDTresholdDoubleSpinBox = QDoubleSpinBox(self.verticalLayoutWidget)
        self.RightCam_STDTresholdDoubleSpinBox.setObjectName(u"RightCam_Exposition_Box")
        self.RightCam_STDTresholdDoubleSpinBox.setMinimum(0)
        self.RightCam_STDTresholdDoubleSpinBox.setMaximum(10)
        self.RightCam_STDTresholdDoubleSpinBox.setValue(5)
        self.RightCam_layout_Horizontal_2.addWidget(self.RightCam_STDTresholdDoubleSpinBox)
        self.RightCam_layout.addLayout(self.RightCam_layout_Horizontal_2)



        self.Pos_State_label = QLabel(self.verticalLayoutWidget_2)
        self.Pos_State_label.setObjectName(u"Pos_State_label")
        self.RightCam_layout.addWidget(self.Pos_State_label)

        self.RightCam_SlopeDown_CheckBox = QCheckBox(self.verticalLayoutWidget_2)
        self.RightCam_SlopeDown_CheckBox.setObjectName(u"checkBox")
        self.RightCam_layout.addWidget(self.RightCam_SlopeDown_CheckBox)

        
        
#####################################################################################

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 10, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)


        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.LeftCam.get_frame()
        imagedata = self.LeftCam.frame
        imagedata = cv2.cvtColor(imagedata, cv2.COLOR_BGR2RGB)
        imagedata = np.transpose(imagedata, [1,0,2])
        self.LeftCamImg_back.updateImage(cv2.blur(imagedata, [3,3]))

        self.LeftCam.beam_init(self.LeftCam.frame, channel=self.LeftCam_Channel)
        self.pos1_curve.setData(self.LeftCam.d_pos)
        self.angle1_curve.setData(self.LeftCam.d_ang)

        self.edgeup_1.setData(self.LeftCam.down_edge)
        self.edgedown_1.setData(self.LeftCam.up_edge)
        self.beam_1.setData(self.LeftCam.beam)
        self.center_1.setData(self.LeftCam.center)
        self.beam_part_1.setData(self.LeftCam.beam_part)

        self.RightCam.get_frame()
        imagedata = self.RightCam.frame
        imagedata = cv2.cvtColor(imagedata, cv2.COLOR_BGR2RGB)
        imagedata = np.transpose(imagedata, [1,0,2])
        self.RightCamImg_back.updateImage(cv2.blur(imagedata, [3,3]))

        self.RightCam.beam_init(self.RightCam.frame, channel=self.RightCam_Channel)
        self.pos2_curve.setData(self.RightCam.d_pos)
        self.angle2_curve.setData(self.RightCam.d_ang)

        self.edgeup_2.setData(self.RightCam.down_edge)
        self.edgedown_2.setData(self.RightCam.up_edge)
        self.beam_2.setData(self.RightCam.beam)
        self.center_2.setData(self.RightCam.center)
        self.beam_part_2.setData(self.RightCam.beam_part)


        self.Angle_State_label.setText('AngleLeft = ' + str(np.around(np.mean(self.LeftCam.d_ang[-20:]), 4)) + "±" + str(np.around(np.std(self.LeftCam.d_ang[-20:]), 4)) + '\n' 
                                + 'AngleRight = ' + str(np.around(np.mean(self.RightCam.d_ang[-20:]), 4)) + "±" + str(np.around(np.std(self.RightCam.d_ang[-20:]), 4)))
        
        self.Pos_State_label.setText('PosLeft = ' + str(np.around(np.mean(self.LeftCam.d_pos[-20:]), 4)) + "±" + str(np.around(np.std(self.LeftCam.d_pos[-20:]), 4)) + '\n' 
                                + 'PosRight = ' + str(np.around(np.mean(self.RightCam.d_pos[-20:]), 4)) + "±" + str(np.around(np.std(self.RightCam.d_pos[-20:]), 4)))
        None
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LeftCam_R_Button.setText(QCoreApplication.translate("MainWindow", u"R Channel", None))
        self.LeftCam_G_Button.setText(QCoreApplication.translate("MainWindow", u"G Channel", None))
        self.LeftCam_B_Button.setText(QCoreApplication.translate("MainWindow", u"B Channel", None))
        self.LeftCam_Gray_Button.setText(QCoreApplication.translate("MainWindow", u"GrayScale", None))
        self.LeftCam_Update_Button.setText(QCoreApplication.translate("MainWindow", u"Update Edges", None))
        self.LeftCamExpositionLabel.setText(QCoreApplication.translate("MainWindow", u"Exposition", None))
        self.LeftCam_SlopeDown_CheckBox.setText(QCoreApplication.translate("MainWindow", u"SlopedDown", None))
        self.RightCam_R_Button.setText(QCoreApplication.translate("MainWindow", u"R Channel", None))
        self.RightCam_G_Button.setText(QCoreApplication.translate("MainWindow", u"G Channel", None))
        self.RightCam_B_Button.setText(QCoreApplication.translate("MainWindow", u"B Channel", None))
        self.RightCam_Gray_Button.setText(QCoreApplication.translate("MainWindow", u"GrayScale", None))
        self.RightCam_Update_Button.setText(QCoreApplication.translate("MainWindow", u"Update Edges", None))
        self.RightCamExpositionLabel.setText(QCoreApplication.translate("MainWindow", u"Exposition", None))
        self.RightCam_SlopeDown_CheckBox.setText(QCoreApplication.translate("MainWindow", u"SlopedDown", None))
    # retranslateUi

