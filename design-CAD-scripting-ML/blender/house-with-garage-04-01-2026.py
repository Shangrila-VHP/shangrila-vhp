"""
House with Garage and Front Lawn - Blender Python Script
Created: 04-01-2026
---------------------------------------------------------
HOW TO OPEN / RUN:
  1. Open Blender
  2. Go to the "Scripting" tab (top menu)
  3. Click "Open" and navigate to this file, OR
     paste this entire script into the text editor
  4. Click "Run Script" (the ▶ button, or Alt+P)
  5. The scene will be built automatically!
  6. Switch to the "3D Viewport" tab to see it
  7. To render: press F12 (or Render > Render Image)
     Output will be saved to: ./renders/house-with-garage-04-01-2026.png

SCENE CONTENTS:
  - Main house body with gabled roof
  - Attached garage with roof + garage door
  - Front door + windows
  - Chimney
  - Front lawn (grass)
  - Walkway + driveway (concrete)
  - 3 trees with trunks + leaf canopies
  - Sun + sky lighting
  - Camera already positioned for a nice angle
"""

import bpy
import math

# ── CLEAR SCENE ──────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)


# ── MATERIALS ─────────────────────────────────────────────────────────────────
def make_mat(name, r, g, b, roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat

M_WALL       = make_mat("Walls",       0.87, 0.80, 0.67)   # warm beige
M_ROOF       = make_mat("Roof",        0.42, 0.18, 0.08)   # terracotta
M_LAWN       = make_mat("Lawn",        0.12, 0.52, 0.09)   # grass green
M_CONCRETE   = make_mat("Concrete",    0.58, 0.58, 0.56)   # driveway / path
M_DOOR       = make_mat("Door",        0.28, 0.16, 0.06)   # dark walnut
M_GARAGE_DR  = make_mat("GarageDoor", 0.72, 0.72, 0.74)   # light silver
M_WINDOW     = make_mat("Window",      0.45, 0.70, 0.90, roughness=0.05)  # glass blue
M_CHIMNEY    = make_mat("Chimney",     0.55, 0.28, 0.17)   # brick red
M_TRIM       = make_mat("Trim",        0.96, 0.95, 0.92)   # near-white
M_TRUNK      = make_mat("Trunk",       0.28, 0.16, 0.07)   # tree trunk
M_LEAVES     = make_mat("Leaves",      0.09, 0.42, 0.07)   # tree canopy


# ── HELPERS ───────────────────────────────────────────────────────────────────
def assign_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def add_box(name, loc, dims, mat):
    """Create a box at loc=(x,y,z) with dims=(W,D,H)."""
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dims[0] / 2, dims[1] / 2, dims[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    assign_mat(obj, mat)
    return obj


def add_gabled_roof(name, cx, cy, base_z, W, D, H, mat):
    """
    Gabled roof centred at (cx, cy), bottom at base_z.
    Ridge runs along Y axis.  W=total width, D=total depth, H=ridge height.
    """
    hw, hd = W / 2, D / 2
    verts = [
        (-hw, -hd, 0),   # 0 front-left  base
        ( hw, -hd, 0),   # 1 front-right base
        ( hw,  hd, 0),   # 2 back-right  base
        (-hw,  hd, 0),   # 3 back-left   base
        (  0, -hd, H),   # 4 front ridge
        (  0,  hd, H),   # 5 back  ridge
    ]
    faces = [
        (0, 1, 4),        # front gable triangle
        (3, 2, 5),        # back  gable triangle
        (0, 4, 5, 3),     # left  slope
        (1, 2, 5, 4),     # right slope
    ]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = (cx, cy, base_z)
    bpy.context.collection.objects.link(obj)
    assign_mat(obj, mat)
    return obj


def add_sphere(name, loc, r, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=r, location=loc, segments=24, ring_count=14)
    obj = bpy.context.active_object
    obj.name = name
    assign_mat(obj, mat)
    return obj


def add_tree(name, x, y, trunk_h=1.8, canopy_r=1.3):
    add_box(f"{name}_trunk", (x, y, trunk_h / 2), (0.35, 0.35, trunk_h), M_TRUNK)
    add_sphere(f"{name}_canopy", (x, y, trunk_h + canopy_r * 0.75), canopy_r, M_LEAVES)


# ── GROUND / LAWN ─────────────────────────────────────────────────────────────
# Large flat grass plane in front of house
add_box("Lawn",     (0,  5, -0.05), (28, 22, 0.10), M_LAWN)
# Thin base under whole scene
add_box("Ground",   (2,  0, -0.15), (32, 32, 0.10), M_CONCRETE)


# ── DRIVEWAY ──────────────────────────────────────────────────────────────────
add_box("Driveway", (6,  -5, 0.01), (5.0, 12, 0.07), M_CONCRETE)

# ── WALKWAY (front path to main door) ─────────────────────────────────────────
add_box("Walkway",  (-1, -5, 0.01), (1.4,  6, 0.06), M_CONCRETE)


# ── MAIN HOUSE ────────────────────────────────────────────────────────────────
# Body: 9 m wide, 7 m deep, 4.5 m tall; centred at (-1, 0)
HX, HY, HW, HD, HH = -1.0, 0.0, 9.0, 7.0, 4.5
add_box("HouseBody", (HX, HY, HH / 2), (HW, HD, HH), M_WALL)

# Trim (fascia) around top edge
add_box("HouseTrim_front", (HX, HY - HD/2 - 0.05, HH + 0.12), (HW + 0.4, 0.15, 0.25), M_TRIM)
add_box("HouseTrim_back",  (HX, HY + HD/2 + 0.05, HH + 0.12), (HW + 0.4, 0.15, 0.25), M_TRIM)
add_box("HouseTrim_left",  (HX - HW/2 - 0.05, HY, HH + 0.12), (0.15, HD + 0.3, 0.25), M_TRIM)
add_box("HouseTrim_right", (HX + HW/2 + 0.05, HY, HH + 0.12), (0.15, HD + 0.3, 0.25), M_TRIM)

# Gabled roof over house
add_gabled_roof("HouseRoof", HX, HY, HH, HW + 0.5, HD + 0.5, 2.8, M_ROOF)

# Chimney (sits on roof)
add_box("Chimney", (HX - 2.0, HY + 1.0, HH + 1.8), (0.9, 0.9, 2.6), M_CHIMNEY)


# ── GARAGE ────────────────────────────────────────────────────────────────────
# Attached to right side of house; 5 m wide, 6 m deep, 3.2 m tall
GCX = HX + HW/2 + 2.5
GCY = -0.5
GW, GD, GH = 5.0, 6.0, 3.2
add_box("GarageBody", (GCX, GCY, GH / 2), (GW, GD, GH), M_WALL)
add_gabled_roof("GarageRoof", GCX, GCY, GH, GW + 0.4, GD + 0.4, 1.6, M_ROOF)

# Garage door (large panel, front face)
add_box("GarageDoor", (GCX, GCY - GD/2 - 0.05, 1.2), (3.8, 0.12, 2.3), M_GARAGE_DR)

# Garage side window
add_box("GarageWindow", (GCX, GCY - GD/2 - 0.05, GH - 0.8), (1.2, 0.12, 0.7), M_WINDOW)


# ── FRONT DOOR ────────────────────────────────────────────────────────────────
add_box("FrontDoor",   (HX,       HY - HD/2 - 0.06, 1.1), (1.1, 0.12, 2.1), M_DOOR)
# Door frame / lintel
add_box("DoorLintel",  (HX,       HY - HD/2 - 0.06, 2.4), (1.4, 0.12, 0.18), M_TRIM)
# Porch step
add_box("PorchStep",   (HX,       HY - HD/2 - 0.5,  0.1), (2.0, 0.8,  0.2),  M_CONCRETE)


# ── HOUSE WINDOWS ─────────────────────────────────────────────────────────────
# Front face (y = HY - HD/2)
fy = HY - HD/2 - 0.06
add_box("Win_front_L",  (HX - 2.8, fy, 2.4), (1.6, 0.12, 1.3), M_WINDOW)
add_box("Win_front_R",  (HX + 1.8, fy, 2.4), (1.6, 0.12, 1.3), M_WINDOW)

# Back face
by_ = HY + HD/2 + 0.06
add_box("Win_back_L",   (HX - 2.5, by_, 2.4), (1.6, 0.12, 1.3), M_WINDOW)
add_box("Win_back_R",   (HX + 1.5, by_, 2.4), (1.6, 0.12, 1.3), M_WINDOW)

# Left side
lx = HX - HW/2 - 0.06
add_box("Win_left",     (lx, HY,   2.4), (0.12, 1.4, 1.2), M_WINDOW)


# ── TREES ─────────────────────────────────────────────────────────────────────
add_tree("TreeFL",  -8.0,  2.0, trunk_h=2.0, canopy_r=1.4)   # front-left
add_tree("TreeFR",  -8.0, -2.0, trunk_h=1.8, canopy_r=1.3)   # front-left cluster
add_tree("TreeBR",   3.0,  7.0, trunk_h=2.5, canopy_r=1.6)   # back-right
add_tree("TreeS",  -10.0,  5.0, trunk_h=3.0, canopy_r=1.8)   # far left tall


# ── CAMERA ────────────────────────────────────────────────────────────────────
bpy.ops.object.camera_add(location=(22, -24, 14))
cam = bpy.context.active_object
cam.name = "MainCamera"
cam.rotation_euler = (
    math.radians(57),
    math.radians(0),
    math.radians(47),
)
bpy.context.scene.camera = cam


# ── LIGHTING ──────────────────────────────────────────────────────────────────
# Sun (key light)
bpy.ops.object.light_add(type='SUN', location=(15, -12, 25))
sun = bpy.context.active_object
sun.name = "Sun"
sun.rotation_euler = (math.radians(40), 0, math.radians(35))
sun.data.energy = 4.0
sun.data.angle  = math.radians(2)   # slightly soft sun disc

# Sky fill (large area light from above, cool blue)
bpy.ops.object.light_add(type='AREA', location=(0, 0, 20))
sky = bpy.context.active_object
sky.name = "SkyFill"
sky.data.energy = 300
sky.data.size   = 30
sky.data.color  = (0.55, 0.75, 1.0)

# Bounce fill from front-right
bpy.ops.object.light_add(type='AREA', location=(14, -14, 5))
bounce = bpy.context.active_object
bounce.name = "BounceFill"
bounce.data.energy = 120
bounce.data.size   = 10
bounce.data.color  = (1.0, 0.95, 0.85)


# ── WORLD / SKY ───────────────────────────────────────────────────────────────
world = bpy.data.worlds["World"]
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value    = (0.48, 0.70, 1.00, 1.0)
    bg_node.inputs["Strength"].default_value = 0.6


# ── RENDER SETTINGS ───────────────────────────────────────────────────────────
scene = bpy.context.scene
scene.render.engine          = 'CYCLES'
scene.cycles.samples         = 128
scene.render.resolution_x    = 1920
scene.render.resolution_y    = 1080
scene.render.filepath        = "//renders/house-with-garage-04-01-2026.png"
scene.render.image_settings.file_format = 'PNG'

# Optional: enable denoising for faster preview
scene.cycles.use_denoising = True

print("\n✅  Scene built successfully!")
print("   Switch to 3D Viewport to inspect.")
print("   Press F12 to render → saved to ./renders/house-with-garage-04-01-2026.png\n")
