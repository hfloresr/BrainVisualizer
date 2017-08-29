#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np

import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.cm as cm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout,
                             QSlider, QHBoxLayout, QVBoxLayout, QFrame,
                             QMessageBox, QSizePolicy)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5 import QtCore

from lfpcluster import lfpcluster as lc
from scipy.io import loadmat


data = loadmat('../data/F141020-lfp-5min-1kHz.mat')
Z_pre = data['pre_pmcao']
Z_post = data['post_pmcao']

rate = 1000
num_epochs = 300
bad_channels = {5, 8, 10, 12, 16, 26}

pre_cluster = lc.LFPCluster(Z_pre, rate, bad_channels)
pre_cluster.standardize_lfp(num_epochs)

post_clust = lc.LFPCluster(Z_post, rate, bad_channels)
post_clust.standardize_post_lfp(num_epochs)

norm = mpl.colors.Normalize(vmin=0, vmax=4, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.hsv)



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

        resolution = 60
        radius = 2.0
        height = 12.0

        # Electrode placements
        channel_locs = [(-30, -80, 22),
                        (-10, -80, 25),
                        (10, -80, 25),
                        (30, -80, 22),
                        (-30, -60, 40), 
                        (-10, -60, 45),
                        (10, -60, 45),
                        (30, -60, 40),
                        (-30, -40, 48),
                        (-10, -40, 55),
                        (10, -40, 55),
                        (30, -40, 48),
                        (-30, -20, 50),
                        (-10, -20, 55),
                        (10, -20, 55),
                        (30, -20, 50),
                        (-30, 0, 45),
                        (-10, 0, 50),
                        (10, 0, 50),
                        (30, 0, 45),
                        (-30, 20, 38),
                        (-10, 20, 45),
                        (10, 20, 45),
                        (30, 20, 38),
                        (-30, 40, 20),
                        (-10, 40, 30),
                        (10, 40, 30),
                        (30, 40, 23),
                        (-30, 60, -5),
                        (-10, 60, 8),
                        (10, 60, 8),
                        (30, 60, -5)]

        channels = [vtk.vtkConeSource() for i in range(32)]
        for i, ch in enumerate(channels):
            ch.SetResolution(resolution)
            ch.SetRadius(radius)
            ch.SetHeight(height)
            x, y, z = channel_locs[i]
            ch.SetCenter(x, y, z)
            ch.SetDirection(0., 0., -1.)

        lh_reader.Update()
        rh_reader.Update()

        # Mapper
        lhmapper = vtk.vtkPolyDataMapper()
        lhmapper.SetInputConnection(lh_reader.GetOutputPort())
        rhmapper = vtk.vtkPolyDataMapper()
        rhmapper.SetInputConnection(rh_reader.GetOutputPort())

        chns_mapper = [vtk.vtkPolyDataMapper() for i in range(len(channels))]
        for ch, mapper in enumerate(chns_mapper):
            mapper.SetInputConnection(channels[ch].GetOutputPort())

        # Actor
        lhactor = vtk.vtkActor()
        lhactor.SetMapper(lhmapper)
        rhactor = vtk.vtkActor()
        rhactor.SetMapper(rhmapper)

        self.chns_actors = [vtk.vtkActor() for i in range(len(chns_mapper))]
        for mapper, actor in enumerate(self.chns_actors):
            actor.SetMapper(chns_mapper[mapper])
        self.init_clusters()

        ren.AddActor(lhactor)
        ren.AddActor(rhactor)
        for actor in self.chns_actors:
            ren.AddActor(actor)
        
        self.ren = ren
        self.interactor = interactor
        self.ren_window = ren_window

    def start(self):
        self.interactor.Initialize()
        self.interactor.Start()

    def init_clusters(self, epoch=1):
        Z_pre_clust, my_clusters = pre_cluster.get_clusters(k=4, epoch=epoch)
        my_colors = [(0,0,0,0) if c == 0 else mapper.to_rgba(c) for c in my_clusters]  
        for col, actor in enumerate(self.chns_actors):
            r, g, b, a = my_colors[col]
            actor.GetProperty().SetDiffuseColor(r, g, b)

    def set_color(self, epoch):
        self.init_clusters(epoch=epoch)
        self.ren_window.Render()
        

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

        self.ui.epoch_slider.setValue(1)
        self.ui.epoch_slider.valueChanged.connect(self.vtk_widget.set_color)

    def initialize(self):
        self.vtk_widget.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrainViewerApp('../all_ply/pial_Full')
    window.show()
    window.initialize()
    sys.exit(app.exec_())
