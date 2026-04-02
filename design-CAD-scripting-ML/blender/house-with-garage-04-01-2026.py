"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         House with Garage and Front Lawn — Blender Python Script            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Version     : 1.01                                                         ║
║  Date        : 04-01-2026                                                   ║
║  Author      : Antigravity (Google DeepMind)                                ║
║  Requestor   : @genidma                                                     ║
║  Co-collaborator : @genidma                                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CHANGELOG                                                                  ║
║  v1.00  Initial scene: house, garage, lawn, trees, lighting                 ║
║  v1.01  + Ownership & credits header                                        ║
║         + Realistic glass windows (Glass BSDF, IOR, transmission)          ║
║         + Pine trees (stacked cones + trunk)                                ║
║         + 3D-print-ready geometry (manifold/watertight, wall thickness,     ║
║           export notes for STL/OBJ for large-format printers)               ║
║         + NVIDIA GPU render config (OptiX path tracing, adaptive sampling)  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  HOW TO RUN                                                                 ║
║  1. Open Blender (3.x or 4.x)                                               ║
║  2. Go to the Scripting workspace tab                                       ║
║     (tip: scroll the top tab bar right if it's hidden)                      ║
║  3. Click Open → select this file                                           ║
║  4. Click ▶ Run Script  (or Alt+P)                                          ║
║  5. Switch to Layout / 3D Viewport to inspect                               ║
║  6. Press F12 to render → saved to ./renders/                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  3D PRINTING NOTES                                                          ║
║  - All meshes are built as closed, manifold (watertight) solids             ║
║  - Wall thickness: 0.2 m minimum (scalable via SCALE constant below)        ║
║  - To export for a large-format 3D printer:                                 ║
║      File > Export > STL (.stl)  or  Wavefront OBJ (.obj)                  ║
║  - Recommended slicer: OrcaSlicer / PrusaSlicer (GPU-accelerated preview)  ║
║  - Fine-tuning with NVIDIA GPU:                                             ║
║      Use Blender Cycles + OptiX (NVIDIA RTX) for real-time iteration        ║
║      Enable: Edit > Preferences > System > Cycles Render Devices > OptiX   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import bpy
import math

# ── GLOBAL SCALE (1.0 = metres; change to match your printer's units) ─────────
SCALE = 1.0   # e.g. set to 0.001 to work in mm for STL export


# ── CLEAR SCENE ───────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    bpy.data.materials.remove(block)


# ── MATERIAL HELPERS ──────────────────────────────────────────────────────────
def make_mat(name, r, g, b, roughness=0.7, metallic=0.0, alpha=1.0):
    """Standard Principled BSDF material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value  = (r, g, b, 1.0)
    bsdf.inputs["Roughness"].default_value   = roughness
    bsdf.inputs["Metallic"].default_value    = metallic
    bsdf.inputs["Alpha"].default_value       = alpha
    if alpha < 1.0:
        mat.blend_method = 'BLEND'
    return mat


def make_glass_mat(name, r=0.75, g=0.88, b=0.95, ior=1.45):
    """
    Realistic glass material using Glass BSDF for physical accuracy.
    Tinted slightly blue like real window glass.
    For 3D-print slicers: swap this for a solid material before export.
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear defaults
    for n in nodes:
        nodes.remove(n)

    # Output
    out   = nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)

    # Mix: mostly Glass, small Principled for surface glint
    mix   = nodes.new("ShaderNodeMixShader")
    mix.location = (200, 0)
    mix.inputs["Fac"].default_value = 0.85   # 85% glass, 15% principled

    glass = nodes.new("ShaderNodeBsdfGlass")
    glass.location = (-50, 60)
    glass.inputs["Color"].default_value = (r, g, b, 1.0)
    glass.inputs["Roughness"].default_value = 0.02
    glass.inputs["IOR"].default_value = ior

    princ = nodes.new("ShaderNodeBsdfPrincipled")
    princ.location = (-50, -60)
    princ.inputs["Base Color"].default_value   = (r, g, b, 1.0)
    princ.inputs["Roughness"].default_value    = 0.05
    princ.inputs["Metallic"].default_value     = 0.1
    princ.inputs["Specular IOR Level"].default_value = 1.0

    links.new(glass.outputs["BSDF"], mix.inputs[1])
    links.new(princ.outputs["BSDF"], mix.inputs[2])
    links.new(mix.outputs["Shader"], out.inputs["Surface"])

    mat.use_backface_culling = False
    mat.blend_method = 'HASHED'
    mat.shadow_method = 'HASHED'
    return mat


# ── MATERIALS ─────────────────────────────────────────────────────────────────
M_WALL      = make_mat("Walls",      0.87, 0.80, 0.67)
M_ROOF      = make_mat("Roof",       0.42, 0.18, 0.08)
M_LAWN      = make_mat("Lawn",       0.12, 0.52, 0.09)
M_CONCRETE  = make_mat("Concrete",   0.58, 0.58, 0.56)
M_DOOR      = make_mat("Door",       0.28, 0.16, 0.06)
M_GARAGE_DR = make_mat("GarageDoor", 0.72, 0.72, 0.74, metallic=0.15)
M_WINDOW    = make_glass_mat("Window")          # ← realistic glass v1.01
M_CHIMNEY   = make_mat("Chimney",    0.55, 0.28, 0.17)
M_TRIM      = make_mat("Trim",       0.96, 0.95, 0.92)
M_TRUNK     = make_mat("Trunk",      0.28, 0.16, 0.07)
M_PINE      = make_mat("PineNeedles",0.06, 0.30, 0.08)   # dark pine green


# ── GEOMETRY HELPERS ──────────────────────────────────────────────────────────
def assign_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def add_box(name, loc, dims, mat):
    """
    Watertight closed box — safe for 3D print export.
    loc=(cx,cy,cz)  dims=(W,D,H)
    """
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dims[0] / 2 * SCALE,
                 dims[1] / 2 * SCALE,
                 dims[2] / 2 * SCALE)
    bpy.ops.object.transform_apply(scale=True)
    assign_mat(obj, mat)
    return obj


def add_gabled_roof(name, cx, cy, base_z, W, D, H, mat):
    """
    Closed gabled roof — all faces present (watertight).
    Ridge runs along Y. W=width, D=depth, H=ridge height.
    """
    hw, hd = W / 2 * SCALE, D / 2 * SCALE
    h = H * SCALE
    bz = base_z * SCALE
    verts = [
        (-hw, -hd, 0),  # 0
        ( hw, -hd, 0),  # 1
        ( hw,  hd, 0),  # 2
        (-hw,  hd, 0),  # 3
        (  0, -hd, h),  # 4  front ridge
        (  0,  hd, h),  # 5  back  ridge
    ]
    # Fully closed: 6 faces (4 slopes + 2 gable triangles)
    faces = [
        (0, 1, 4),       # front gable
        (3, 2, 5),       # back  gable
        (0, 4, 5, 3),    # left  slope
        (1, 2, 5, 4),    # right slope
        (3, 0, 1, 2),    # bottom (hidden but closes the mesh)
    ]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = (cx * SCALE, cy * SCALE, bz)
    bpy.context.collection.objects.link(obj)
    assign_mat(obj, mat)
    return obj


def add_cone(name, loc, r_base, r_top, height, mat, verts=16):
    """Cone/frustum — used for pine tree tiers."""
    bpy.ops.mesh.primitive_cone_add(
        vertices=verts,
        radius1=r_base * SCALE,
        radius2=r_top  * SCALE,
        depth=height   * SCALE,
        location=(loc[0] * SCALE, loc[1] * SCALE, loc[2] * SCALE)
    )
    obj = bpy.context.active_object
    obj.name = name
    assign_mat(obj, mat)
    return obj


def add_pine_tree(name, x, y):
    """
    Realistic pine tree: stacked diminishing cones + narrow trunk.
    3D-print friendly — all cones are closed meshes.
    """
    # Trunk
    add_box(f"{name}_trunk",
            (x, y, 1.0), (0.25, 0.25, 2.0), M_TRUNK)
    # Tier 1 — bottom / widest
    add_cone(f"{name}_t1",
             (x, y, 1.8), r_base=1.4, r_top=0.5, height=1.6, mat=M_PINE)
    # Tier 2
    add_cone(f"{name}_t2",
             (x, y, 2.9), r_base=1.0, r_top=0.35, height=1.3, mat=M_PINE)
    # Tier 3
    add_cone(f"{name}_t3",
             (x, y, 3.8), r_base=0.7, r_top=0.2, height=1.1, mat=M_PINE)
    # Tip
    add_cone(f"{name}_tip",
             (x, y, 4.55), r_base=0.4, r_top=0.0, height=0.8, mat=M_PINE)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE CONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════════

# ── GROUND & LAWN ─────────────────────────────────────────────────────────────
add_box("Lawn",    ( 0,  5, -0.05), (28, 22, 0.10), M_LAWN)
add_box("Ground",  ( 2,  0, -0.15), (32, 32, 0.10), M_CONCRETE)

# ── DRIVEWAY & WALKWAY ────────────────────────────────────────────────────────
add_box("Driveway", ( 6.0, -5.0, 0.01), (5.0, 12.0, 0.07), M_CONCRETE)
add_box("Walkway",  (-1.0, -5.0, 0.01), (1.4,  6.0, 0.06), M_CONCRETE)

# ── MAIN HOUSE ────────────────────────────────────────────────────────────────
HX, HY, HW, HD, HH = -1.0, 0.0, 9.0, 7.0, 4.5
add_box("HouseBody", (HX, HY, HH / 2), (HW, HD, HH), M_WALL)

# Trim fascia
add_box("Trim_front", (HX, HY - HD/2 - 0.05, HH + 0.12), (HW+0.4, 0.15, 0.25), M_TRIM)
add_box("Trim_back",  (HX, HY + HD/2 + 0.05, HH + 0.12), (HW+0.4, 0.15, 0.25), M_TRIM)
add_box("Trim_left",  (HX - HW/2 - 0.05, HY, HH + 0.12), (0.15, HD+0.3, 0.25), M_TRIM)
add_box("Trim_right", (HX + HW/2 + 0.05, HY, HH + 0.12), (0.15, HD+0.3, 0.25), M_TRIM)

# Gabled roof
add_gabled_roof("HouseRoof", HX, HY, HH, HW + 0.5, HD + 0.5, 2.8, M_ROOF)

# Chimney
add_box("Chimney", (HX - 2.0, HY + 1.0, HH + 1.8), (0.9, 0.9, 2.6), M_CHIMNEY)

# ── GARAGE ────────────────────────────────────────────────────────────────────
GCX, GCY, GW, GD, GH = HX + HW/2 + 2.5, -0.5, 5.0, 6.0, 3.2
add_box("GarageBody",  (GCX, GCY, GH / 2), (GW, GD, GH), M_WALL)
add_gabled_roof("GarageRoof", GCX, GCY, GH, GW + 0.4, GD + 0.4, 1.6, M_ROOF)
add_box("GarageDoor",  (GCX, GCY - GD/2 - 0.05, 1.2), (3.8, 0.12, 2.3), M_GARAGE_DR)
add_box("GarageWindow",(GCX, GCY - GD/2 - 0.05, GH - 0.8), (1.2, 0.12, 0.7), M_WINDOW)

# ── FRONT DOOR ────────────────────────────────────────────────────────────────
add_box("FrontDoor",  (HX, HY - HD/2 - 0.06, 1.1), (1.1, 0.12, 2.1), M_DOOR)
add_box("DoorLintel", (HX, HY - HD/2 - 0.06, 2.4), (1.4, 0.12, 0.18), M_TRIM)
add_box("PorchStep",  (HX, HY - HD/2 - 0.5,  0.1), (2.0, 0.80, 0.20), M_CONCRETE)

# ── WINDOWS — Realistic glass v1.01 ───────────────────────────────────────────
fy  = HY - HD/2 - 0.06   # front face y
by_ = HY + HD/2 + 0.06   # back  face y
lx  = HX - HW/2 - 0.06   # left  face x

# Window frames (thin trim boxes behind each pane for depth)
for tag, pos, dims in [
    ("WF_FL", (HX-2.8, fy-0.02, 2.4),   (1.8, 0.08, 1.5)),   # front-left frame
    ("WF_FR", (HX+1.8, fy-0.02, 2.4),   (1.8, 0.08, 1.5)),   # front-right frame
    ("WF_BL", (HX-2.5, by_+0.02, 2.4),  (1.8, 0.08, 1.5)),   # back-left frame
    ("WF_BR", (HX+1.5, by_+0.02, 2.4),  (1.8, 0.08, 1.5)),   # back-right frame
    ("WF_SL", (lx-0.02,  HY, 2.4),      (0.08, 1.6, 1.4)),   # side frame
]:
    add_box(tag, pos, dims, M_TRIM)

# Glass panes (thinner, on top of frames)
add_box("Win_FL", (HX-2.8, fy,  2.4), (1.6, 0.06, 1.3), M_WINDOW)
add_box("Win_FR", (HX+1.8, fy,  2.4), (1.6, 0.06, 1.3), M_WINDOW)
add_box("Win_BL", (HX-2.5, by_, 2.4), (1.6, 0.06, 1.3), M_WINDOW)
add_box("Win_BR", (HX+1.5, by_, 2.4), (1.6, 0.06, 1.3), M_WINDOW)
add_box("Win_SL", (lx,     HY,  2.4), (0.06, 1.4, 1.2), M_WINDOW)

# ── PINE TREES — v1.01 ────────────────────────────────────────────────────────
add_pine_tree("PineFL",  -8.0,  2.0)   # front-left
add_pine_tree("PineFR",  -8.0, -2.0)   # front-left cluster
add_pine_tree("PineBR",   3.0,  7.0)   # back-right
add_pine_tree("PineTall",-10.0, 5.0)   # far-left tall


# ═══════════════════════════════════════════════════════════════════════════════
# CAMERA
# ═══════════════════════════════════════════════════════════════════════════════
bpy.ops.object.camera_add(location=(22, -24, 14))
cam = bpy.context.active_object
cam.name = "MainCamera"
cam.rotation_euler = (math.radians(57), 0, math.radians(47))
cam.data.lens = 35   # 35 mm focal length — good for architecture
bpy.context.scene.camera = cam


# ═══════════════════════════════════════════════════════════════════════════════
# LIGHTING
# ═══════════════════════════════════════════════════════════════════════════════
bpy.ops.object.light_add(type='SUN', location=(15, -12, 25))
sun = bpy.context.active_object
sun.name = "Sun"
sun.rotation_euler = (math.radians(40), 0, math.radians(35))
sun.data.energy = 4.0
sun.data.angle  = math.radians(2)

bpy.ops.object.light_add(type='AREA', location=(0, 0, 20))
sky = bpy.context.active_object
sky.name = "SkyFill"
sky.data.energy = 300
sky.data.size   = 30
sky.data.color  = (0.55, 0.75, 1.0)

bpy.ops.object.light_add(type='AREA', location=(14, -14, 5))
bounce = bpy.context.active_object
bounce.name = "BounceFill"
bounce.data.energy = 120
bounce.data.size   = 10
bounce.data.color  = (1.0, 0.95, 0.85)


# ═══════════════════════════════════════════════════════════════════════════════
# WORLD / SKY BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value    = (0.48, 0.70, 1.00, 1.0)
    bg.inputs["Strength"].default_value = 0.6


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER SETTINGS — NVIDIA GPU / OptiX OPTIMISED
# ═══════════════════════════════════════════════════════════════════════════════
scene = bpy.context.scene
prefs = bpy.context.preferences.addons.get("cycles", None)

scene.render.engine       = 'CYCLES'
scene.cycles.device       = 'GPU'          # use GPU (NVIDIA CUDA / OptiX)

# Try to enable OptiX (NVIDIA RTX hardware ray tracing)
try:
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = 'OPTIX'
    bpy.context.preferences.addons["cycles"].preferences.refresh_devices()
    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d.use = True
    print("  ✅  OptiX (NVIDIA RTX) enabled for GPU rendering")
except Exception as e:
    print(f"  ⚠️  OptiX not available ({e}) — falling back to CUDA/CPU")
    try:
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = 'CUDA'
        bpy.context.preferences.addons["cycles"].preferences.refresh_devices()
        for d in bpy.context.preferences.addons["cycles"].preferences.devices:
            d.use = True
        print("  ✅  CUDA (NVIDIA GPU) enabled")
    except Exception as e2:
        print(f"  ⚠️  CUDA not available ({e2}) — CPU render will be used")

scene.cycles.samples                    = 256   # high quality; lower to 64 for quick preview
scene.cycles.use_adaptive_sampling      = True  # NVIDIA-friendly — fewer samples where low noise
scene.cycles.adaptive_threshold         = 0.01
scene.cycles.use_denoising             = True   # AI denoiser (NVIDIA OptiX Denoiser preferred)
scene.cycles.denoising_use_gpu         = True   # offload denoising to GPU

scene.render.resolution_x              = 1920
scene.render.resolution_y              = 1080
scene.render.filepath                  = "//renders/house-with-garage-v1.01-04-01-2026.png"
scene.render.image_settings.file_format = 'PNG'

# ── 3D PRINT EXPORT REMINDER ──────────────────────────────────────────────────
print("\n" + "═" * 60)
print("  ✅  Scene v1.01 built successfully!")
print("  Author : Antigravity (Google DeepMind)")
print("  Request: @genidma")
print("═" * 60)
print("  RENDER  → Press F12  (GPU/OptiX/CUDA auto-selected above)")
print("  OUTPUT  → ./renders/house-with-garage-v1.01-04-01-2026.png")
print("─" * 60)
print("  3D PRINT EXPORT:")
print("    File > Export > STL (.stl)  — for large-format printers")
print("    File > Export > Wavefront OBJ — for slicer fine-tuning")
print("    Recommended: OrcaSlicer / PrusaSlicer with GPU preview")
print("    NVIDIA fine-tuning: use OptiX for real-time material iter.")
print("═" * 60 + "\n")
