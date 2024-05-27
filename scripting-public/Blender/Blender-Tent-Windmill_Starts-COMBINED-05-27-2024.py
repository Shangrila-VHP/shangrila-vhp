#This script is two scripts combined into one. The first script creates a tent with a flap and a door. The second script creates a windmill with rotating blades. The windmill is protected by a cage-like mesh. The tent and windmill are created at different locations in the scene.
#I started this script with the intention of creating a better tent city, powered by clean energy. The windmill is a symbol of sustainability and self-sufficiency. The protective mesh around the windmill is a safety feature to prevent accidents (and not have birds and bats go into it also)

#Beginning of the original script for a better tent city powered by clean energy.
import bpy
import bmesh

#05-27-2024 around 0636 AM. Note: Having issues trying to load the Blender_Windmill_Starts.py by invoking the sys.path.append() function. Hence, commenting out these lines below for now.
#import sys
#sys.path.append('*UNC PATH REDACTED TO PROTECT PRIVACY AND PRACTICE SECURE CODING*')
#import Blender_Windmill_Starts
#This comment ends here.

from mathutils import Vector

def create_tent(name, location, size=2, flap_verts_count=3, door_verts_count=4, inset_thickness=0.1, inset_depth=0):
    # Create a new mesh object with a single vertex
    mesh = bpy.data.meshes.new(name + '_mesh')
    obj = bpy.data.objects.new(name, mesh)

    # Link the object to the scene
    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    # Set the object as the active object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Create a bmesh object and add a cube to it
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=size)
    # Move two of the top vertices to create the tent shape
    base_z_coords = []  # List to store the z-coordinates of the base vertices
    for v in bm.verts:
        if v.co.z > 0:
            if v.co.y > 0:
                v.co.y += 1
            else:
                v.co.y -= 1
        else:
            base_z_coords.append(v.co.z)  # Add the z-coordinate to the list

    # Calculate the average z-coordinate of the base vertices
    average_base_z = sum(base_z_coords) / len(base_z_coords)

    # Set the z-coordinate of all base vertices to the average
    for v in bm.verts:
        if v.co.z <= 0:
            v.co.z = average_base_z  # Make the base flat

    # Create a flap as a new face
    flap_verts = [v for v in bm.verts if v.co.z > 0]
    if len(flap_verts) >= flap_verts_count:
        flap_face = bm.faces.new(flap_verts)
    else:
        print("Not enough vertices to create a flap.")

    # Rotate the flap
    flap_edge = flap_face.edges[0]  # Use the first edge of the flap face
    bmesh.ops.rotate(bm, cent=flap_edge.verts[0].co, matrix=bpy.context.scene.cursor.matrix, verts=flap_verts)

    # Create a door as two new faces
    door_verts = [v for v in bm.verts if v.co.x > 0 and v.co.z < 1]
    if len(door_verts) >= door_verts_count:
        door_face = bm.faces.new(door_verts)
        bm.faces.remove(door_face)  # Remove the face to create an opening
    else:
        print("Not enough vertices to create a door.")

    # Create a rectangular door by moving some vertices upwards
    rectangular_door_verts = [v for v in bm.verts if v.co.x > 0 and v.co.z < 0.5]
    for v in rectangular_door_verts:
        v.co.z += 0.5

    # Update the mesh with the new data
    bm.to_mesh(mesh)
    bm.free()

    # Move the tent to the desired location
    obj.location = location

    # Create a new bmesh object
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Create an inset on each face of the tent
    faces = [f for f in bm.faces if f.normal.z > 0]  # Select the top faces
    bmesh.ops.inset_individual(bm, faces=faces, thickness=inset_thickness, depth=inset_depth)

    # Update the mesh with the new data
    bm.to_mesh(mesh)
    bm.free()

    return obj

# Create  five tents
tent1 = create_tent('Tent1', (-25, 0, 0), size=1, inset_thickness=0.2, inset_depth=0.2)
tent2 = create_tent('Tent2', bpy.context.scene.cursor.location + Vector((-5, 5, 0)))
tent3 = create_tent('Tent3', bpy.context.scene.cursor.location + Vector((-10, 5, 0)))
tent4 = create_tent('Tent4', bpy.context.scene.cursor.location + Vector((-15, 5, 0)))
tent5 = create_tent('Tent5', bpy.context.scene.cursor.location + Vector((-20, 5, 0)))

#End of the original script for a better tent city powered by clean energy.

#Copying the contents of the Blender_Windmill_Starts.py script here. At 05-27-2024 at 0640 AM.
# Let's try manually adding the code in here, for the windmill as importing it using the sys feature did not via previous attempts.

#I had to comment this bit out to get the tents to render.
# Clear all mesh objects
#bpy.ops.object.select_all(action='DESELECT')
#bpy.ops.object.select_by_type(type='MESH')
#bpy.ops.object.delete()

# Create the base of the windmill. 
bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=2, location=(0, 0, -3))
body = bpy.context.object

# Create a cube to represent the hollowed-out area
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.5))
cube = bpy.context.object

# Use the Boolean modifier to hollow out the body
body.modifiers.new(name="Hollow", type='BOOLEAN')
body.modifiers["Hollow"].operation = 'DIFFERENCE'
body.modifiers["Hollow"].object = cube
bpy.context.view_layer.objects.active = body
bpy.ops.object.modifier_apply(modifier="Hollow")

# Delete the cube
bpy.ops.object.select_all(action='DESELECT')
cube.select_set(True)
bpy.ops.object.delete()

# Create an empty object at the top of the body
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 2))
rotator = bpy.context.object
rotator.hide_viewport = True  # Hide the rotator in the viewport
rotator.hide_render = True  # Hide the rotator in the final render

# Create a cylinder to serve as the rod that is directly attached to the blade
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=17, location=(0, 0, 2.5))
rod = bpy.context.object
rod.parent = rotator

# Create a cylinder for the body of the windmill. This will go right above the base.
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, location=(0, 0, 2))

# Create an empty object at the top of the body to serve as the rotator
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 4))
rotator = bpy.context.object
rotator.hide_viewport = True  # Hide the rotator in the viewport
rotator.hide_render = True  # Hide the rotator in the final render

# Create four planes for the blades and parent them to the rotator
for i in range(4):
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 2 + i * 0.5))  # Adjust the Z location to be inside the cylinder
    blade = bpy.context.object
    blade.scale.x = 0.2  # Make the blades broad and thin
    blade.scale.y = 2
    blade.rotation_euler = (3.14159 / 2, 0, i * 3.14159 / 2)  # Rotate blades to be parallel to the Z-axis and evenly spaced around the rotator
    blade.parent = rotator

    # Convert the plane to a mesh and give it some thickness
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.1)})
    bpy.ops.object.mode_set(mode='OBJECT')

# New code
# Create four toruses for the curved blades and parent them to the rotator
for i in range(4):
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 2 + i * 0.5), rotation=(3.14159 / 2, 0, i * 3.14159 / 2))  # Adjust the Z location to be inside the cylinder and rotate the torus to be parallel to the Z-axis
    curved_blade = bpy.context.object
    curved_blade.scale.x = 1.2  # Make the curved blades broad and thin
    curved_blade.scale.y = 5
    curved_blade.scale.z = 0.2  # Make the curved blades flat
    # Existing code
    curved_blade.parent = rotator
    
     #05-25-2024: *This line hides the Mesh!* Edit back. 21:09 
    # Create a protective mesh around the windmill
    bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=10, location=(0, 0, 5))  # Adjust the depth to cover the whole windmill
    protective_mesh = bpy.context.object

    # 05-26-2024: *This line hides the Mesh!*
    # protective_mesh.hide_viewport = True
    # Kinda redundant?

    protective_mesh.scale.x = 1.3  # Make the protective mesh slightly larger than the windmill
    protective_mesh.scale.y = 1.3
    protective_mesh.scale.z = 1.83  # Stretch the protective mesh along the Z-axis
    
    # Convert the cylinder to a mesh and give it some thickness
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.1)})
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a wireframe modifier to make the protective mesh look like a cage
    wireframe_modifier = protective_mesh.modifiers.new(name="Wireframe", type='WIREFRAME')
    wireframe_modifier.thickness = 0.02  # Adjust the thickness of the wireframe
    wireframe_modifier.use_even_offset = True
    wireframe_modifier.use_relative_offset = False
    wireframe_modifier.use_boundary = True
    
    # Animate the rotator to rotate
    rotator.rotation_mode = 'QUATERNION'
    for i in range(250):  # for 250 frames
        rotator.rotation_euler = (0, 0, i * 3.14159 / 30)  # rotate 12 degrees per frame
        rotator.keyframe_insert(data_path="rotation_euler", frame=i, index=2)

# Animate the rotator to rotate
rotator.rotation_mode = 'XYZ'
for i in range(250):  # for 250 frames
    rotator.rotation_euler = (0, 0, i * 3.14159 / 30)  # rotate 12 degrees per frame
    rotator.keyframe_insert(data_path="rotation_euler", frame=i, index=2)
