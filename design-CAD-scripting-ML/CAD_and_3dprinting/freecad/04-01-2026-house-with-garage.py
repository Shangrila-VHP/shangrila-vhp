"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         House with Garage — Unified Hollow Interior (v1.1)                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Changes:                                                                    ║
║  - Unified House & Garage footprint (Hollow Interior)                        ║
║  - Added Floor Slab (for 3D Printing base)                                   ║
║  - Single 15° Slanted Roof across the entire structure                       ║
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
# Create Garage Rectangle (offset to the right)
r_garage = Draft.make_rectangle(length=GW, height=GL, placement=FreeCAD.Placement(FreeCAD.Vector(L/2 - 500, -GL/2, 0), FreeCAD.Rotation()))

# Merge them into one single hollow outline
merged_footprint = Draft.union([r_house, r_garage])
doc.recompute()

# ── WALLS & FLOOR ─────────────────────────────────────────────────────────────
# Create one unified wall object (removes the internal wall)
house_walls = Arch.makeWall(merged_footprint, width=WALL_THICKNESS, height=H)
house_walls.Label = "UnifiedWalls"

# Add Floor Slab (150mm thick base)
floor = Arch.makeStructure(merged_footprint)
floor.Height = 150
floor.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,-155), FreeCAD.Rotation())
floor.Label = "FloorSlab"

# ── UNIFIED SLANTED ROOF ──────────────────────────────────────────────────────
doc.recompute()
# Define a larger footprint for the entire roof
roof_rect = Draft.make_rectangle(length=L+GW+400, height=W+400, face=True, placement=FreeCAD.Placement(FreeCAD.Vector(-L/2-200, -W/2-200, H), FreeCAD.Rotation()))
doc.recompute()

# Create a single 15-degree roof slanted Right -> Left
roof = Arch.makeRoof(roof_rect)
roof.Angles = [89.0, 15.0, 89.0, 89.0] 
roof.Runs = [0.0, L + GW, 0.0, 0.0]
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
house_walls.Height = H + 3000
house_walls.Additions = house_walls.Additions + [roof]

# ── FINAL RECOMPUTE & VIEW FIT ───────────────────────────────────────────────
doc.recompute()
if FreeCAD.GuiUp:
    import FreeCADGui as Gui
    Gui.ActiveDocument.ActiveView.viewAxonometric()
    Gui.ActiveDocument.ActiveView.viewFit()

print("\n✅ Unified Hollow House generated in FreeCAD!")
print("   - Single shell interior (no internal wall).")
print("   - Solid floor slab added for 3D printing.\n")
