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
    door = Arch.makeDoor(width=width, height=height)
    if placement:
        door.Placement = placement
    return door

def makeWindow(width, height, placement=None):
    window = Arch.makeWindow(width=width, height=height)
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
roof = Arch.makeRoof([wall1, wall2, wall3, wall4], height=2000)

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

# Recompute the document to update the view
doc.recompute()
