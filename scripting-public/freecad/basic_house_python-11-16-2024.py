import FreeCAD
import Part

# House dimensions
house_width = 6
house_length = 4
house_height = 3

# Door dimensions
door_width = 1.5
door_height = 2.5

# Window dimensions (big and small)
big_window_width = 2
big_window_height = 2
small_window_width = 1
small_window_height = 1

# Create the house body
house_box = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "House")
house_box.Length = house_length
house_box.Width = house_width
house_box.Height = house_height

# Create the front door
front_door = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "FrontDoor")
front_door.Length = door_height
front_door.Width = door_width
front_door.Placement = FreeCAD.Placement(FreeCAD.Vector(house_length/2 - door_height/2, house_width/2 - door_width/2, 0), FreeCAD.Rotation(0,0,0)) # Adjust placement

# Create the back door
back_door = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "BackDoor")
back_door.Length = door_height
back_door.Width = door_width
back_door.Placement = FreeCAD.Placement(FreeCAD.Vector(-house_length/2 + door_height/2, house_width/2 - door_width/2, 0), FreeCAD.Rotation(0,0,0))

# Create the big window
big_window = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "BigWindow")
big_window.Length = big_window_height
big_window.Width = big_window_width
big_window.Placement = FreeCAD.Placement(FreeCAD.Vector(0, -house_width/2 + big_window_width/2, house_height/2 - big_window_height/2), FreeCAD.Rotation(0,0,0))

# Create the small windows (back)
small_window1 = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "SmallWindow1")
small_window1.Length = small_window_height
small_window1.Width = small_window_width
small_window1.Placement = FreeCAD.Placement(FreeCAD.Vector(-house_length/2 + small_window_height/2, -house_width/2 + small_window_width/2, house_height/2 - small_window_height/2), FreeCAD.Rotation(0,0,0))

small_window2 = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "SmallWindow2")
small_window2.Length = small_window_height
small_window2.Width = small_window_width
small_window2.Placement = FreeCAD.Placement(FreeCAD.Vector(-house_length/2 + small_window_height/2, house_width/2 - small_window_width/2 * 1.5, house_height/2 - small_window_height/2), FreeCAD.Rotation(0,0,0))



# Simple roof (replace with a more realistic roof if needed)
roof = FreeCAD.newDocument("TinyHouse").addObject("Part::Box", "Roof")
roof.Length = house_length
roof.Width = house_width
roof.Height = house_height/2
roof.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, house_height), FreeCAD.Rotation(0,0,0))

#This part doesn't work
#Add color (this requires more advanced techniques for realistic materials)
#house_box.ViewObject.ShapeColor = (1,0,0) # Red

FreeCAD.ActiveDocument.recompute()