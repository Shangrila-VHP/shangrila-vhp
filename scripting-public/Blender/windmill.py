import bpy

# Clear all mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a cube for the base
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

# Create a cylinder for the windmill body
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 1))
body = bpy.context.object

# Create an empty object at the top of the body
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 2))
rotator = bpy.context.object
rotator.hide_viewport = True  # Hide the rotator in the viewport
rotator.hide_render = True  # Hide the rotator in the final render

# Create four planes for the propellers and parent them to the rotator
for i in range(4):
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 2))
    propeller = bpy.context.object
    propeller.scale.x = 3
    propeller.rotation_euler = (0, 0, i * 3.14159 / 2)
    propeller.parent = rotator

# Animate the rotator to rotate
rotator.rotation_mode = 'XYZ'
for i in range(250):  # for 250 frames
    rotator.rotation_euler = (0, 0, i * 3.14159 / 60)  # rotate 6 degrees per frame
    rotator.keyframe_insert(data_path="rotation_euler", frame=i, index=2)