import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa


lh_fname = 'all_ply/pial_Full/lh.pial.ply'
#rh_fname = 'all_ply/pial_Full/rh.pial.ply'

lhreader = vtk.vtkPLYReader()
lhreader.SetFileName(lh_fname)

#rhreader = vtk.vtkPLYReader()
#rhreader.SetFileName(rh_fname)

lhreader.Update()
#rhreader.Update()

lh_data = lhreader.GetOutput()
#rh_data = rhreader.GetOutput()

# points are (x, y, z)
lh_points = [lh_data.GetPoint(i) for i in range(lh_data.GetNumberOfPoints())]
#rh_points = [rh_data.GetPoint(i) for i in range(rh_data.GetNumberOfPoints())]

import pdb; pdb.set_trace()


chnradius = 3.0
chnheight = 12.0


ch1 = vtk.vtkConeSource()
ch1.SetResolution(60)
ch1.SetRadius(chnradius)
ch1.SetHeight(chnheight)
ch1.SetCenter(30., 20., 40.)  # TODO: more channels
ch1.SetDirection(0., 0., -1.)

mlh = vtk.vtkPolyDataMapper()
mlh.SetInputConnection(lhreader.GetOutputPort())

#mrh = vtk.vtkPolyDataMapper()
#mrh.SetInputConnection(rhreader.GetOutputPort())

mch1 = vtk.vtkPolyDataMapper()
mch1.SetInputConnection(ch1.GetOutputPort())

alh = vtk.vtkActor()
alh.SetMapper(mlh)
#alh.GetProperty().SetOpacity(0.6)

#arh = vtk.vtkActor()
#arh.SetMapper(mrh)
#arh.GetProperty().SetOpacity(0.65)

ach1 = vtk.vtkActor()
ach1.SetMapper(mch1)
ach1.GetProperty().SetDiffuseColor(0.333, 0.0, 0.0)

axes = vtk.vtkAxesActor()
a = vtk.vtkOrientationMarkerWidget()
a.SetOrientationMarker(axes)

ren = vtk.vtkRenderer()
ren.SetGradientBackground(True)
ren.AddActor(alh)
#ren.AddActor(arh)
ren.AddActor(ach1)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

a.SetInteractor(iren)
a.EnabledOn()
a.InteractiveOn()

ren.ResetCamera()
iren.Initialize()
renWin.Render()
iren.Start()
