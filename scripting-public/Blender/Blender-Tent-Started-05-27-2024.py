import bpy
import bmesh
#mathutil needs to be imported in Blender's Python API
from mathutils import Vector

# Create a new mesh object with a single vertex
mesh = bpy.data.meshes.new('tent_mesh')
obj = bpy.data.objects.new('Tent', mesh)

# Link the object to the scene
scene = bpy.context.scene
scene.collection.objects.link(obj)

# Set the object as the active object
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Create a bmesh object and add a cube to it
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=2)

# Move two of the top vertices to create the tent shape
for v in bm.verts:
    if v.co.z > 0:
        if v.co.y > 0:
            v.co.y += 1
        else:
            v.co.y -= 1

# Create a flap as a new face
flap_verts = [v for v in bm.verts if v.co.z > 0]
if len(flap_verts) >= 3:
    flap_face = bm.faces.new(flap_verts)
else:
    print("Not enough vertices to create a flap.")

# Rotate the flap
flap_edge = flap_face.edges[0]  # Use the first edge of the flap face
bmesh.ops.rotate(bm, cent=flap_edge.verts[0].co, matrix=bpy.context.scene.cursor.matrix, verts=flap_verts)

# Create a door as two new faces
door_verts = [v for v in bm.verts if v.co.x > 0 and v.co.z < 1]
if len(door_verts) >= 4:
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
obj.location = bpy.context.scene.cursor.location

# Create a new bmesh object
bm = bmesh.new()
bm.from_mesh(mesh)

# Create an inset on each face of the tent
faces = [f for f in bm.faces if f.normal.z > 0]  # Select the top faces
bmesh.ops.inset_individual(bm, faces=faces, thickness=0.1, depth=0.1)

# Update the mesh with the new data
bm.to_mesh(mesh)
bm.free()

# Move the tent to the desired location
obj.location = bpy.context.scene.cursor.location

# Here is where you can place the code to duplicate the tent and create an opening
# Duplicate the tent
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.object.duplicate()

# Get the duplicated object
dup_obj = bpy.context.selected_objects[0]

# Set the location of the duplicated object
offset = Vector((5, 0, 0))  # Adjust the offset as needed
dup_obj.location = obj.location + offset

# Create a new bmesh object
bm = bmesh.new()
bm.from_mesh(dup_obj.data)

# Create a panel as a new face
panel_verts = [v for v in bm.verts if v.co.x > 0 and v.co.z < 1]
if len(panel_verts) >= 4:
    panel_face = bm.faces.new(panel_verts)
    bm.faces.remove(panel_face)  # Remove the face to create an opening
else:
    print("Not enough vertices to create a panel.")

# Update the mesh with the new data
bm.to_mesh(dup_obj.data)
bm.free()

# Continue with the rest of your code
# Create a new bmesh object
bm = bmesh.new()
bm.from_mesh(mesh)

# Create an inset on each face of the tent
faces = [f for f in bm.faces if f.normal.z > 0]  # Select the top faces
bmesh.ops.inset_individual(bm, faces=faces, thickness=0.1, depth=0.1)

# Update the mesh with the new data
bm.to_mesh(mesh)
bm.free()

# Create a cog
...
# Create a cog
cog_mesh = bpy.data.meshes.new('cog_mesh')
cog_obj = bpy.data.objects.new('Cog', cog_mesh)
scene.collection.objects.link(cog_obj)
bpy.context.view_layer.objects.active = cog_obj
cog_obj.select_set(True)
bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=0.1, radius2=0.1, depth=0.05)
bm.to_mesh(cog_mesh)
bm.free()
cog_obj.location = bpy.context.scene.cursor.location + Vector((1, 0, 0.5))  # Position the cog next to the door

# Create a wheel
wheel_mesh = bpy.data.meshes.new('wheel_mesh')
wheel_obj = bpy.data.objects.new('Wheel', wheel_mesh)
scene.collection.objects.link(wheel_obj)
bpy.context.view_layer.objects.active = wheel_obj
wheel_obj.select_set(True)
bm = bmesh.new()
bmesh.ops.create_circle(bm, cap_ends=True, cap_tris=False, segments=24, radius=0.3)
bm.to_mesh(wheel_mesh)
bm.free()
wheel_obj.location = bpy.context.scene.cursor.location + Vector((1.2, 0, 0.5))  # Position the wheel next to the cog

#Try and get the door to work

# Set the initial rotation of the cog and wheel
cog_obj.rotation_euler = (0, 0, 0)
wheel_obj.rotation_euler = (0, 0, 0)

# Set the initial location of the door
#Commenting this out (below) based on suggestion
#door_obj.location = (0, 0, 0)

# Insert keyframes for the initial state at frame 0
cog_obj.keyframe_insert(data_path="rotation_euler", frame=0)
wheel_obj.keyframe_insert(data_path="rotation_euler", frame=0)
#Commenting this out (below) based on suggestion
#door_obj.keyframe_insert(data_path="location", frame=0)

# Rotate the cog and wheel by 90 degrees over 100 frames
cog_obj.rotation_euler = (0, 0, 90)
wheel_obj.rotation_euler = (0, 0, 90)
cog_obj.keyframe_insert(data_path="rotation_euler", frame=100)
wheel_obj.keyframe_insert(data_path="rotation_euler", frame=100)

# Move the door up by 2 units over 100 frames
#Commenting this out (below) based on suggestion
#door_obj.location = (0, 0, 2)
#door_obj.keyframe_insert(data_path="location", frame=100)