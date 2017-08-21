#!/usr/bin/env python3

import os
import numpy as np
import vtk

# Helper functions
def vtk_show(renderer, width=400, height=300):
    renderer_window = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(width, height)
    renderer_window.Render()

    win2imgfilter = vtk.vtkWindowToImageFilter()
    win2imgfilter.SetInput(renderer_window)
    win2imgfilter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputconnection(win2imgfilter.GetOutputPort())
    writer.Write()

    return writer.GetResult()

# path to the .mha file
fname_seg = '../nac_brain_atlas/brain_segmentation.mha'

reader = vtk.vtkMetaImageReader()
reader.SetFileName(fname_seg)

import pdb; pdb.set_trace()
cast_filter = vtk.vtkImageCast()
cast_filter.SetInputConnection(reader.GetOutputPort())
cast_filter.SetOutputScalarTypeToUnsignedShort()
cast_filter.Update()

imdata_brain = cast_filter.GetOutput()



x = 3
