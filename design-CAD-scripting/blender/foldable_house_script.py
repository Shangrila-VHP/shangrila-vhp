import bpy
import math
from mathutils import Vector

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ==================== PARAMETERS ====================
# House dimensions (Boxabl-like: 20ft x 20ft)
HOUSE_WIDTH = 20.0  # Blender units
HOUSE_DEPTH = 20.0
HOUSE_HEIGHT = 9.0   # Typical room height

# Wall thickness (realistic: 4-6 inches = 0.33-0.5 ft)
WALL_THICKNESS = 0.4

# Folding mechanism parameters
HINGE_RADIUS = 0.05
FOLDING_WALL_WIDTH = 8.0
FOLDING_WALL_HEIGHT = 7.0

# Modular connector parameters
CONNECTOR_LENGTH = 2.0
CONNECTOR_WIDTH = 1.0
CONNECTOR_HEIGHT = 1.0

# Number of modular sections (default 1, can be increased)
MODULAR_SECTIONS = 1

# ==================== MATERIAL DEFINITIONS ====================
MATERIAL_COLORS = {
    'Exterior': (0.8, 0.8, 0.8, 1.0),        # Light gray exterior
    'Interior': (0.95, 0.95, 0.95, 1.0),    # White interior
    'Roof': (0.4, 0.4, 0.4, 1.0),           # Dark gray roof
    'Floor': (0.7, 0.7, 0.7, 1.0),          # Concrete floor
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
    """Create a hollow wall box with thickness"""
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
            [0, 8, 12, 4],    # front-left connector
            [1, 9, 13, 5],    # front-right connector
            [2, 10, 14, 6],   # back-right connector
            [3, 11, 15, 7],   # back-left connector
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
    
    # Hinge at the connection point
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

def create_house():
    # List to store all house objects for grouping
    house_objects = []
    
    # Create floor (foundation)
    floor = create_wall_box(
        position=(HOUSE_WIDTH/2, HOUSE_DEPTH/2, 0.1),
        size=(HOUSE_WIDTH, HOUSE_DEPTH, 0.2),
        material_name='Floor'
    )
    house_objects.append(floor)
    
    # Create main structure (4 walls)
    wall_height_exterior = HOUSE_HEIGHT - 0.5  # For roof
    wall_z = wall_height_exterior / 2 + 0.1  # Sitting on floor
    
    # Front wall (facing +y)
    front_wall = create_wall_box(
        position=(HOUSE_WIDTH/2, HOUSE_DEPTH, wall_z),
        size=(HOUSE_WIDTH, WALL_THICKNESS, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(front_wall)
    
    # Back wall (facing -y)
    back_wall = create_wall_box(
        position=(HOUSE_WIDTH/2, 0, wall_z),
        size=(HOUSE_WIDTH, WALL_THICKNESS, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(back_wall)
    
    # Left wall (facing +x)
    left_wall = create_wall_box(
        position=(HOUSE_WIDTH, HOUSE_DEPTH/2, wall_z),
        size=(WALL_THICKNESS, HOUSE_DEPTH, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(left_wall)
    
    # Right wall (facing -x)
    right_wall = create_wall_box(
        position=(0, HOUSE_DEPTH/2, wall_z),
        size=(WALL_THICKNESS, HOUSE_DEPTH, wall_height_exterior),
        material_name='Exterior'
    )
    house_objects.append(right_wall)
    
    # Create folding walls (optional: for demo, create one on left side)
    folding_wall_left, hinge_left = create_folding_wall('left')
    house_objects.extend([folding_wall_left, hinge_left])
    folding_wall_right, hinge_right = create_folding_wall('right')
    house_objects.extend([folding_wall_right, hinge_right])
    
    # Create modular connectors (front and back)
    for side in ['front', 'back', 'left', 'right']:
        connector = create_modular_connector(side)
        house_objects.append(connector)
    
    # Create roof
    roof_thickness = 0.3
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
    house_objects.append(roof)
    
    # Apply roof material
    mat = create_material('Roof', MATERIAL_COLORS['Roof'])
    if roof.data.materials:
        roof.data.materials[0] = mat
    else:
        roof.data.materials.append(mat)
    
    # Create a collection for the house
    house_collection = bpy.data.collections.new(name="FoldableHouse")
    bpy.context.scene.collection.children.link(house_collection)
    
    # Add all house objects to the collection
    for obj in house_objects:
        house_collection.objects.link(obj)
    
    print("Modular, foldable house created successfully!")
    print("Features:")
    print("- Realistic wall thickness")
    print("- Folding side walls with hinges")
    print("- Modular connectors for expansion")
    print("- Proper roof structure")
    print("- Grouped for easy selection")
    
    print("Modular, foldable house created successfully!")
    print("Features:")
    print("- Realistic wall thickness")
    print("- Folding side walls with hinges")
    print("- Modular connectors for expansion")
    print("- Proper roof structure")
    print("- Grouped for easy selection")

# Run the house creation
create_house()

# Add lighting
bpy.ops.object.light_add(type='SUN', radius=1, location=(20, 20, 40))
light = bpy.context.object
light.data.energy = 2000

# Add some ambient light
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