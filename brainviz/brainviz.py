#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import numpy as np
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout,
                             QSlider, QHBoxLayout, QVBoxLayout, QFrame)
from PyQt5.QtCore import QObject, Qt, pyqtSignal


class QBrainViewer(QFrame):
    def __init__(self, parent, data_dir):
        super(QBrainViewer, self).__init__(parent)

        # Create QtWidget a child
        interactor = QVTKRenderWindowInteractor(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(interactor)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # Read data source
        lh_file = os.path.join(data_dir, 'lh.pial.ply')
        rh_file = os.path.join(data_dir, 'rh.pial.ply')
        lh_reader = vtk.vtkPLYReader()
        lh_reader.SetFileName(lh_file)
        rh_reader = vtk.vtkPLYReader()
        rh_reader.SetFileName(rh_file)

        # Setup VTK environment
        ren = vtk.vtkRenderer()
        ren_window = interactor.GetRenderWindow()
        ren_window.AddRenderer(ren)

        ren_window.SetInteractor(interactor)
        ren.SetGradientBackground(True)

        ch1 = vtk.vtkConeSource()
        ch1.SetResolution(60)
        ch1.SetRadius(2.0)
        ch1.SetHeight(12.0)
        ch1.SetCenter(30.0, 20.0, 40.0)
        ch1.SetDirection(0., 0., -1.)

        #lhreader.Update()
        #rhreader.Update()

        # Mapper
        lhmapper = vtk.vtkPolyDataMapper()
        lhmapper.SetInputConnection(lh_reader.GetOutputPort())
        rhmapper = vtk.vtkPolyDataMapper()
        rhmapper.SetInputConnection(rh_reader.GetOutputPort())
        ch1m = vtk.vtkPolyDataMapper()
        ch1m.SetInputConnection(ch1.GetOutputPort())

        # Actor
        lhactor = vtk.vtkActor()
        lhactor.SetMapper(lhmapper)
        rhactor = vtk.vtkActor()
        rhactor.SetMapper(rhmapper)
        ch1actor = vtk.vtkActor()
        ch1actor.SetMapper(ch1m)
        ch1actor.GetProperty().SetDiffuseColor(0.333, 0., 0.)

        ren.AddActor(lhactor)
        ren.AddActor(rhactor)
        ren.AddActor(ch1actor)

        self.ren = ren
        self.interactor = interactor

    def start(self):
        self.interactor.Initialize()
        self.interactor.Start()

    #def set_epoch(self, new_value):
    #    print(new_value)
    #    self.epoch.

class BrainViewerApp(QMainWindow):
    def __init__(self, data_dir):
        super(BrainViewerApp, self).__init__()
        self.vtk_widget = None
        self.ui = None
        self.setup(data_dir)

    def setup(self, data_dir):
        import brain_ui
        self.ui = brain_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.vtk_widget = QBrainViewer(self.ui.vtk_panel, data_dir)
        self.ui.vtk_layout = QHBoxLayout()
        self.ui.vtk_layout.addWidget(self.vtk_widget)
        self.ui.vtk_layout.setContentsMargins(0,0,0,0)
        self.ui.vtk_panel.setLayout(self.ui.vtk_layout)

        #self.ui.epoch_slider.setValue(1)
        #self.ui.epoch_slider.valueChanged.connect(self.vtk_widget.set_epoch)

    def initialize(self):
        self.vtk_widget.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrainViewerApp('../all_ply/pial_Full')
    window.show()
    window.initialize()
    sys.exit(app.exec_())
