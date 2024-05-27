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

# Create a cylinder for the body of the windmill
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=4, location=(0, 0, 2))

# Create an empty object at the top of the body to serve as the rotator
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 4))
rotator = bpy.context.object
rotator.hide_viewport = True  # Hide the rotator in the viewport
rotator.hide_render = True  # Hide the rotator in the final render

#05-26-2024: Commenting this out as we do not need the cone at the top.
# Create a cone for the cap of the windmill and parent it to the rotator
# bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=1.2, depth=1, location=(0, 0, 4.5))
#cap = bpy.context.object
#cap.parent = rotator

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
    curved_blade.scale.x = 0.7  # Make the curved blades broad and thin
    curved_blade.scale.y = 5
    curved_blade.scale.z = 0.3  # Make the curved blades flat
    # Existing code
    curved_blade.parent = rotator
    
    # New code
    # Create a protective mesh around the windmill
    bpy.ops.mesh.primitive_cylinder_add(radius=2.5, depth=10, location=(0, 0, 5))  # Adjust the depth to cover the whole windmill
    protective_mesh = bpy.context.object

    # 05-26-2024: *This line hides the Mesh!*
    # protective_mesh.hide_viewport = True

    protective_mesh.scale.x = 1.1  # Make the protective mesh slightly larger than the windmill
    protective_mesh.scale.y = 1.1
    protective_mesh.scale.z = 2  # Stretch the protective mesh along the Z-axis
    
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