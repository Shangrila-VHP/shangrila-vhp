import bpy
import bmesh
import sys
sys.path.append('C:\\Users\\user\\Documents\\GitHub\\shangrila-vhp\\scripting-public\\')
import Blender-Windmill-Started-5-26-2024.py

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
tent1 = create_tent('Tent1', (0, 0, 0), size=1, inset_thickness=0.2, inset_depth=0.2)
tent2 = create_tent('Tent2', bpy.context.scene.cursor.location + Vector((5, 0, 0)))
tent3 = create_tent('Tent3', bpy.context.scene.cursor.location + Vector((10, 0, 0)))
tent4 = create_tent('Tent4', bpy.context.scene.cursor.location + Vector((15, 0, 0)))
tent5 = create_tent('Tent5', bpy.context.scene.cursor.location + Vector((20, 0, 0)))

