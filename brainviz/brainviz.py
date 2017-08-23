#!/usr/bin/env python3

import os
import numpy as np
import vtk

# Helper functions
def vtk_show(renderer, width=400, height=300):
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
    renderWindow.Render()

    win2imgfilter = vtk.vtkWindowToImageFilter()
    win2imgfilter.SetInput(renderWindow)
    win2imgfilter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputconnection(win2imgfilter.GetOutputPort())
    writer.Write()

    return writer.GetResult()

def createDummyRenderer():
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0)

    camera = renderer.MakeCamera()
    camera.SetPosition(-256, -256, 512)
    camera.SetFocalPoint(0.0, 0.0, 255.0)
    camera.SetViewAngle(30.0)
    camera.SetViewUp(0.46, -0.80, -0.38)
    renderer.SetActiveCamera(camera)

    return renderer


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
