#!/usr/bin/env python
from __future__ import print_function
import vtk

# SOURCES
# https://www.evl.uic.edu/aspale/cs526/final/3-5-2-0.htm
# https://vtk.org/doc/nightly/html/classvtkMarchingCubes.html
# https://github.com/Beastmaster/itk-python-example/blob/master/vtkMarchingCubes.py
# https://www.evl.uic.edu/aspale/cs526/final/3-2-2-0.htm
# https://www.youtube.com/watch?v=0f3ZwnHvAK0
# https://kitware.github.io/vtk-examples/site/Python/

# Interactor style that handles mouse and keyboard events
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if (parent is not None):
            self.parent = parent
        self.AddObserver("KeyPressEvent", self.keyPress)

    def keyPress(self, obj, event):
        key = self.parent.GetKeySym()

        if (key == "Up"):
          # TODO: have this increase the isovalue
            isoValue = mc.GetValue(0)
            isoValue += 0.01
            mc.SetValue(0, isoValue)
            mc.Update()
            textActor.SetInput("Isovalue: %.2f" % isoValue)
            surfaceActor.GetProperty().SetColor(color_func.GetColor(isoValue))
            renwin.Render()
            print("Up")

        if (key == "Down"):
            # TODO: have this decrease the isovalue
            isoValue = mc.GetValue(0)
            isoValue -= 0.01
            mc.SetValue(0, isoValue)
            mc.Update()
            textActor.SetInput("Isovalue: %.2f" % isoValue)
            surfaceActor.GetProperty().SetColor(color_func.GetColor(isoValue))
            renwin.Render()
            print("Down")


# Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/hydrogen.vtk")
imageReader.Update()

# Print dimensions and range of the 3d image
dims = imageReader.GetOutput().GetDimensions()
print("Dimensions of image: " + str(dims[0]) + " x "
      + str(dims[1]) + " x " + str(dims[2]))
range = imageReader.GetOutput().GetScalarRange()
print("Range of image: " + str(range[0]) + " to " + str(range[1]))

# create an outline that shows the bounds of our dataset
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(imageReader.GetOutputPort())
# mapper to push the outline geometry to the graphics library
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
# actor for the outline to add to our renderer
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetLineWidth(2.0)

# TODO: Insert isosurfacing, scalebar, and text code here
mc = vtk.vtkMarchingCubes()
isoValue = 0.125
mc.SetInputConnection(imageReader.GetOutputPort())
mc.SetValue(0, isoValue)
mc.Update()

surfaceMapper = vtk.vtkPolyDataMapper()
surfaceMapper.SetInputConnection(mc.GetOutputPort())
surfaceMapper.ScalarVisibilityOff()

surfaceActor = vtk.vtkActor()
surfaceActor.SetMapper(surfaceMapper)
surfaceActor.GetProperty().SetColor(0, 1, 0)

textActor = vtk.vtkTextActor()
textActor.SetInput("Isovalue: %.2f" % isoValue)
textActor.GetTextProperty().SetFontSize(18)
textActor.GetTextProperty().SetColor(1, 1, 1)
textActor.SetPosition2(10, 40)

color_func = vtk.vtkColorTransferFunction()
color_func.AddRGBPoint(range[0], 0, 1, 0)
color_func.AddRGBPoint(range[1], 1, 1, 1)

scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(color_func)
scalar_bar.SetTitle("Function Value")
scalar_bar.SetNumberOfLabels(3)
scalar_bar.SetLabelFormat("%4.1f")

scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetPosition(0.1, 0.05)
scalar_bar.SetWidth(0.8)
scalar_bar.SetHeight(0.15)

renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)


# Add actors to our renderer
renderer.AddActor(outlineActor)
# TODO: You'll probably need to add additional actors to the scene
renderer.AddActor(surfaceActor)
renderer.AddActor2D(textActor)
renderer.AddActor(scalar_bar)


# The render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize(512, 512)
renwin.AddRenderer(renderer)

# Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent=interactor))
interactor.SetRenderWindow(renwin)
interactor.Initialize()
interactor.Start()