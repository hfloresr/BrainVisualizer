import vtk
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa


# VTK visualization pipeline
# Data Sources -> Data Filters -> Data Mappers -> Rendering


# Data sources
iD = vtk.vtkImageData()
dims = [31, 31, 31]  # dimension of cube
iD.SetSpacing(1., 1., 1.,)
iD.SetOrigin(0, 0, 0)
iD.SetDimensions(dims)

# Create a mesh of 31x31x31
xaxis = np.linspace(-.5, 1., dims[0])
yaxis = np.linspace(-1., 1., dims[1])
zaxis = np.linspace(-1., .5, dims[2])
[xc, yc, zc] = np.meshgrid(zaxis, yaxis, xaxis, indexing='ij')
data = np.sqrt(xc**2 + yc**2 + zc**2)

image = dsa.WrapDataObject(iD)
# Point data associates data to the vertices of the mesh
image.PointData.append(data.ravel(), 'scalar')  # linearize data

# Data Filters
contour = vtk.vtkContourFilter()  # Contour Filter
contour.SetInputData(iD)
contour.SetValue(0, 1.0)  # First threshold at idx 0 to 1.0
contour.SetInputArrayToProcess(0, 0, 0, 0, 'scalar')

#geom = vtk.vtkGeometryFilter()  # vtkAlgorithm
#geom.SetInputData(iD)  # data source -> filter

# Lookup table (purple to red)
lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(6)
lut.SetHueRange(0.6667, 0)
lut.SetSaturationRange(1, 1)
lut.SetValueRange(1, 1)
lut.SetTableRange(0.0, np.sqrt(3.))

# Data Mappers
m = vtk.vtkPolyDataMapper()
#m.SetInputConnection(geom.GetOutputPort())  # filter -> mapper
m.SetInputConnection(contour.GetOutputPort())
m.UseLookupTableScalarRangeOn()
m.SetLookupTable(lut)
m.SelectColorArray("scalar")  # color variable "scalars"
m.SetColorModeToMapScalars()
m.ScalarVisibilityOn()
m.SetScalarModeToUsePointFieldData()

# Actor (Graphics Object)
a = vtk.vtkActor()
a.SetMapper(m)
a.GetProperty().EdgeVisibilityOn()

# Rendering
ren = vtk.vtkRenderer()
ren.AddActor(a)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)  # add renderer to render window
renWin.SetSize(600, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()  # triggers execution
iren.Start()
