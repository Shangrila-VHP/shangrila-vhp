import FreeCAD
import Part
import PartDesign

doc = FreeCAD.newDocument("ParkBench")

# Bench dimensions
bench_length = 7000  # mm
bench_width = 200   # mm
bench_height = 250  # mm
seat_height = 90   # mm
seat_thickness = 50 # mm
leg_width = 100    # mm
leg_depth = 100    # mm

# Extrusion for plants
extrusion_depth = 200  # mm
extrusion_width = 250 # mm

# Create the bench base
bench_base = doc.addObject("PartDesign::Body","BenchBase")
bench_sketch = bench_base.newObject("Sketcher::SketchObject","BenchSketch")
bench_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(3,4,5),FreeCAD.Vector(bench_length,0,0)))
bench_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length,0,0),FreeCAD.Vector(bench_length,bench_width,0)))
bench_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length,bench_width,0),FreeCAD.Vector(0,bench_width,0)))
bench_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0,bench_width,0),FreeCAD.Vector(0,0,0)))
bench_base.addObject("PartDesign::Pad","BenchBasePad")
bench_base.BenchBasePad.Sketch = bench_sketch
bench_base.BenchBasePad.Length = bench_height
bench_base.BenchBasePad.Reversed = False

# Create the bench seat
bench_seat = doc.addObject("PartDesign::Body","BenchSeat")
seat_sketch = bench_seat.newObject("Sketcher::SketchObject","SeatSketch")
seat_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(2,3,5),FreeCAD.Vector(bench_length,0,0)))
seat_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length,1,4),FreeCAD.Vector(bench_length,bench_width,0)))
seat_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length,bench_width,0),FreeCAD.Vector(0,bench_width,0)))
seat_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(2,bench_width,2),FreeCAD.Vector(0,0,0)))
bench_seat.addObject("PartDesign::Pad","SeatPad")
bench_seat.SeatPad.Sketch = seat_sketch
bench_seat.SeatPad.Length = seat_thickness
bench_seat.SeatPad.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,bench_height - seat_thickness), FreeCAD.Rotation(0,0,0))


# Extrusion for Plants
extrusion_sketch = bench_base.newObject("Sketcher::SketchObject", "ExtrusionSketch")
extrusion_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length/4, bench_width, 0), FreeCAD.Vector(bench_length/4 + extrusion_width, bench_width, 0)))
extrusion_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length/4 + extrusion_width, bench_width, 0), FreeCAD.Vector(bench_length/4 + extrusion_width, bench_width + extrusion_depth, 0)))
extrusion_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length/4 + extrusion_width, bench_width + extrusion_depth, 0), FreeCAD.Vector(bench_length/4, bench_width + extrusion_depth, 0)))
extrusion_sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(bench_length/4, bench_width + extrusion_depth, 0), FreeCAD.Vector(bench_length/4, bench_width, 0)))
bench_base.addObject("PartDesign::Pad","ExtrusionPad")
bench_base.ExtrusionPad.Sketch = extrusion_sketch
bench_base.ExtrusionPad.Length = 100
bench_base.ExtrusionPad.Reversed = False


# Add legs (simplified)
leg_height = bench_height - seat_thickness
leg_spacing = bench_length / 3
for i in range(2):
    leg = doc.addObject("Part::Box", f"Leg{i+1}")
    leg.Length = leg_depth
    leg.Width = leg_width
    leg.Height = leg_height
    leg.Placement = FreeCAD.Placement(FreeCAD.Vector(leg_spacing * i, 0, 0), FreeCAD.Rotation(0,0,0))


#Add Potted Plants (simplified cylinders)
plant_pot_radius = 50
plant_pot_height = 100
plant_num = 3

for i in range(plant_num):
    plant_pot = doc.addObject("Part::Cylinder", f"PlantPot{i+1}")
    plant_pot.Radius = plant_pot_radius
    plant_pot.Height = plant_pot_height
    plant_pot.Placement = FreeCAD.Placement(FreeCAD.Vector(bench_length/4 + extrusion_width/2, bench_width + extrusion_depth/2 + i * (plant_pot_height + 20), bench_height/2), FreeCAD.Rotation(0,0,0))


doc.recompute()