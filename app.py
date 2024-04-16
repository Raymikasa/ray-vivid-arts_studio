import os
import boto3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance

app = Flask(__name__)

# AWS Credentials and Configuration
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_DEFAULT_REGION')

# S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Bucket Names
source_bucket_name = 'source-photo'
modified_bucket_name = 'modified-photo'

# Image Processing Functions
def enhance_image(image, color_factor=1.5, saturation_factor=0.8, sharpness_factor=1.5, contrast_factor=1.5):
    """Enhances the image with adjustable color adjustments, sharpness, and contrast."""
    # Convert image to grayscale
    grayscale_image = image.convert('L')
    
    # Adjust color
    enhanced_image = ImageEnhance.Color(grayscale_image).enhance(color_factor)
    
    # Adjust saturation
    enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast_factor)
    
    # Adjust sharpness
    enhanced_image = ImageEnhance.Sharpness(enhanced_image).enhance(sharpness_factor)
    
    # Adjust contrast
    enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast_factor)

    return enhanced_image

# Routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            try:
                s3_client.upload_file(
                    Bucket=source_bucket_name,
                    Filename=filename,
                    Key=filename
                )
                # Open and enhance the image
                with Image.open(filename) as image:
                    enhanced_image = enhance_image(image)

                # Save the processed image
                processed_filename = f"modified-photo/{filename}"
                enhanced_image.save(processed_filename, format='JPEG')  # Save as JPEG format

                # Upload the processed image to the modified bucket
                s3_client.upload_file(
                    Bucket=modified_bucket_name,
                    Filename=processed_filename,
                    Key=processed_filename
                )

                # Generate pre-signed URL for the processed image
                presigned_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': modified_bucket_name, 'Key': processed_filename},
                    ExpiresIn=3600
                )

                # Return the processing completion response
                return redirect(url_for('download', filename=filename, presigned_url=presigned_url))

            except Exception as e:
                error_msg = f"Error handling file: {str(e)}"
                return jsonify({'error': error_msg}), 500
    return render_template("index.html")

@app.route('/download/<filename>/<path:presigned_url>')
def download(filename, presigned_url):
    return render_template('download.html', filename=filename, presigned_url=presigned_url)

if __name__ == '__main__':
    app.run(debug=True)
