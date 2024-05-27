import bpy
import bmesh
from mathutils import Vector

def create_tent(name, location):
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
    obj.location = location

    # Create a new bmesh object
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # Create an inset on each face of the tent
    faces = [f for f in bm.faces if f.normal.z > 0]  # Select the top faces
    bmesh.ops.inset_individual(bm, faces=faces, thickness=0.1, depth=0)

    # Update the mesh with the new data
    bm.to_mesh(mesh)
    bm.free()

    return obj

# Create  five tents
tent1 = create_tent('Tent1', bpy.context.scene.cursor.location)
tent2 = create_tent('Tent2', bpy.context.scene.cursor.location + Vector((5, 0, 0)))
tent3 = create_tent('Tent3', bpy.context.scene.cursor.location + Vector((20, 0, 6)))
tent4 = create_tent('Tent4', bpy.context.scene.cursor.location + Vector((30, 0, 12)))
tent5 = create_tent('Tent5', bpy.context.scene.cursor.location + Vector((40, 0, 18)))