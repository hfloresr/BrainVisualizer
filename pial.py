import vtk
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa

lh_file = 'lh.pial.ply'
rh_file = 'rh.pial.ply'

r = vtk.vtkPLYReader()
r.SetFileName(lh_file)
r.Update()

r2 = vtk.vtkPLYReader()
r2.SetFileName(rh_file)
r2.Update()

m = vtk.vtkPolyDataMapper()
m.SetInputConnection(r.GetOutputPort())

m2 = vtk.vtkPolyDataMapper()
m2.SetInputConnection(r2.GetOutputPort())

a = vtk.vtkActor()
a.SetMapper(m)
a.GetProperty().EdgeVisibilityOn()

a2 = vtk.vtkActor()
a2.SetMapper(m2)
a2.GetProperty().EdgeVisibilityOn()

ren = vtk.vtkRenderer()
ren.AddActor(a)
ren.AddActor(a2)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
iren.Start()
