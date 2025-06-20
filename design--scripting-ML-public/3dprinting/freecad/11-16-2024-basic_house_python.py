import FreeCAD, Part, Arch
from FreeCAD import Base

# Create a new document
doc = FreeCAD.newDocument("House")

# Define functions to create walls, doors, and windows
def makeWall(length, height, width, placement=None):
    wall = Arch.makeWall(length=length, height=height, width=width)
    if placement:
        wall.Placement = placement
    return wall

def makeDoor(width, height, placement=None):
    door = Arch.makeBuildingPart()
    door.Label = "Door"
    door.addObject(Arch.makeWall(length=width, height=height, width=100))
    if placement:
        door.Placement = placement
    return door

def makeWindow(width, height, placement=None):
    window = Arch.makeWindowPreset("Simple")
    window.Width = width
    window.Height = height
    if placement:
        window.Placement = placement
    return window

# Create the house walls
wall1 = makeWall(length=10000, height=3000, width=300)
wall2 = makeWall(length=10000, height=3000, width=300, placement=Base.Placement(Base.Vector(10000, 0, 0), Base.Rotation(Base.Vector(0, 0, 1), 90)))
wall3 = makeWall(length=10000, height=3000, width=300, placement=Base.Placement(Base.Vector(10000, 10000, 0), Base.Rotation(Base.Vector(0, 0, 1), 180)))
wall4 = makeWall(length=10000, height=3000, width=300, placement=Base.Placement(Base.Vector(0, 10000, 0), Base.Rotation(Base.Vector(0, 0, 1), 270)))

# Create the door
door = makeDoor(width=1000, height=2000, placement=Base.Placement(Base.Vector(5000, 0, 0), Base.Rotation(Base.Vector(0, 0, 1), 0)))

# Create the windows
window1 = makeWindow(width=1000, height=1500, placement=Base.Placement(Base.Vector(2000, 0, 1000), Base.Rotation(Base.Vector(0, 0, 1), 0)))
window2 = makeWindow(width=1000, height=1500, placement=Base.Placement(Base.Vector(8000, 0, 1000), Base.Rotation(Base.Vector(0, 0, 1), 0)))
window3 = makeWindow(width=1000, height=1500, placement=Base.Placement(Base.Vector(2000, 10000, 1000), Base.Rotation(Base.Vector(0, 0, 1), 180)))
window4 = makeWindow(width=1000, height=1500, placement=Base.Placement(Base.Vector(8000, 10000, 1000), Base.Rotation(Base.Vector(0, 0, 1), 180)))

# Create the roof
roof = Arch.makeRoof([wall1, wall2, wall3, wall4])

# Create the chimney
chimney = Part.makeBox(500, 500, 2000, Base.Vector(8000, 8000, 3000))
chimney_obj = doc.addObject("Part::Feature", "Chimney")
chimney_obj.Shape = chimney

# Apply red brick texture to the walls
brick_texture = FreeCAD.ActiveDocument.addObject("App::MaterialObject", "BrickTexture")
brick_texture.Material = {
    "Name": "Brick",
    "DiffuseColor": (0.8, 0.1, 0.1),
    "AmbientColor": (0.8, 0.1, 0.1),
    "SpecularColor": (0.5, 0.5, 0.5),
    "Shininess": 0.1,
    "Transparency": 0,
    "Reflectivity": 0.1
}
wall1.ViewObject.Material = brick_texture
wall2.ViewObject.Material = brick_texture
wall3.ViewObject.Material = brick_texture
wall4.ViewObject.Material = brick_texture

# Create the zen garden
def makeZenGarden():
    # Create the sand base
    sand_base = Part.makeBox(5000, 5000, 100, Base.Vector(12000, 0, 0))
    sand_base_obj = doc.addObject("Part::Feature", "SandBase")
    sand_base_obj.Shape = sand_base

    # Create rocks
    rock1 = Part.makeSphere(300, Base.Vector(13000, 1000, 100))
    rock1_obj = doc.addObject("Part::Feature", "Rock1")
    rock1_obj.Shape = rock1

    rock2 = Part.makeSphere(200, Base.Vector(14000, 3000, 100))
    rock2_obj = doc.addObject("Part::Feature", "Rock2")
    rock2_obj.Shape = rock2

    rock3 = Part.makeSphere(250, Base.Vector(13500, 4000, 100))
    rock3_obj = doc.addObject("Part::Feature", "Rock3")
    rock3_obj.Shape = rock3

    # Create a small tree
    tree_trunk = Part.makeCylinder(100, 1000, Base.Vector(15000, 2000, 100))
    tree_trunk_obj = doc.addObject("Part::Feature", "TreeTrunk")
    tree_trunk_obj.Shape = tree_trunk

    tree_foliage = Part.makeSphere(500, Base.Vector(15000, 2000, 1100))
    tree_foliage_obj = doc.addObject("Part::Feature", "TreeFoliage")
    tree_foliage_obj.Shape = tree_foliage

    return [sand_base_obj, rock1_obj, rock2_obj, rock3_obj, tree_trunk_obj, tree_foliage_obj]

zen_garden = makeZenGarden()

# Recompute the document to update the view
doc.recompute()
