'''

- This script was generated by Chatgpt. I provided subsequent prompts for additions and edits
- We have a basic house for a small family, some trees & a pool has been added later on

'''

import FreeCAD as App
import Part

# Create a new FreeCAD document
doc = App.newDocument("HouseWithPoolAndTrees")

# Function to create and place a box
def create_box(length, width, height, x, y, z, name, color):
    box = doc.addObject("Part::Box", name)
    box.Length = length
    box.Width = width
    box.Height = height
    box.Placement.Base = App.Vector(x, y, z)
    box.ViewObject.ShapeColor = color
    return box

# Function to create a cylinder (e.g., for tree trunks)
def create_cylinder(radius, height, x, y, z, name, color):
    cylinder = doc.addObject("Part::Cylinder", name)
    cylinder.Radius = radius
    cylinder.Height = height
    cylinder.Placement.Base = App.Vector(x, y, z)
    cylinder.ViewObject.ShapeColor = color
    return cylinder

# Create the main house structure
house = create_box(20, 10, 10, 0, 0, 0, "House", (1.0, 0.2, 0.2))  # Red bricks

# Create the roof, affixed to the house
roof = doc.addObject("Part::Wedge", "Roof")
roof.Length = 20
roof.Width = 10
roof.Height = 6
roof.Xmin = 0
roof.Xmax = 20
roof.Ymin = 0
roof.Ymax = 10
roof.Zmin = 0  # Bottom of the wedge starts from Z=0
roof.Zmax = 6  # Height of the wedge is 6
roof.Placement.Base = App.Vector(0, 0, 10)  # Base of the roof starts at the top of the house
roof.ViewObject.ShapeColor = (0.4, 0.2, 0.0)  # Brown roof

# Create the door (20% bigger)
door = create_box(2.4, 0.5, 4.8, 8.8, -0.5, 0, "Door", (0.6, 0.3, 0.0))  # Wood door

# Create windows (8% bigger)
window1 = create_box(2.16, 0.5, 2.16, 2.92, -0.5, 5, "Window1", (0.7, 0.9, 1.0))  # Left window
window2 = create_box(2.16, 0.5, 2.16, 14.92, -0.5, 5, "Window2", (0.7, 0.9, 1.0))  # Right window

# Create the chimney
chimney = create_box(2, 2, 6, 16, 7, 10, "Chimney", (0.8, 0.1, 0.1))  # Red chimney

# Add trees on either side of the house
tree_trunk_radius = 0.5
tree_trunk_height = 4
tree_foliage_radius = 2
tree_foliage_height = 3
tree_spacing = 6  # Increased spacing between trees
tree_positions = [i * tree_spacing for i in range(-4, -1)]  # Keep trees farther from the door

# Create trees on the left
for i, x in enumerate(tree_positions):
    trunk = create_cylinder(tree_trunk_radius, tree_trunk_height, x, -10, 0, f"TreeTrunkLeft{i+1}", (0.5, 0.25, 0.0))
    foliage = doc.addObject("Part::Sphere", f"TreeFoliageLeft{i+1}")
    foliage.Radius = tree_foliage_radius
    foliage.Placement.Base = App.Vector(x, -10, tree_trunk_height)  # On top of the trunk
    foliage.ViewObject.ShapeColor = (0.0, 0.5, 0.0)  # Green foliage

# Create trees on the right
for i, x in enumerate(tree_positions):
    trunk = create_cylinder(tree_trunk_radius, tree_trunk_height, x + 26, -10, 0, f"TreeTrunkRight{i+1}", (0.5, 0.25, 0.0))
    foliage = doc.addObject("Part::Sphere", f"TreeFoliageRight{i+1}")
    foliage.Radius = tree_foliage_radius
    foliage.Placement.Base = App.Vector(x + 26, -10, tree_trunk_height)  # On top of the trunk
    foliage.ViewObject.ShapeColor = (0.0, 0.5, 0.0)  # Green foliage

# Create a swimming pool on the left-hand side of the house
pool_length = 12
pool_width = 6
pool_depth = 2
pool_x = -16  # Position to the left of the house
pool_y = -3   # Centered along the y-axis with the house
pool_z = -pool_depth  # Sink the pool below ground level

# Add the pool to the scene
swimming_pool = create_box(pool_length, pool_width, pool_depth, pool_x, pool_y, pool_z, "SwimmingPool", (0.0, 0.5, 1.0))  # Blue water

# Recompute the document to apply changes
doc.recompute()

print("House with swimming pool and spaced trees creation complete! Open in FreeCAD to view the model.")

