# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QHBoxLayout,
                             QVBoxLayout, QLabel, QSlider, QMenuBar, QMenuBar,
                             QSplitter, QSpacerItem, QSizePolicy, QStatusBar)
from PyQt5.QtCore import Qt, QRect, QMetaObject

def _translate(context, text, disambig):
    return QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame = QFrame(self.splitter)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.epoch_slider= QSlider(self.frame)
        self.epoch_slider.setMinimum(1)
        self.epoch_slider.setMaximum(300)
        self.epoch_slider.setOrientation(Qt.Horizontal)
        self.epoch_slider.setObjectName("epoch_slider")
        self.verticalLayout.addWidget(self.epoch_slider)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.vector_size = QLabel(self.frame)
        self.vector_size.setFrameShape(QFrame.StyledPanel)
        self.vector_size.setFrameShadow(QFrame.Sunken)
        self.vector_size.setObjectName("vector_size")
        self.verticalLayout.addWidget(self.vector_size)
        self.vtk_panel = QFrame(self.splitter)
        self.vtk_panel.setFrameShape(QFrame.StyledPanel)
        self.vtk_panel.setFrameShadow(QFrame.Raised)
        self.vtk_panel.setObjectName("vtk_panel")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            _translate("MainWindow", "BrainViewer", None))
        self.label.setText(
            _translate("MainWindow", "Epoch", None))
        self.label_2.setText(
            _translate("MainWindow", "Vector Size:", None))
        self.vector_size.setText(
            _translate("MainWindow", "<No vector selected>", None))

