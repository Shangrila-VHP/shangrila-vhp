"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         House with Garage — FreeCAD BIM Python Script                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Version     : 1.01                                                         ║
║  Date        : 04-01-2026                                                   ║
║  Author      : Antigravity (Google DeepMind)                                ║
║  Requestor   : @genidma                                                     ║
║  Co-collaborator : @genidma                                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  HOW TO RUN IN FREECAD:                                                     ║
║  1. Open FreeCAD (1.1+ AppImage recommended)                                ║
║  2. Go to File -> Open and select this file.                                ║
║  3. Once open in the internal editor, press the green "Play" button (▶)     ║
║     in the top toolbar.                                                     ║
║  4. Switch to the 3D View to see your parametric house!                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  3D PRINTING NOTES:                                                         ║
║  - This script creates "Arch" objects which are true solids.                ║
║  - To export for 3D printing: Select the objects in the Tree View, then     ║
║    File -> Export -> STL (.stl).                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import FreeCAD, Draft, Arch, Part

# ── CREATE NEW DOCUMENT ──────────────────────────────────────────────────────
if FreeCAD.ActiveDocument:
    doc = FreeCAD.ActiveDocument
else:
    doc = FreeCAD.newDocument("HouseWithGarage")

# Clear existing objects if re-running
for obj in doc.Objects:
    doc.removeObject(obj.Name)

# ── DIMENSIONS (in mm) ───────────────────────────────────────────────────────
L, W, H = 9000, 7000, 3500  # Main House: 9m x 7m x 3.5m
GL, GW, GH = 5000, 6000, 2800 # Garage: 5m x 6m x 2.8m
WALL_THICKNESS = 200

# ── MAIN HOUSE WALLS ─────────────────────────────────────────────────────────
# Create the footprint rectangle
rect_house = Draft.make_rectangle(length=L, height=W, placement=FreeCAD.Placement(FreeCAD.Vector(-L/2, -W/2, 0), FreeCAD.Rotation()))
rect_house.Label = "HouseFootprint"

# Generate walls from the footprint (Arch Wall)
house_walls = Arch.makeWall(rect_house, width=WALL_THICKNESS, height=H)
house_walls.Label = "MainHouseWalls"

# ── GARAGE WALLS ─────────────────────────────────────────────────────────────
# Position garage to the right of the house
gx_offset = L/2 + GW/2 - 1000 # Slight overlap for a solid join
rect_garage = Draft.make_rectangle(length=GW, height=GL, placement=FreeCAD.Placement(FreeCAD.Vector(L/2 - 500, -GL/2, 0), FreeCAD.Rotation()))
rect_garage.Label = "GarageFootprint"

garage_walls = Arch.makeWall(rect_garage, width=WALL_THICKNESS, height=GH)
garage_walls.Label = "GarageWalls"

# ── ROOF ─────────────────────────────────────────────────────────────────────
# Force recompute so the geometry is ready for the roof tool
doc.recompute()

# House Roof Footprint
house_rect = Draft.make_rectangle(length=L+400, height=W+400, face=True, placement=FreeCAD.Placement(FreeCAD.Vector(-L/2-200, -W/2-200, H), FreeCAD.Rotation()))
doc.recompute()

# Create Roof object - Slanted from Right (15 deg) to Left
roof = Arch.makeRoof(house_rect)
# Edges: 0:Front, 1:Right, 2:Back, 3:Left
roof.Angles = [89.0, 15.0, 89.0, 89.0] 
roof.Runs = [0.0, L + 400, 0.0, 0.0]
roof.Thickness = [200.0, 200.0, 200.0, 200.0]
roof.Overhang = [400.0, 400.0, 400.0, 400.0]
roof.Label = "MainRoof"

# Garage Roof Footprint
garage_rect = Draft.make_rectangle(length=GW+400, height=GL+400, face=True, placement=FreeCAD.Placement(FreeCAD.Vector(L/2-700, -GL/2-200, GH), FreeCAD.Rotation()))
doc.recompute()

# Create Garage Roof - Slanted from Right to Left
g_roof = Arch.makeRoof(garage_rect)
g_roof.Angles = [89.0, 15.0, 89.0, 89.0]
g_roof.Runs = [0.0, GW + 400, 0.0, 0.0]
g_roof.Thickness = [150.0, 150.0, 150.0, 150.0]
g_roof.Overhang = [300.0, 300.0, 300.0, 300.0]
g_roof.Label = "GarageRoof"

# ── OPENINGS (Doors & Windows) ───────────────────────────────────────────────
# In Arch/BIM, we create a "Window" object and host it in a wall.
# For simplicity in this script, we'll create simple boxes that "subtract" from the wall.

def add_opening(parent_wall, x, y, z, w, h, d, label):
    box = doc.addObject("Part::Box", label)
    box.Length = w
    box.Width = d
    box.Height = h
    box.Placement = FreeCAD.Placement(FreeCAD.Vector(x - w/2, y - d/2, z), FreeCAD.Rotation())
    # Add the box to the wall as a subtraction (In v1.1 this is .Subtractions)
    parent_wall.Subtractions = parent_wall.Subtractions + [box]
    box.ViewObject.Visibility = False
    return box

# Front Door (House)
add_opening(house_walls, 0, -W/2, 0, 1000, 2100, 400, "FrontDoorOpening")

# Garage Door
add_opening(garage_walls, L/2 + GW/2 - 500, -GL/2, 0, 3500, 2200, 400, "GarageDoorOpening")

# Windows (House Front)
add_opening(house_walls, -2500, -W/2, 1200, 1500, 1200, 400, "Window_L")
add_opening(house_walls,  2500, -W/2, 1200, 1500, 1200, 400, "Window_R")

# ── FINAL RECOMPUTE & VIEW FIT ───────────────────────────────────────────────
doc.recompute()

# If running inside the FreeCAD GUI, zoom to fit the house
if FreeCAD.GuiUp:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewAxonometric()
    Gui.ActiveDocument.ActiveView.viewFit()

print("\n✅ FreeCAD House with Garage v1.01 generated!")
print("   - Objects are parametric Arch solids.")
print("   - Check the 3D view and Tree View.")
print("   - Ownership: Antigravity | Requestor: @genidma\n")
