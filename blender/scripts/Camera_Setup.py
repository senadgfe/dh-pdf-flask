import bpy
import os

names = ["front","right","back","left"]

# Select the active object
obj = bpy.data.objects["CameraCircle"]

# Set the camera and the render settings
bpy.context.scene.camera = bpy.data.objects["Camera"]
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Create a new folder for the rendered images
output_folder = os.path.join(os.path.dirname(bpy.data.filepath), "output")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through four rotations and renders
for i in range(4):

    # Set the filepath for the rendered image
    bpy.context.scene.render.filepath = os.path.join(output_folder, names[i] + ".png")
    
    # Render the image
    bpy.ops.render.render(write_still=True)
    
    # Rotate the object 90 degrees around the z-axis
    obj.rotation_euler[2] += 1.5708

obj.rotation_euler[2] = 0