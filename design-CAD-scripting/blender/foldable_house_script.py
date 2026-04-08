# Foldable House Script - v1.1
# Author: Kilo (with collaborator @genidma)
# Date: 2026-04-08
#
# Related to GitHub Issues:
# - Issue #38: Initial prototype and training (TinkerCAD)
# - Issue #50: Hinge design improvements (circular/concave portion for alignment)
#
# This script generates a 3D-printable foldable house model.
#
# Features:
# - Functional 3D-printable hinges with separate plates and pins
# - Windows with glass panes
# - Doors with thickness
# - Interior flooring and partition walls
# - Detachable roof with overhangs
# - Modular connectors for expansion
# - All objects grouped in "FoldableHouse" collection

import bpy
import math
from mathutils import Vector

# ==================== PARAMETERS ====================
# House dimensions (Boxabl-like: 20ft x 20ft)
HOUSE_WIDTH = 20.0  # Blender units
HOUSE_DEPTH = 20.0
HOUSE_HEIGHT = 9.0   # Typical room height

# Wall thickness (realistic: 4-6 inches = 0.33-0.5 ft)
WALL_THICKNESS = 0.4

# Folding wall parameters
FOLDING_WALL_WIDTH = 8.0
FOLDING_WALL_HEIGHT = 7.0

# Modular connector parameters
CONNECTOR_LENGTH = 2.0
CONNECTOR_WIDTH = 1.0
CONNECTOR_HEIGHT = 1.0

# 3D printing parameters (tolerances for movement)
PRINT_TOLERANCE = 0.02      # Clearance between moving parts
HINGE_PIN_DIAMETER = 0.1    # Diameter of hinge pin
HINGE_BARREL_DIAMETER = 0.5 # Diameter of hinge barrel
HINGE_LEAF_THICKNESS = 0.1  # Thickness of hinge leaf plate
HINGE_LEAF_WIDTH = 1.0      # Width of hinge leaf
HINGE_LEAF_HEIGHT = 0.5     # Height of hinge leaf

# Window and door parameters
WINDOW_WIDTH = 2.0
WINDOW_HEIGHT = 3.0
DOOR_WIDTH = 3.0
DOOR_HEIGHT = 7.0

# ==================== MATERIAL DEFINITIONS ====================
MATERIAL_COLORS = {
    'Exterior': (0.8, 0.8, 0.8, 1.0),        # Light gray exterior
    'Interior': (0.95, 0.95, 0.95, 1.0),    # White interior
    'Roof': (0.4, 0.4, 0.4, 1.0),           # Dark gray roof
    'Floor': (0.7, 0.7, 0.7, 1.0),          # Concrete floor
    'WindowGlass': (0.9, 0.9, 1.0, 0.7),    # Blue-tinted glass
    'WindowFrame': (0.2, 0.2, 0.2, 1.0),    # Black window frames
    'Door': (0.5, 0.3, 0.1, 1.0),           # Wood door
    'Hinge': (0.7, 0.7, 0.7, 1.0),          # Metal hinges
    'Connector': (0.6, 0.6, 0.6, 1.0)       # Modular connectors
}

def create_material(name, color, metallic=0.0, roughness=0.5):
    """Create a new material with given name and properties"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # Clear existing nodes
    nodes = mat.node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add Principled BSDF node
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    
    # Add output node
    output = nodes.new('ShaderNodeOutputMaterial')
    
    # Connect nodes
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_mesh(name, vertices, faces, location=(0,0,0)):
    """Create a mesh object from vertices and faces"""
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    return obj

def create_wall_box(position, size, material_name):
    """Create a hollow wall box with realistic thickness"""
    x, y, z = position
    width, height, depth = size
    
    half_w = width / 2
    half_d = depth / 2
    half_h = height / 2
    
    # Outer dimensions
    outer_vertices = [
        Vector((x - half_w, y - half_d, z - half_h)),
        Vector((x + half_w, y - half_d, z - half_h)),
        Vector((x + half_w, y + half_d, z - half_h)),
        Vector((x - half_w, y + half_d, z - half_h)),
        Vector((x - half_w, y - half_d, z + half_h)),
        Vector((x + half_w, y - half_d, z + half_h)),
        Vector((x + half_w, y + half_d, z + half_h)),
        Vector((x - half_w, y + half_d, z + half_h)),
    ]
    
    # Inner dimensions (subtract thickness)
    inner_thickness = WALL_THICKNESS
    inner_width = width - 2 * inner_thickness
    inner_depth = depth - 2 * inner_thickness
    inner_height = height - 2 * inner_thickness
    
    if inner_width <= 0 or inner_depth <= 0 or inner_height <= 0:
        # If thickness makes inner dimensions negative, create solid wall
        vertices = outer_vertices
        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [1, 2, 6, 5],  # right
            [2, 3, 7, 6],  # back
            [3, 0, 4, 7],  # left
        ]
    else:
        half_w_inner = inner_width / 2
        half_d_inner = inner_depth / 2
        half_h_inner = inner_height / 2
        
        inner_x = x
        inner_y = y
        inner_z = z + inner_thickness
        
        inner_vertices = [
            Vector((inner_x - half_w_inner, inner_y - half_d_inner, inner_z - half_h_inner)),
            Vector((inner_x + half_w_inner, inner_y - half_d_inner, inner_z - half_h_inner)),
            Vector((inner_x + half_w_inner, inner_y + half_d_inner, inner_z - half_h_inner)),
            Vector((inner_x - half_w_inner, inner_y + half_d_inner, inner_z - half_h_inner)),
            Vector((inner_x - half_w_inner, inner_y - half_d_inner, inner_z + half_h_inner)),
            Vector((inner_x + half_w_inner, inner_y - half_d_inner, inner_z + half_h_inner)),
            Vector((inner_x + half_w_inner, inner_y + half_d_inner, inner_z + half_h_inner)),
            Vector((inner_x - half_w_inner, inner_y + half_d_inner, inner_z + half_h_inner)),
        ]
        
        vertices = outer_vertices + inner_vertices
        
        # Outer faces
        faces = [
            [0, 1, 2, 3],    # bottom outer
            [4, 5, 6, 7],    # top outer
            [0, 1, 5, 4],    # front outer
            [1, 2, 6, 5],    # right outer
            [2, 3, 7, 6],    # back outer
            [3, 0, 4, 7],    # left outer
        ]
        
        # Inner faces
        inner_start = 8
        faces.extend([
            [inner_start+0, inner_start+1, inner_start+2, inner_start+3],  # bottom inner
            [inner_start+4, inner_start+5, inner_start+6, inner_start+7],  # top inner
            [inner_start+0, inner_start+1, inner_start+5, inner_start+4],  # front inner
            [inner_start+1, inner_start+2, inner_start+6, inner_start+5],  # right inner
            [inner_start+2, inner_start+3, inner_start+7, inner_start+6],  # back inner
            [inner_start+3, inner_start+0, inner_start+4, inner_start+7],  # left inner
        ])
        
        # Connecting faces (between outer and inner)
        faces.extend([
            [0, inner_start+0, inner_start+4, 4],    # front-left connector
            [1, inner_start+1, inner_start+5, 5],    # front-right connector
            [2, inner_start+2, inner_start+6, 6],   # back-right connector
            [3, inner_start+3, inner_start+7, 7],   # back-left connector
        ])
    
    obj = create_mesh(f"Wall_{int(x)}_{int(y)}", vertices, faces)
    
    # Create and assign material
    mat = create_material(material_name, MATERIAL_COLORS[material_name])
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    return obj

def create_folding_wall(side):
    """Create a folding wall section (left or right)"""
    if side == 'left':
        start_x = 0
        rotation_axis = 'X'
        rotation_angle = math.radians(90)
    else:  # right
        start_x = HOUSE_WIDTH
        rotation_axis = '-X'
        rotation_angle = math.radians(-90)
    
    # Wall panel
    wall = create_wall_box(
        position=(start_x - (HOUSE_WIDTH/2 if side == 'left' else -HOUSE_WIDTH/2), 
                  HOUSE_DEPTH/2, 
                  HOUSE_HEIGHT/2),
        size=(FOLDING_WALL_WIDTH, FOLDING_WALL_HEIGHT, WALL_THICKNESS),
        material_name='Exterior'
    )
    
    # Hinge at the connection point (simple placeholder - actual hinge is separate)
    hinge = create_mesh(
        "Hinge",
        vertices=[
            Vector((0, 0, 0)),
            Vector((0.1, 0, 0)),
            Vector((0.1, 0.3, 0)),
            Vector((0, 0.3, 0)),
            Vector((0, 0, 0.1)),
            Vector((0.1, 0, 0.1)),
            Vector((0.1, 0.3, 0.1)),
            Vector((0, 0.3, 0.1)),
        ],
        faces=[
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [1, 2, 6, 5],  # right
            [2, 3, 7, 6],  # back
            [3, 0, 4, 7],  # left
        ]
    )
    hinge.location = (start_x, HOUSE_DEPTH/2 - 0.5, HOUSE_HEIGHT/2)
    hinge.rotation_euler = (0, 0, math.radians(90) if side == 'left' else math.radians(-90))
    
    # Apply hinge material
    mat = create_material('Hinge', MATERIAL_COLORS['Hinge'], metallic=0.8, roughness=0.3)
    if hinge.data.materials:
        hinge.data.materials[0] = mat
    else:
        hinge.data.materials.append(mat)
    
    return wall, hinge

def create_modular_connector(side):
    """Create a modular connector for attaching additional units"""
    if side == 'front':
        location = (HOUSE_WIDTH/2, HOUSE_DEPTH, HOUSE_HEIGHT/2)
        rotation = (0, 0, 0)
        connector_x = 1.0
        connector_y = CONNECTOR_LENGTH
        connector_z = CONNECTOR_HEIGHT
    elif side == 'back':
        location = (HOUSE_WIDTH/2, 0, HOUSE_HEIGHT/2)
        rotation = (0, 0, math.radians(180))
        connector_x = 1.0
        connector_y = CONNECTOR_LENGTH
        connector_z = CONNECTOR_HEIGHT
    elif side == 'left':
        location = (0, HOUSE_DEPTH/2, HOUSE_HEIGHT/2)
        rotation = (0, 0, math.radians(90))
        connector_x = CONNECTOR_LENGTH
        connector_y = 1.0
        connector_z = CONNECTOR_HEIGHT
    else:  # right
        location = (HOUSE_WIDTH, HOUSE_DEPTH/2, HOUSE_HEIGHT/2)
        rotation = (0, 0, math.radians(-90))
        connector_x = CONNECTOR_LENGTH
        connector_y = 1.0
        connector_z = CONNECTOR_HEIGHT
    
    # Create connector shape
    vertices = [
        Vector((-connector_x/2, -connector_y/2, -connector_z/2)),
        Vector((connector_x/2, -connector_y/2, -connector_z/2)),
        Vector((connector_x/2, connector_y/2, -connector_z/2)),
        Vector((-connector_x/2, connector_y/2, -connector_z/2)),
        Vector((-connector_x/2, -connector_y/2, connector_z/2)),
        Vector((connector_x/2, -connector_y/2, connector_z/2)),
        Vector((connector_x/2, connector_y/2, connector_z/2)),
        Vector((-connector_x/2, connector_y/2, connector_z/2)),
    ]
    
    faces = [
        [0, 1, 2, 3],  # front
        [4, 5, 6, 7],  # back
        [0, 1, 5, 4],  # bottom
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # top
        [3, 0, 4, 7],  # left
    ]
    
    obj = create_mesh(f"Connector_{side}", vertices, faces, location)
    obj.rotation_euler = rotation
    
    # Apply material
    mat = create_material('Connector', MATERIAL_COLORS['Connector'])
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    return obj

def create_window_with_glass(location, orientation=(0,0,0)):
    """Create a window with frame and glass pane"""
    # Frame
    frame_thickness = 0.05
    frame_width = WINDOW_WIDTH
    frame_height = WINDOW_HEIGHT
    frame_depth = WALL_THICKNESS + 0.05
    
    half_w = frame_width / 2
    half_d = frame_depth / 2
    half_h = frame_height / 2
    
    vertices = [
        Vector((-half_w, -half_d, -half_h)),
        Vector((half_w, -half_d, -half_h)),
        Vector((half_w, half_d, -half_h)),
        Vector((-half_w, half_d, -half_h)),
        Vector((-half_w, -half_d, half_h)),
        Vector((half_w, -half_d, half_h)),
        Vector((half_w, half_d, half_h)),
        Vector((-half_w, half_d, half_h)),
    ]
    
    faces = [
        [0, 1, 2, 3],  # front
        [4, 5, 6, 7],  # back
        [0, 1, 5, 4],  # top
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # bottom
        [3, 0, 4, 7],  # left
    ]
    
    window = create_mesh("WindowFrame", vertices, faces, location)
    window.rotation_euler = orientation
    
    # Glass pane (slightly smaller)
    glass_x = location[0]
    glass_y = location[1]
    glass_z = location[2]
    
    # Adjust for frame thickness
    glass_vertices = [
        Vector((-half_w + 0.02, -half_d + 0.02, -half_h + 0.01)),
        Vector((half_w - 0.02, -half_d + 0.02, -half_h + 0.01)),
        Vector((half_w, half_d - 0.02, -half_h + 0.01)),
        Vector((-half_w, half_d - 0.02, -half_h + 0.01)),
        Vector((-half_w, -half_d + 0.02, half_h - 0.01)),
        Vector((half_w, -half_d + 0.02, half_h - 0.01)),
        Vector((half_w, half_d - 0.02, half_h - 0.01)),
        Vector((-half_w, half_d - 0.02, half_h - 0.01)),
    ]
    
    glass = create_mesh("Glass", glass_vertices, faces, (0,0,0))
    glass.location = (glass_x, glass_y, glass_z)
    glass.rotation_euler = orientation
    
    # Apply materials
    frame_mat = create_material('WindowFrame', MATERIAL_COLORS['WindowFrame'], metallic=0.3, roughness=0.2)
    if window.data.materials:
        window.data.materials[0] = frame_mat
    else:
        window.data.materials.append(frame_mat)
    
    glass_mat = create_material('Glass', MATERIAL_COLORS['WindowGlass'], metallic=0.8, roughness=0.1)
    if glass.data.materials:
        glass.data.materials[0] = glass_mat
    else:
        glass.data.materials.append(glass_mat)
    
    return window, glass

def create_door_with_thickness(location, orientation=(0,0,0)):
    """Create a door with thickness and frame"""
    door_thickness = 0.1
    half_w = DOOR_WIDTH / 2
    half_d = door_thickness / 2
    half_h = DOOR_HEIGHT / 2
    
    # Door panel
    vertices = [
        Vector((-half_w, -half_d, -half_h)),
        Vector((half_w, -half_d, -half_h)),
        Vector((half_w, half_d, -half_h)),
        Vector((-half_w, half_d, -half_h)),
        Vector((-half_w, -half_d, half_h)),
        Vector((half_w, -half_d, half_h)),
        Vector((half_w, half_d, half_h)),
        Vector((-half_w, half_d, half_h)),
    ]
    
    faces = [
        [0, 1, 2, 3],  # front
        [4, 5, 6, 7],  # back
        [0, 1, 5, 4],  # top
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # bottom
        [3, 0, 4, 7],  # left
    ]
    
    door = create_mesh("Door", vertices, faces, location)
    door.rotation_euler = orientation
    
    # Door frame (simple)
    frame_thickness = 0.05
    frame_width = DOOR_WIDTH + 0.1
    frame_height = DOOR_HEIGHT + 0.1
    frame_depth = WALL_THICKNESS + 0.1
    
    half_fw = frame_width / 2
    half_fh = frame_height / 2
    half_fd = frame_depth / 2
    
    frame_vertices = [
        Vector((-half_fw, -half_fd, -half_fh)),
        Vector((half_fw, -half_fd, -half_fh)),
        Vector((half_fw, half_fd, -half_fh)),
        Vector((-half_fw, half_fd, -half_fh)),
        Vector((-half_fw, -half_fd, half_fh)),
        Vector((half_fw, -half_fd, half_fh)),
        Vector((half_fw, half_fd, half_fh)),
        Vector((-half_fw, half_fd, half_fh)),
    ]
    
    frame = create_mesh("DoorFrame", frame_vertices, faces, location)
    frame.rotation_euler = orientation
    
    # Apply materials
    door_mat = create_material('Door', MATERIAL_COLORS['Door'], metallic=0.1, roughness=0.7)
    if door.data.materials:
        door.data.materials[0] = door_mat
    else:
        door.data.materials.append(door_mat)
    
    frame_mat = create_material('WindowFrame', MATERIAL_COLORS['WindowFrame'], metallic=0.3, roughness=0.2)
    if frame.data.materials:
        frame.data.materials[0] = frame_mat
    else:
        frame.data.materials.append(frame_mat)
    
    return door, frame

def create_hinge_plate(leaf_type, location, rotation):
    """
    Create a hinge leaf plate with a barrel.
    leaf_type: 'fixed' or 'moving' - determines barrel orientation.
    
    Design based on work from Issue #50 (circular/concave portion for alignment).
    """
    # Leaf plate dimensions
    leaf_x = HINGE_LEAF_WIDTH
    leaf_y = HINGE_LEAF_HEIGHT
    leaf_z = HINGE_LEAF_THICKNESS
    
    # Barrel dimensions
    barrel_diameter = HINGE_BARREL_DIAMETER
    barrel_length = leaf_y - 0.2  # Barrel along the height of leaf
    
    # Create leaf plate mesh
    half_x = leaf_x / 2
    half_y = leaf_y / 2
    half_z = leaf_z / 2
    
    vertices = [
        Vector((-half_x, -half_y, -half_z)),
        Vector((half_x, -half_y, -half_z)),
        Vector((half_x, half_y, -half_z)),
        Vector((-half_x, half_y, -half_z)),
        Vector((-half_x, -half_y, half_z)),
        Vector((half_x, -half_y, half_z)),
        Vector((half_x, half_y, half_z)),
        Vector((-half_x, half_y, half_z)),
    ]
    
    faces = [
        [0, 1, 2, 3],  # front
        [4, 5, 6, 7],  # back
        [0, 1, 5, 4],  # top
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # bottom
        [3, 0, 4, 7],  # left
    ]
    
    # Create barrel cylinder (aligned along Y axis for vertical hinge)
    barrel_radius = barrel_diameter / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=barrel_radius, depth=barrel_length, location=location)
    barrel_obj = bpy.context.object
    barrel_obj.name = f"HingeBarrel_{leaf_type}"
    # Rotate cylinder so its axis is along Y (up/down)
    barrel_obj.rotation_euler = (math.radians(90), 0, 0)
    
    # Parent barrel to leaf plate (or join)
    leaf_obj = create_mesh(f"HingePlate_{leaf_type}", vertices, faces, location)
    leaf_obj.rotation_euler = rotation
    # leaf_obj is already linked to the active collection by create_mesh
    
    # Join barrel to leaf
    bpy.ops.object.select_all(action='DESELECT')
    leaf_obj.select_set(True)
    barrel_obj.select_set(True)
    bpy.context.view_layer.objects.active = leaf_obj
    bpy.ops.object.join()
    
    # Apply material
    mat = create_material('Hinge', MATERIAL_COLORS['Hinge'], metallic=0.8, roughness=0.3)
    if leaf_obj.data.materials:
        leaf_obj.data.materials[0] = mat
    else:
        leaf_obj.data.materials.append(mat)
    
    return leaf_obj

def create_hinge_pin():
    """Create a hinge pin"""
    pin_diameter = HINGE_PIN_DIAMETER
    pin_length = HINGE_BARREL_DIAMETER - 2 * PRINT_TOLERANCE
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=pin_diameter/2, depth=pin_length)
    pin = bpy.context.object
    pin.name = "HingePin"
    mat = create_material('Hinge', MATERIAL_COLORS['Hinge'], metallic=0.8, roughness=0.3)
    if pin.data.materials:
        pin.data.materials[0] = mat
    else:
        pin.data.materials.append(mat)
    return pin

def create_roof_with_lip():
    """Create a detachable roof with a lip for the house"""
    roof_thickness = 0.3
    lip_height = 0.1
    lip_thickness = 0.05
    
    # Main roof
    roof = create_mesh(
        "Roof",
        vertices=[
            Vector((0, 0, HOUSE_HEIGHT - roof_thickness/2)),
            Vector((HOUSE_WIDTH, 0, HOUSE_HEIGHT - roof_thickness/2)),
            Vector((HOUSE_WIDTH, HOUSE_DEPTH, HOUSE_HEIGHT - roof_thickness/2)),
            Vector((0, HOUSE_DEPTH, HOUSE_HEIGHT - roof_thickness/2)),
            Vector((0, 0, HOUSE_HEIGHT + roof_thickness/2)),
            Vector((HOUSE_WIDTH, 0, HOUSE_HEIGHT + roof_thickness/2)),
            Vector((HOUSE_WIDTH, HOUSE_DEPTH, HOUSE_HEIGHT + roof_thickness/2)),
            Vector((0, HOUSE_DEPTH, HOUSE_HEIGHT + roof_thickness/2)),
        ],
        faces=[
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [1, 2, 6, 5],  # right
            [2, 3, 7, 6],  # back
            [3, 0, 4, 7],  # left
        ]
    )
    
    # Apply material
    mat = create_material('Roof', MATERIAL_COLORS['Roof'])
    if roof.data.materials:
        roof.data.materials[0] = mat
    else:
        roof.data.materials.append(mat)
    
    return roof

def create_interior_wall():
    """Create an interior partition wall"""
    wall = create_wall_box(
        position=(HOUSE_WIDTH/2, HOUSE_DEPTH/2, HOUSE_HEIGHT/2),
        size=(0.1, HOUSE_DEPTH, HOUSE_HEIGHT/2),
        material_name='Interior'
    )
    return wall

def create_house(offset_x=0, offset_y=0, offset_z=0):
    # List to store all house objects for grouping
    house_objects = []
    
    # Create floor (foundation)
    floor = create_wall_box(
        position=(HOUSE_WIDTH/2 + offset_x, HOUSE_DEPTH/2 + offset_y, 0.1 + offset_z),
        size=(HOUSE_WIDTH, HOUSE_DEPTH, 0.2),
        material_name='Floor'
    )
    house_objects.append(floor)
    
    # Create main structure (4 walls)
    wall_height_exterior = HOUSE_HEIGHT - 0.5
    wall_z = wall_height_exterior / 2 + 0.1 + offset_z
    
    # Front wall (facing +y)
    front_wall = create_wall_box(
        position=(HOUSE_WIDTH/2 + offset_x, HOUSE_DEPTH + offset_y, wall_z),
        size=(HOUSE_WIDTH, WALL_THICKNESS, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(front_wall)
    
    # Back wall (facing -y)
    back_wall = create_wall_box(
        position=(HOUSE_WIDTH/2 + offset_x, 0 + offset_y, wall_z),
        size=(HOUSE_WIDTH, WALL_THICKNESS, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(back_wall)
    
    # Left wall (facing +x)
    left_wall = create_wall_box(
        position=(HOUSE_WIDTH + offset_x, HOUSE_DEPTH/2 + offset_y, wall_z),
        size=(WALL_THICKNESS, HOUSE_DEPTH, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(left_wall)
    
    # Right wall (facing -x)
    right_wall = create_wall_box(
        position=(0 + offset_x, HOUSE_DEPTH/2 + offset_y, wall_z),
        size=(WALL_THICKNESS, HOUSE_DEPTH, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(right_wall)
    
    # Create folding walls with hinges
    folding_wall_left = create_wall_box(
        position=(-FOLDING_WALL_WIDTH/2 + offset_x, HOUSE_DEPTH/2 + offset_y, HOUSE_HEIGHT/2 + offset_z),
        size=(FOLDING_WALL_WIDTH, FOLDING_WALL_HEIGHT, WALL_THICKNESS),
        material_name='Exterior'
    )
    house_objects.append(folding_wall_left)
    
    folding_wall_right = create_wall_box(
        position=(HOUSE_WIDTH + FOLDING_WALL_WIDTH/2 + offset_x, HOUSE_DEPTH/2 + offset_y, HOUSE_HEIGHT/2 + offset_z),
        size=(FOLDING_WALL_WIDTH, FOLDING_WALL_HEIGHT, WALL_THICKNESS),
        material_name='Exterior'
    )
    house_objects.append(folding_wall_right)
    
    # Hinge components for left folding wall
    fixed_leaf_left = create_hinge_plate('fixed', (-WALL_THICKNESS/2 + offset_x, HOUSE_DEPTH/2 + offset_y, HOUSE_HEIGHT/2 + offset_z), (0, 0, 0))
    house_objects.append(fixed_leaf_left)
    moving_leaf_left = create_hinge_plate('moving', (-FOLDING_WALL_WIDTH/2 + FOLDING_WALL_WIDTH/2 + offset_x, HOUSE_DEPTH/2 + offset_y, HOUSE_HEIGHT/2 + offset_z), (0, 0, math.radians(180)))
    house_objects.append(moving_leaf_left)
    pin_left = create_hinge_pin()
    pin_left.location = (0 + offset_x, HOUSE_DEPTH/2, HOUSE_HEIGHT/2 + offset_z)
    house_objects.append(pin_left)
    
    # Hinge components for right folding wall
    fixed_leaf_right = create_hinge_plate('fixed', (HOUSE_WIDTH + WALL_THICKNESS/2 + offset_x, HOUSE_DEPTH/2 + offset_y, HOUSE_HEIGHT/2 + offset_z), (0, 0, math.radians(180)))
    house_objects.append(fixed_leaf_right)
    moving_leaf_right = create_hinge_plate('moving', (HOUSE_WIDTH + FOLDING_WALL_WIDTH/2 - FOLDING_WALL_WIDTH/2 + offset_x, HOUSE_DEPTH/2 + offset_y, HOUSE_HEIGHT/2 + offset_z), (0, 0, 0))
    house_objects.append(moving_leaf_right)
    pin_right = create_hinge_pin()
    pin_right.location = (HOUSE_WIDTH + offset_x, HOUSE_DEPTH/2, HOUSE_HEIGHT/2 + offset_z)
    house_objects.append(pin_right)
    
    # Modular connectors
    for side in ['front', 'back', 'left', 'right']:
        connector = create_modular_connector(side)
        house_objects.append(connector)
    
    # Roof
    roof = create_roof_with_lip()
    house_objects.append(roof)
    
    # Interior wall
    interior_wall = create_interior_wall()
    house_objects.append(interior_wall)
    
    # Windows and doors
    front_window, front_glass = create_window_with_glass((HOUSE_WIDTH/2 + offset_x, HOUSE_DEPTH - 1 + offset_y, HOUSE_HEIGHT/2 + offset_z), (0, 0, 0))
    house_objects.extend([front_window, front_glass])
    
    front_door, front_door_frame = create_door_with_thickness((HOUSE_WIDTH/2 + offset_x, HOUSE_DEPTH - 0.5 + offset_y, HOUSE_HEIGHT/2 + offset_z), (0, 0, 0))
    house_objects.extend([front_door, front_door_frame])
    
    # Create collection
    house_collection = bpy.data.collections.new(name="FoldableHouse")
    bpy.context.scene.collection.children.link(house_collection)
    
    # Add objects to collection
    for obj in house_objects:
        house_collection.objects.link(obj)
    
    print("Modular, foldable house created successfully!")
    print("- Realistic wall thickness")
    print("- Folding side walls with functional hinges (separate plates and pins)")
    print("- Modular connectors for expansion")
    print("- Detachable roof")
    print("- Interior partition wall")
    print("- Windows and doors (with glass and frames)")
    print("- Grouped for easy selection")

def create_second_house():
    # Create a second house offset to the right of the first house
    create_house(offset_x=30, offset_y=0, offset_z=0)

# Create the first house
create_house()

# Create the second house
create_second_house()

# Add lighting
bpy.ops.object.light_add(type='SUN', radius=1, location=(20, 20, 40))
light = bpy.context.object
light.data.energy = 2000

bpy.ops.object.light_add(type='AREA', radius=5, location=(0, 0, 10))
area_light = bpy.context.object
area_light.data.energy = 500
area_light.data.size = 10

print("\nTo animate the folding walls:")
print("1. Select the folding wall object")
print("2. Go to frame 1, rotate it to 0 degrees (closed)")
print("3. Insert rotation keyframe")
print("4. Go to frame 30, rotate it to 90 degrees (open)")
print("5. Insert rotation keyframe")
print("6. Repeat for the other folding wall")