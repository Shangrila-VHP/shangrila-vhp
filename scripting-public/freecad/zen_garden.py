import FreeCAD, Part
from FreeCAD import Base

# Create a new document
doc = FreeCAD.newDocument("ZenGarden")

# Create the sand base
sand_base = Part.makeBox(5000, 5000, 100, Base.Vector(0, 0, 0))
sand_base_obj = doc.addObject("Part::Feature", "SandBase")
sand_base_obj.Shape = sand_base

# Create rocks
rock1 = Part.makeSphere(300, Base.Vector(1000, 1000, 100))
rock1_obj = doc.addObject("Part::Feature", "Rock1")
rock1_obj.Shape = rock1

rock2 = Part.makeSphere(200, Base.Vector(3000, 3000, 100))
rock2_obj = doc.addObject("Part::Feature", "Rock2")
rock2_obj.Shape = rock2

rock3 = Part.makeSphere(250, Base.Vector(4000, 4000, 100))
rock3_obj = doc.addObject("Part::Feature", "Rock3")
rock3_obj.Shape = rock3

# Create a small tree
tree_trunk = Part.makeCylinder(100, 1000, Base.Vector(2000, 2000, 100))
tree_trunk_obj = doc.addObject("Part::Feature", "TreeTrunk")
tree_trunk_obj.Shape = tree_trunk

tree_foliage = Part.makeSphere(500, Base.Vector(2000, 2000, 1100))
tree_foliage_obj = doc.addObject("Part::Feature", "TreeFoliage")
tree_foliage_obj.Shape = tree_foliage

# Recompute the document to update the view
doc.recompute()
