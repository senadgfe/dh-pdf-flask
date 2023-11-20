import subprocess
import os

testingSet = [
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90586810_FS_DHP_Minoxidil_fuer_Frauen_60ml-PDFX4_2_MV100x40x162.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90586393_FS_DH_AugenTropfen_Hyaluron_04_Extra_10ml-PDFX4_2_MV31x31x87.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90586895_FS_DH_Kollagen3000_Btl14-PDFX4_2_MV69x50x142.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90587041_FS_DH_Bei_Reizdarm_Tbl_30-PDFX4_2_MV69x23x133.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90587051_FS_DH_Rachen-PDFX4_2_MV38x38x105.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90587116_FS_DH_Eisen_Spray_60ml-PDFX4_2_MV53x53x120.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90587310_FS_DH_Melatonin-Heissgetraenk_Btl_20-PDFX4_2_MV94x64x106.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90588401_FS_DH_B12_Intense_Vita_Energie_TrinkFl_8-PDFX4_2_MV101x52x69.png",
"C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90588403_FS_DH_B12_Intense_Vita_Energie_TrinkFl_18er-PDFX4_2_MV75x75x130.png",
]

blender_executable = "blender"  # Replace with the full path to your Blender executable if necessary
blender_file = os.path.abspath("./blender/Boxgenerator.blend")  # Replace with the correct path to your Blender file
script = "./blender/generate_images.py"
rgb_profile = "./profiles/sRGB.icm"
cmyk_profile = "./profiles/ISOcoated_v2_300_eci.icc"
output_folder = 'C:/Shared/Work/GFE/dh-pdf-flask/blender/output'

def generate_images():
    for texture in testingSet:
        generate_single_image(texture)

def convert_to_cmyk():
    # Get a list of all files in the folder
    files = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))]

    # Print the list of files
    for file in files:
        print(f'Convert to CMYK: {file}')
        os.chdir(output_folder)
        convert_cmyk = f"convert {file} -profile {rgb_profile} -profile {cmyk_profile} {file}"
        os.system(convert_cmyk)
        
def generate_single_image(texture):
    # image_path = 'C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90586393_FS_DH_AugenTropfen_Hyaluron_04_Extra_10ml-PDFX4_2_MV31x31x87.png'
    generate_image = f"{blender_executable} -b {blender_file} -P {script} -- {texture} {output_folder}"
    os.system(generate_image)
    
# generate_single_image()

generate_images()
convert_to_cmyk()
