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

# Create a door as a new face
door_verts = [v for v in bm.verts if v.co.y < 0]
if len(door_verts) >= 3:
    door_face = bm.faces.new(door_verts)
else:
    print("Not enough vertices to create a door.")

# Update the mesh with the new data
bm.to_mesh(mesh)
bm.free()

# Move the tent to the desired location
obj.location = bpy.context.scene.cursor.location