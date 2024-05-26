import bpy

# Clear all mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create the body of the windmill
bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=6, location=(0, 0, 1))
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

# Create a cylinder to serve as the rod
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1, location=(0, 0, 2.5))
rod = bpy.context.object
rod.parent = rotator

# Create four planes for the propellers and parent them to the rotator
for i in range(4):
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 1.25 + i * 0.5))  # Adjust the Z location to be inside the cylinder
    propeller = bpy.context.object
    propeller.scale.x = 0.1  # Make the propellers long and thin
    propeller.scale.y = 3
    propeller.rotation_euler = (3.14159 / 2, 0, i * 3.14159 / 2)  # Rotate propellers to be perpendicular to the X-axis and evenly spaced around the rotator
    propeller.parent = rotator

    # Convert the plane to a mesh and give it some thickness
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.1)})
    bpy.ops.object.mode_set(mode='OBJECT')

# Animate the rotator to rotate
rotator.rotation_mode = 'XYZ'
for i in range(250):  # for 250 frames
    rotator.rotation_euler = (0, 0, i * 3.14159 / 60)  # rotate 6 degrees per frame
    rotator.keyframe_insert(data_path="rotation_euler", frame=i, index=2)