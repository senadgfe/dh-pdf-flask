from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import pytesseract
from pdf2image import convert_from_path
import fitz
import numpy as np
from datetime import datetime
from flask import flash
import re
import cv2
from PIL import Image, ImageDraw, ImageFont

application = Flask(__name__) 

# Configurationsl
UPLOAD_FOLDER = './static/uploads'
UPLOAD_FOLDER_ANNOTATED = './static/uploads/annotated'
ALLOWED_EXTENSIONS = {'pdf'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['UPLOAD_FOLDER_ANNOTATED'] = UPLOAD_FOLDER_ANNOTATED
application.config['MAX_CONTENT_LENGTH'] = 16 * \
    1024 * 1024  # 16MB upload limit


def generate_model_name(dimensions):
    # Split the dimensions using commas
    dimensions_list = dimensions.split(',')

    # Extract the numerical values using regex
    numbers = [re.search(r"(\d+\.\d+)", dim).group(1)
               for dim in dimensions_list if re.search(r"(\d+\.\d+)", dim)]

    # Generate the model name
    if len(numbers) == 3:  # If there are three dimensions
        return f"DH_{numbers[0]}x{numbers[1]}x{numbers[2]}"
    elif len(numbers) == 2:  # If there are two dimensions
        return f"DH_{numbers[0]}x{numbers[1]}"
    else:
        return "ModelNotFound"

# Function to check file extension

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_path):
    # Convert each PDF page to an image
    images = convert_from_path(file_path, dpi=600)  # Set dpi to 600

    # Initialize an empty string to hold the extracted text
    extracted_text = ''

    # Loop through each image and perform OCR
    for i in range(len(images)):
        extracted_text += pytesseract.image_to_string(images[i])

    return extracted_text


def hide_layers_box_outlines(file_path):
    doc = fitz.open(file_path)

    ocgs = doc.get_ocgs()
    layer = doc.get_layer()
    onLayer = layer.get("on", [])
    offLayer = layer.get("off", [])

    for key in ocgs:
        if ocgs[key]['name'].lower().find('maß') > -1 or ocgs[key]['name'].lower().find('bemassung') > -1 or ocgs[key]['name'].lower().find('vermassung') > -1 or ocgs[key]['name'].lower().find('dispersion') > -1 or ocgs[key]['name'].lower().find('lack') > -1 or ocgs[key]['name'].lower().find('jobinfo') > -1 or ocgs[key]['name'].lower().find('braille') > -1 or ocgs[key]['name'].lower().find('faz') > -1 or ocgs[key]['name'].lower().find('praegung') > -1 or ocgs[key]['name'].lower().find('blinden') > -1 or ocgs[key]['name'].lower().find('varnish') > -1:
            if key in onLayer:
                onLayer.remove(key)
                offLayer.append(key)

    doc.set_layer(-1, on=onLayer, off=offLayer)

    # Save the modified PDF and return its file path
    new_file_path = os.path.join(
        application.config['UPLOAD_FOLDER'], "hidden_layers_box_outlines_" + os.path.basename(file_path))
    doc.save(new_file_path, garbage=4)
    doc.close()

    return new_file_path


def hide_layers(file_path):
    doc2 = fitz.open(file_path)

    ocgs = doc2.get_ocgs()
    layer = doc2.get_layer()
    onLayer = layer.get("on", [])
    offLayer = layer.get("off", [])

    for key in ocgs:
        if ocgs[key]['name'].lower().find('stanz') > -1 or ocgs[key]['name'].lower().find('maß') > -1 or ocgs[key]['name'].lower().find('bemassung') > -1 or ocgs[key]['name'].lower().find('vermassung') > -1 or ocgs[key]['name'].lower().find('kontur') > -1 or ocgs[key]['name'].lower().find('dispersion') > -1 or ocgs[key]['name'].lower().find('lack') > -1 or ocgs[key]['name'].lower().find('guides') > -1 or ocgs[key]['name'].lower().find('jobinfo') > -1 or ocgs[key]['name'].lower().find('braille') > -1 or ocgs[key]['name'].lower().find('faz') > -1 or ocgs[key]['name'].lower().find('praegung') > -1 or ocgs[key]['name'].lower().find('blinden') > -1 or ocgs[key]['name'].lower().find('cutter') > -1 or ocgs[key]['name'].lower().find('varnish') > -1:
            if key in onLayer:
                onLayer.remove(key)
                offLayer.append(key)

    doc2.set_layer(-1, on=onLayer, off=offLayer)

    # Save the modified PDF and return its file path
    new_file_path = os.path.join(
        application.config['UPLOAD_FOLDER'], "hidden_layers_" + os.path.basename(file_path))
    doc2.save(new_file_path, garbage=4)
    doc2.close()

    return new_file_path

def extract_dimensions(text):
    # Replace commas with dots
    text = text.replace(',', '.')

    # Remove all spaces
    text = text.replace(' ', '')

    # Replace all variations of 'x' with a single standard 'x'
    text = re.sub(r'[xX×]', 'x', text)

    # Handle extra 'x's not involved in dimensions
    text = re.sub(r'x(?!\d)', '', text)

    # This regular expression will find strings that look like dimensions
    three_dimension_regex = r'(\d{1,3}(?:\.\d{1})?)x(\d{1,3}(?:\.\d{1})?)x(\d{1,3}(?:\.\d{1})?)'
    two_dimension_regex = r'(\d{1,3}(?:\.\d{1})?)x(\d{1,3}(?:\.\d{1})?)'

    matches = re.findall(three_dimension_regex, text)

    # If three dimensional matches are found, format the first one and return
    if matches:
        match = matches[0]
        dimensions = "Breite: {} mm, Tiefe: {} mm, Höhe: {} mm".format(
            round(float(match[0]), 1), round(float(match[1]), 1), round(float(match[2]), 1))
        print("Extracted dimensions:", dimensions)
        return dimensions
    else:
        matches = re.findall(two_dimension_regex, text)
        # If two dimensional matches are found, format the first one and return
        if matches:
            match = matches[0]
            dimensions = "Breite: {} mm, Höhe: {} mm".format(
                round(float(match[0]), 1), round(float(match[1]), 1))
            print("Extracted dimensions:", dimensions)
            return dimensions

    
    return None


def get_main_object_dimensions(image):
    # Convert the PIL Image object to a numpy array
    np_image = np.array(image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get non-white pixels. 255 is the value for white, so we use a bit less.
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours from the thresholded image (non-white regions)
    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If there are no contours, return None
    if not contours:
        return None

    # Find the largest contour (main object) based on contour area
    main_contour = max(contours, key=cv2.contourArea)

    # Calculate the bounding rectangle around the main contour
    x, y, w, h = cv2.boundingRect(main_contour)

    return w, h


def get_image_objects_dimensions_and_draw(image, cutter_image, image_name, model_variation):
    # Create a copy of the original image to prevent color distortion and annotations
    original_image = image.copy()
    cutter_image_original = cutter_image.copy()
    print(original_image)
    def extract_contours_and_crop(np_img, original_img):
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None, None, None, None, None

        x_min, y_min = np.inf, np.inf
        x_max, y_max = 0, 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        cropped_image = np.array(original_img)[y_min:y_max, x_min:x_max]
        return cropped_image, x_min, x_max, y_min, y_max

    sub_image, x_min, x_max, y_min, y_max = extract_contours_and_crop(
        np.array(original_image), original_image)
    sub_image_box_outlines, _, _, _, _ = extract_contours_and_crop(
        np.array(original_image), cutter_image_original)

    # Convert numpy images to PIL
    sub_image_pil = Image.fromarray(
        sub_image) if sub_image is not None else None
    sub_image_box_outlines_pil = Image.fromarray(
        sub_image_box_outlines) if sub_image_box_outlines is not None else None

    # Calculate the proportion of width to height
    proportion = (x_max - x_min) / \
        (y_max - y_min) if (y_max - y_min) != 0 else 0
    proportion_string = f"Proportion (Breite/Höhe) = {proportion:.2f}"

    # Annotate the image with dimensions
    draw = ImageDraw.Draw(original_image)
    font_size = 60
    font = ImageFont.truetype("static/arial.ttf", font_size)
    dimensions_string = f"Breite = {x_max - x_min} pixels, Höhe = {y_max - y_min} pixels"
    draw.text((10, 10), dimensions_string, fill="red", font=font)
    draw.text((10, 60), proportion_string, fill="red", font=font)
    draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=3)

    annotated_folder_path = application.config['UPLOAD_FOLDER_ANNOTATED']
    if not os.path.exists(annotated_folder_path):
        os.makedirs(annotated_folder_path)

    # Save the sub-image as a separate high-quality PNG with timestamp
    sub_image_path = os.path.join(
        annotated_folder_path, f'{image_name}_{model_variation}.png')
    sub_image_pil.save(sub_image_path, "PNG", quality=95)

    # Save the sub-image_box_outlines with timestamp
    sub_image_path_box_outlines = os.path.join(
        annotated_folder_path, f'{image_name}_box_outlines.png')
    sub_image_box_outlines_pil.save(sub_image_path_box_outlines, "PNG", quality=95)

    # Relative paths for serving images to the frontend with timestamp
    sub_image_path = os.path.join(
        '/uploads/annotated/', f'{image_name}_{model_variation}.png')
    sub_image_path_box_outlines = os.path.join(
        '/uploads/annotated/', f'{image_name}_box_outlines.png')


    return {
        # "image_path": image_path,
        "sub_image_path": sub_image_path,
        "sub_image_path_box_outlines": sub_image_path_box_outlines,
        "dimensions": dimensions_string,
        "proportion": proportion_string
    }

def process_pdf(file_path):
    # Hide layers in PDF first
    hidden_layers_pdf_path = hide_layers(file_path)
    hidden_layers_pdf_path_box_outlines = hide_layers_box_outlines(file_path)
    
    # extract filename
    # Normalize the path to handle mixed slashes
    normalized_path = os.path.normpath(hidden_layers_pdf_path)

    # Get the base file name
    file_name = os.path.basename(normalized_path)
    # Remove the ".pdf" extension if it exists
    image_name = os.path.splitext(file_name)[0]

    # Then, Convert the modified PDFs to images
    images = convert_from_path(hidden_layers_pdf_path, dpi=600)
    images_box_outlines = convert_from_path(
        hidden_layers_pdf_path_box_outlines, dpi=600)
    
    # Convert the original PDF to images for OCR
    original_images = convert_from_path(file_path, dpi=600)

    extracted_text = ''
    for image in original_images:
        extracted_text += pytesseract.image_to_string(image)

    # Extract dimensions from the text
    text_dimensions = extract_dimensions(extracted_text)

    # Look up the model using the extracted dimensions
    model_variation = generate_model_name(
        text_dimensions) if text_dimensions else 'Model not found'


    # Get image dimensions
    sub_image_paths = []
    image_dimensions = []
    image_proportions = []
    sub_image_paths_box_outlines = []

    # Assuming both 'images' and 'images_box_outlines' have the same length
    for i in range(len(images)):
        result = get_image_objects_dimensions_and_draw(
            images[i], images_box_outlines[i],image_name,model_variation)

        if result is not None:
            #image_file_paths.append(result["image_path"])
            sub_image_paths.append(result["sub_image_path"])
            image_dimensions.append(result["dimensions"])
            image_proportions.append(result["proportion"])
            sub_image_paths_box_outlines.append(result["sub_image_path_box_outlines"])

    print("Extracted text:", extracted_text)

    return images, text_dimensions, image_dimensions, image_proportions, sub_image_paths, model_variation, sub_image_paths_box_outlines

@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select a file, the browser also submits an empty part without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)    
        if file and allowed_file(file.filename):
        
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                application.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process the new PDF file
            images, text_dimensions, image_dimensions, image_proportions, sub_image_paths, model_variation, sub_image_paths_box_outlines = process_pdf(
                file_path)

            # Return the dimensions to the user
            return render_template('upload.html',
                                text_dimensions=text_dimensions,
                                dimensions=image_dimensions,
                                sub_image_paths=sub_image_paths,
                                sub_image_paths_box_outlines=sub_image_paths_box_outlines,
                                model_variation=model_variation)

    return render_template('upload.html')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(UPLOAD_FOLDER_ANNOTATED):
        os.makedirs(UPLOAD_FOLDER_ANNOTATED)
    application.run(port=5003, debug=True)

