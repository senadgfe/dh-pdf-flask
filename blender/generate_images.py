import bpy
import os
import sys
import subprocess

texture_path = ""
output_folder = ""
image_name = ""


if len(sys.argv) > 3:
    # Access the parameter value
    texture_path = sys.argv[6]
    output_folder = sys.argv[7]
    image_name = os.path.basename(texture_path)

    print("Texture File: ", texture_path)
    print("Output Folder: ", output_folder)
    
    
mv = texture_path.removesuffix(".png").split("MV")[1]
print("Model Varaint: ",mv)



# override the texture path
# texture_path = os.path.join(os.path.dirname(bpy.data.filepath), relative_path, texture_path)

def find_image(texture_path):
    for img in bpy.data.images:
        if img.filepath == texture_path:
            return img
    return None

def replace_texture(texture_path):
    print(f'Replacing texture with {texture_path}')
    
    # Check if the texture file exists
    if os.path.exists(texture_path):

        material = bpy.data.materials.get("Texture_Material")
        if material is None:
            print("Error: No active material found!")
            return
        
        # Find image texture nodes in the material
        texture_nodes = [node for node in material.node_tree.nodes if node.name == 'Base Color']
        
        for texture_node in texture_nodes:
            # Try to find the image in bpy.data.images
            existing_image = find_image(texture_path)
            print(texture_node)
            
            if existing_image:
                # Image already exists, use it instead of loading a new one
                texture_node.image = existing_image
                print("Using existing image.")
            else:
                # Load the new texture image
                texture_node.image = bpy.data.images.load(texture_path)
                print("Loaded new image.")
            
            print("Texture replaced successfully!")
            return
        else:
            print("Error: No image texture node found in the material!")
    else:
        print("Error: Texture file not found!")
        
def setup_view_layer(mv):
    # Iterate through all the view layers
    for view_layer in bpy.context.scene.view_layers:
        # Check if the view layer name contains the specified string
        if mv in view_layer.name:
            # Enable the view layer for rendering
            print("MV in " + view_layer.name)
            view_layer.use = True
            # Set this view layer in the render layers for the compositor
            for node in bpy.context.scene.node_tree.nodes:
                if node.type == 'R_LAYERS':
                    # Set the selected view layer in the Render Layers node
                    node.layer = view_layer.name
        else:
            # Disable other view layers for rendering
            view_layer.use = False  
            
        
def render_images(image_name):  
    # remove ending
    image_name = image_name.removesuffix(".png")
              
    names = [image_name + "_front",image_name + "_right",image_name + "_back",image_name + "_left"]
    

    # Select the active object
    obj = bpy.data.objects["CameraCircle"]

    # Set the camera and the render settings
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    bpy.context.scene.render.image_settings.file_format = 'TIFF'

    # Create a new folder for the rendered images
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through four rotations and renders
    for i in range(4):

        print(f'Saving image to : {output_folder}' )
        # Set the filepath for the rendered image
        bpy.context.scene.render.filepath = os.path.join(output_folder, names[i] + ".tiff")
        
        # Render the image
        bpy.ops.render.render(write_still=True)
        
        # Rotate the object 90 degrees around the z-axis
        obj.rotation_euler[2] += 1.5708

    obj.rotation_euler[2] = 0
    
replace_texture(texture_path)
setup_view_layer(mv)
render_images(image_name)


