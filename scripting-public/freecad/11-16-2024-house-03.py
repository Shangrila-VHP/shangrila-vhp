import FreeCAD as App
import Part

# Create a new FreeCAD document
doc = App.newDocument("House")

# Function to create and place a box
def create_box(length, width, height, x, y, z, name, color):
    box = doc.addObject("Part::Box", name)
    box.Length = length
    box.Width = width
    box.Height = height
    box.Placement.Base = App.Vector(x, y, z)
    box.ViewObject.ShapeColor = color
    return box

# Create the main house structure
house = create_box(20, 10, 10, 0, 0, 0, "House", (1.0, 0.2, 0.2))  # Red bricks

# Create the roof using a wedge (simpler for alignment)
roof = doc.addObject("Part::Wedge", "Roof")
roof.Length = 20
roof.Width = 10
roof.Height = 6
roof.Xmin = 0
roof.Xmax = 20
roof.Ymin = 0
roof.Ymax = 10
roof.Zmin = 10
roof.Zmax = 16
roof.Placement.Base = App.Vector(0, 0, 10)  # Position on top of the house
roof.ViewObject.ShapeColor = (0.4, 0.2, 0.0)  # Brown roof

# Create the door
door = create_box(2, 0.5, 4, 9, -0.5, 0, "Door", (0.6, 0.3, 0.0))  # Wood door

# Create windows
window1 = create_box(2, 0.5, 2, 3, -0.5, 5, "Window1", (0.7, 0.9, 1.0))  # Left window
window2 = create_box(2, 0.5, 2, 15, -0.5, 5, "Window2", (0.7, 0.9, 1.0))  # Right window

# Create the chimney
chimney = create_box(2, 2, 6, 16, 7, 10, "Chimney", (0.8, 0.1, 0.1))  # Red chimney

# Recompute the document to apply changes
doc.recompute()

print("House creation complete! Open in FreeCAD to view the model.")
