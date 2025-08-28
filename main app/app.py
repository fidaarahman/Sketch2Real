from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import base64
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

print("Loading model...")
try:
    model = load_model("sketch2image_legacy.h5", compile=False)
    print(" Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

def preprocess_to_sketch(image_pil):
   
    image = np.array(image_pil)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray_inv = 255 - img_gray
    img_blur = cv2.GaussianBlur(img_gray_inv, ksize=(21, 21), sigmaX=0, sigmaY=0)
    sketch = cv2.divide(img_gray, 255 - img_blur, scale=256.0)
    sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

   
    sketch = cv2.resize(sketch, (178, 218))
    sketch = sketch.astype(np.float32) / 255.0
    sketch = np.expand_dims(sketch, axis=0)
    return sketch

def postprocess_output(output):
    img = (output[0] * 255).astype(np.uint8)
    return Image.fromarray(img)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image = Image.open(file_path).convert('RGB')
            print(f"📁 Received file upload: {filename}")
        elif 'imageData' in request.form:
            image_data = request.form['imageData']
            header, encoded = image_data.split(',', 1)
            decoded = base64.b64decode(encoded)
            image = Image.open(io.BytesIO(decoded)).convert('RGB')
            filename = 'canvas.png'
            print("🖌️ Received canvas drawing")
        else:
            print("❌ No image found in request")
            return jsonify({'error': 'No image provided'}), 400

        input_tensor = preprocess_to_sketch(image)

        print(f"🧠 Predicting with model...")
        output = model.predict(input_tensor)
        print(f"✅ Prediction complete.")

        generated_image = postprocess_output(output)
        result_filename = f'result_{filename}'
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        generated_image.save(result_path)
        print(f"💾 Saved result image: {result_filename}")

        return jsonify({
            'original': f'/static/uploads/{filename}',
            'result': f'/static/uploads/{result_filename}'
        })

    except Exception as e:
        print(f"Error during upload processing: {e}")
        return jsonify({'error': 'Processing failed', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
