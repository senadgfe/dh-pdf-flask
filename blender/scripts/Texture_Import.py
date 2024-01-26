import bpy
import os
import sys

# Get the relative path to the texture

testingSet = [
"90586393_FS_DH_AugenTropfen_Hyaluron_04_Extra_10ml-PDFX4_2_MV31x31x87.png",
"90586450_FS_DHP_Allergo-Azelind_6ml-PDFX4_2_MV28x28x75.png",
"90586810_FS_DHP_Minoxidil_fuer_Frauen_60ml-PDFX4_2_MV100x40x162.png",
"90586895_FS_DH_Kollagen3000_Btl14-PDFX4_2_MV69x50x142.png",
"90587041_FS_DH_Bei_Reizdarm_Tbl_30-PDFX4_2_MV69x23x133.png",
"90587051_FS_DH_Rachen-PDFX4_2_MV38x38x105.png",
"90587116_FS_DH_Eisen_Spray_60ml-PDFX4_2_MV53x53x120.png",
"90587310_FS_DH_Melatonin-Heissgetraenk_Btl_20-PDFX4_2_MV94x64x106.png",
"90588401_FS_DH_B12_Intense_Vita_Energie_TrinkFl_8-PDFX4_2_MV101x52x69.png",
"90588403_FS_DH_B12_Intense_Vita_Energie_TrinkFl_18er-PDFX4_2_MV75x75x130.png",
"90588404_FS_DH_B12_Vita_Energie_TrinkFl_30_Amazon-PDFX4_2_MV125x75x130.png",
"90588409_FS_DH_Elektrolyte_Extra_20_Btl-PDFX4_2_MV130x52x110.png",
"90587915_FS_DH_Heisser_CurcumaManuka-Honig_Btl_10-PDFX4_2_MV94x75x128.png",
"90587998_FS_DH_Magnesium_500_B12_D3_DIRECT_DEPOT_Port_60-PDFX4_2_MV100x100x80.png",
]

def select_testing_set(mv):
    for index, entry in enumerate(testingSet):
        if mv in entry:
            return index;
        
mv = bpy.context.view_layer.name.split('MV')[1]
index = select_testing_set(mv)

relative_path = "../static/uploads/annotated"
texture_name = testingSet[index]
texture_path = os.path.join(os.path.dirname(bpy.data.filepath), relative_path, texture_name)
texture_path = texture_path.replace("\\", "/")


if len(sys.argv) > 2:
    # Access the parameter value
    texture_name = sys.argv[-1]

    # Now you can use parameter_value in your script
    print("Parameter value:", texture_name)
    
    # override the texture path
    texture_path = os.path.join(os.path.dirname(bpy.data.filepath), relative_path, texture_name)


def find_image(texture_path):
    for img in bpy.data.images:
        if img.filepath == texture_path:
            return img
    return None

def replace_texture(texture_path):
    print(f'Replacing texture with {texture_path}')
    
    # Check if the texture file exists
    if os.path.exists(texture_path):
        # Find the active object's active material
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
            view_layer.use = True
            # Set this view layer in the render layers for the compositor
            for node in bpy.context.scene.node_tree.nodes:
                if node.type == 'R_LAYERS':
                    # Set the selected view layer in the Render Layers node
                    node.layer = view_layer.name
        else:
            # Disable other view layers for rendering
            view_layer.use = False  

setup_view_layer(mv)
replace_texture(texture_path)
