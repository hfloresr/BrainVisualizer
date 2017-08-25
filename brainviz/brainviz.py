#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout,
                             QSlider, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal

class UI(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(600, 600)
        self.centralWidget = QWidget(main_window)
        self.gridlayout = QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralWidget)

        sld = QSlider(Qt.Horizontal, main_window)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(1, 300)
        sld.setValue(1)
        sld.setGeometry(30, 40, 150, 30)



class SimpleView(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = UI()
        self.ui.setup_ui(self)
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        # Get source
        lh_fname = '../all_ply/pial_Full/lh.pial.ply'
        rh_fname = '../all_ply/pial_Full/rh.pial.ply'

        lhreader = vtk.vtkPLYReader()
        lhreader.SetFileName(lh_fname)

        rhreader = vtk.vtkPLYReader()
        rhreader.SetFileName(rh_fname)

        #lhreader.Update()
        #rhreader.Update()

        # Mapper
        lhmapper = vtk.vtkPolyDataMapper()
        lhmapper.SetInputConnection(lhreader.GetOutputPort())
        rhmapper = vtk.vtkPolyDataMapper()
        rhmapper.SetInputConnection(rhreader.GetOutputPort())

        # Actor
        lhactor = vtk.vtkActor()
        lhactor.SetMapper(lhmapper)
        rhactor = vtk.vtkActor()
        rhactor.SetMapper(rhmapper)

        self.ren.SetGradientBackground(True)
        self.ren.AddActor(lhactor)
        self.ren.AddActor(rhactor)

        # TODO: Fix Axes
        #axes = vtk.vtkAxesActor()
        #a = vtk.vtkOrientationMarkerWidget()
        #a.SetOrientationMarker(axes)
        #a.SetInteractor(self.iren)
        #a.EnabledOn()
        #a.InteractiveOn()
        #self.ren.ResetCamera()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleView()
    window.show()
    window.iren.Initialize()  # Need this line to show the render insie Qt
    sys.exit(app.exec_())
