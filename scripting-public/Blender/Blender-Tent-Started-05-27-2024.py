import bpy
import bmesh

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
door_verts_left = [v for v in bm.verts if v.co.x > 0 and v.co.z < 1 and v.co.y < 0]
door_verts_right = [v for v in bm.verts if v.co.x > 0 and v.co.z < 1 and v.co.y > 0]

if len(door_verts_left) >= 4 and len(door_verts_right) >= 4:
    door_face_left = bm.faces.new(door_verts_left)
    door_face_right = bm.faces.new(door_verts_right)
    bm.faces.remove(door_face_left)  # Remove the left face to create an opening
    bm.faces.remove(door_face_right)  # Remove the right face to create an opening
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