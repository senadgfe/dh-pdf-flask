# dh-pdf-flask


# Image Generation
To test the image generation process run blender using the following parameter :
blender -b Boxgenerator.blend -P generate_images.py -- 'C:/Shared/Work/GFE/dh-pdf-flask/static/uploads/annotated/90586393_FS_DH_AugenTropfen_Hyaluron_04_Extra_10ml-PDFX4_2_MV31x31x87.png' 'C:/Shared/Work/GFE/dh-pdf-flask/blender/output'

Have a look at the start_blender.py. The scructure of alling the script and input paramaters are as follows:
f"{blender_executable} -b {blender_file} -P {script} -- {image_path} {output_folder}"
