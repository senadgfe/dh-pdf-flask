import subprocess
import os
import app

class Image_Textures: 
    elektrolyte = r"C:\Shared\Work\GFE\dh-pdf-flask\static\uploads\annotated\90588409_FS_DH_Elektrolyte_Extra_20_Btl-PDFX4_2_MV130x52x110.png"
    az = r"C:\Shared\Work\GFE\dh-pdf-flask\static\uploads\annotated\90587479_FS_DH_A_Z_Complete_DEPOT_Tbl_40-PDFX4_2_MV85x46x122.png"
    melatonin = r"C:\Shared\Work\GFE\dh-pdf-flask\static\uploads\annotated\90587310_FS_DH_Melatonin-Heissgetraenk_Btl_20-PDFX4_2_MV94x64x106.png"

class pdfs:
    halsschmerzen = r"C:\Shared\Work\GFE\dh-pdf-flask\static\uploads\annotated\hl_90587043_FS_DH_Halsschmerzen_Tbl_24-PDFX4_2_MV76x21x125.png"
    melatonin = r"C:\Shared\Work\GFE\dh-pdf-flask\static\uploads\90588160_FS_DH_Melatonin_1,8mg_40_Tbl-PDFX4_2.pdf"
    
texture_path = Image_Textures.halsschmerzen   
class Engine:
    eevee = "BLENDER_EEVEE"
    cycles = "CYCLES"

blender_executable = "blender"  # Replace with the full path to your Blender executable if necessary
blender_file = os.path.abspath("./blender/Boxgenerator.blend")  # Replace with the correct path to your Blender file
script = "./blender/generate_images.py"
rgb_profile = "./profiles/sRGB.icm"
cmyk_profile = "./profiles/ISOcoated_v2_300_eci.icc"
output_folder = 'C:/Shared/Work/GFE/dh-pdf-flask/blender/output'
texture_output_folder = "C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated"

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
        convert_cmyk = f"convert {file} -profile {rgb_profile} -profile {cmyk_profile} {file} -compress LZW"
        os.system(convert_cmyk)
        
def generate_single_image(texture_path):
    texture_path = texture_path.replace("\\", "/")
    generate_image = f"{blender_executable} -b {blender_file} -P {script} -- {texture_path} {output_folder}"
    os.system(generate_image)

def generate_texture(inputfile, outputfolder):
    texture_file = f"python3 app.py {inputfile} {outputfolder}"
    print(texture_file)
    return texture_file

    
# generate_texture(pdfs.melatonin, texture_output_folder)
generate_single_image(texture_path)

# generate_images()
#convert_to_cmyk()
