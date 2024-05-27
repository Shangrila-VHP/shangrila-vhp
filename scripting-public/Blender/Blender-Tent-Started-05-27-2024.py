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

# Move one of the top vertices to create the tent shape
for v in bm.verts:
    if v.co.z > 0:
        v.co.y = 0

# Update the mesh with the new data
bm.to_mesh(mesh)
bm.free()

# Move the tent to the desired location
obj.location = bpy.context.scene.cursor.location