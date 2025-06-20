import bpy

# Delete any existing balls and ground planes
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Sphere'].select_set(True)
bpy.data.objects['Plane'].select_set(True)
bpy.ops.object.delete()

# Create a sphere for the ball
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 5))
ball = bpy.context.object

# Enable rigid body physics for the ball
ball.select_set(True)
bpy.ops.rigidbody.object_add()

# Set the ball's bounce factor
ball.rigid_body.restitution = 0.9

# Create a plane for the ground
bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=False, align='WORLD', location=(0, 0, 0))

# Enable rigid body physics for the ground
ground = bpy.context.object
ground.select_set(True)
bpy.ops.rigidbody.object_add()

# Set the ground's bounce factor
ground.rigid_body.restitution = 0.9
ground.rigid_body.type = 'PASSIVE'