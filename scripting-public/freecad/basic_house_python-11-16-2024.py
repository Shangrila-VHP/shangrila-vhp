import FreeCAD, Part
from FreeCAD import Base

# Create a new cube with size 10
cube = Part.makeBox(20, 30, 25)

# Add it to the document
doc = FreeCAD.activeDocument()
part_obj = doc.addObject("Part::Feature", "Cube")
part_obj.Shape = cube

# Recompute the document to update the view
doc.recompute()
import FreeCAD, Part
from FreeCAD import Base

# Create a new cube with size 10
cube = Part.makeBox(15, 13, 18)

# Add it to the document
doc = FreeCAD.activeDocument()
part_obj = doc.addObject("Part::Feature", "Cube")
part_obj.Shape = cube

# Recompute the document to update the view
doc.recompute()