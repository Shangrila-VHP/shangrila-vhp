"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         House with Garage — Unified Hollow Interior (v1.2)                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Changes:                                                                    ║
║  - Fixed "Vanishing Walls" by using Part.fuse for the footprint.             ║
║  - Improved Roof intersection logic.                                         ║
║  - Retained Floor Slab for 3D Printing.                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import FreeCAD, Draft, Arch, Part

# ── CREATE NEW DOCUMENT ──────────────────────────────────────────────────────
if FreeCAD.ActiveDocument:
    doc = FreeCAD.ActiveDocument
else:
    doc = FreeCAD.newDocument("HouseWithGarage")

for obj in doc.Objects:
    doc.removeObject(obj.Name)

# ── DIMENSIONS (in mm) ───────────────────────────────────────────────────────
L, W, H = 9000, 7000, 3500 
GL, GW, GH = 5000, 6000, 2800
WALL_THICKNESS = 200

# ── UNIFIED HOLLOW FOOTPRINT ─────────────────────────────────────────────────
# Create House Rectangle 
r_house = Draft.make_rectangle(length=L, height=W, placement=FreeCAD.Placement(FreeCAD.Vector(-L/2, -W/2, 0), FreeCAD.Rotation()))
# Create Garage Rectangle
r_garage = Draft.make_rectangle(length=GW, height=GL, placement=FreeCAD.Placement(FreeCAD.Vector(L/2 - 500, -GL/2, 0), FreeCAD.Rotation()))
doc.recompute()

# ROBust MERGE: Use Part.fuse to combine shapes, then get the outer wire
fused_shape = r_house.Shape.fuse(r_garage.Shape)
merged_wire = doc.addObject("Part::Feature", "FullFootprint")
merged_wire.Shape = fused_shape.removeSplitter().OuterWire
merged_wire.ViewObject.Visibility = False
doc.recompute()

# ── WALLS & FLOOR ─────────────────────────────────────────────────────────────
# Create one unified wall object from the merged outer wire
house_walls = Arch.makeWall(merged_wire, width=WALL_THICKNESS, height=H)
house_walls.Label = "UnifiedWalls"

# Add Floor Slab (150mm thick base)
floor = Arch.makeStructure(merged_wire)
floor.Height = 150
floor.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,-155), FreeCAD.Rotation())
floor.Label = "FloorSlab"

# ── UNIFIED SLANTED ROOF ──────────────────────────────────────────────────────
doc.recompute()
# Roof dimensions to cover the whole L-shape (from -L/2 to L/2+GW-500)
total_length = (L/2 + GW - 500) - (-L/2)
roof_rect = Draft.make_rectangle(length=total_length + 800, height=W + 800, face=True, 
                                 placement=FreeCAD.Placement(FreeCAD.Vector(-L/2 - 400, -W/2 - 400, H), FreeCAD.Rotation()))
doc.recompute()

# Create a single 15-degree roof slanted Right -> Left
roof = Arch.makeRoof(roof_rect)
roof.Angles = [89.0, 15.0, 89.0, 89.0] 
roof.Runs = [0.0, total_length + 800, 0.0, 0.0]
roof.Thickness = [200.0, 200.0, 200.0, 200.0]
roof.Overhang = [400.0, 400.0, 400.0, 400.0]
roof.Label = "MainRoof"

# ── OPENINGS (Doors & Windows) ───────────────────────────────────────────────
def add_opening(parent_wall, x, y, z, w, h, d, label):
    box = doc.addObject("Part::Box", label)
    box.Length, box.Width, box.Height = w, d, h
    box.Placement = FreeCAD.Placement(FreeCAD.Vector(x - w/2, y - d/2, z), FreeCAD.Rotation())
    parent_wall.Subtractions = parent_wall.Subtractions + [box]
    box.ViewObject.Visibility = False
    return box

# Front Door (House)
add_opening(house_walls, 0, -W/2, 0, 1000, 2100, 400, "FrontDoor")
# Garage Door
add_opening(house_walls, L/2 + GW/2 - 500, -GL/2, 0, 3500, 2200, 400, "GarageDoor")
# Windows 
add_opening(house_walls, -2500, -W/2, 1200, 1500, 1200, 400, "WindowL")
add_opening(house_walls,  2500, -W/2, 1200, 1500, 1200, 400, "WindowR")

# ── CONNECT WALLS TO ROOF ────────────────────────────────────────────────────
# Temporarily set walls very tall to ensure they intersect the roof
house_walls.Height = H + 3000
# Add the roof as an 'Addition' to trim the walls
house_walls.Additions = house_walls.Additions + [roof]

# ── FINAL RECOMPUTE & VIEW FIT ───────────────────────────────────────────────
doc.recompute()
if FreeCAD.GuiUp:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewAxonometric()
    Gui.ActiveDocument.ActiveView.viewFit()

print("\n✅ Unified Hollow House (v1.2) generated!")
print("   - Walls are back! Fixed via shape fusion.")
print("   - Interior is hollow and connected.")
