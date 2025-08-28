import gradio as gr
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model


model = load_model('sketch2image_best_full.h5',
                   custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
print("Model loaded successfully!")

def generate_face(sketch_img):
    img = cv2.resize(sketch_img, (178, 218))  
    img_input = img.astype(np.float32) / 255.0
    img_input = np.expand_dims(img_input, axis=0)

    predicted = model.predict(img_input)[0]
    predicted = (predicted * 255).astype(np.uint8)

    return predicted

interface = gr.Interface(
    fn=generate_face,
    inputs=gr.Image(type="numpy", label="Upload Your Sketch"),
    outputs=gr.Image(type="numpy", label="Generated Face"),
    title="Sketch to Face Generator",
    description="Upload a sketch image and get a photo-realistic face output using a deep learning model."
)

interface.launch(debug=True)
