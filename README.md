## Sketch2Real

A research-oriented deep learning project for sketch-to-image translation using the CelebA dataset.

### Features
- **Sketch ➜ Photorealistic image** translation
- **Deep learning** image-to-image model (TensorFlow/Keras)
- **CelebA** dataset for training/validation
- **Colab-ready** notebook for full pipeline
- **Web demo** in `main app/` (Flask)
- **Modular design** for extension to GANs and other architectures

### Project Structure
```
├── .git/                     # Git configuration
├── command.txt               # Setup and run commands
├── final_notebook.ipynb      # Complete training & preprocessing notebook (Colab-friendly)
├── main app/                 # Main application (inference/web)
│   ├── app.py                # Flask web app entrypoint
│   ├── new.py                # Auxiliary script (utility/demo)
│   └── train_model.py        # U-Net training script (Colab paths by default)
├── static/                   # Static assets for the web app
│   ├── css/
│   ├── js/
│   └── uploads/              # Saved inputs/outputs at runtime
├── templates/                # HTML templates for Flask
│   └── index.html
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

### Dataset
We use the **CelebA** dataset (large-scale face images).
- **Sketch domain**: Preprocessed using OpenCV (grayscale, inversion, Gaussian blur; division blending) to generate pencil-sketched images.
- **Real domain**: Original CelebA images.

Note: Download CelebA from the official source and organize paths consistent with your environment. The included `train_model.py` assumes a Colab-style layout and Google Drive checkpoints; adjust paths if running locally.

### Installation
Clone the repo:
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate      # Windows (PowerShell/CMD)

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# If you're using the web app or training code, also install:
pip install opencv-python tensorflow keras matplotlib tqdm
```

Alternatively, see quick commands in `command.txt`.

### Usage
#### Run Notebook (training & preprocessing)
All training and preprocessing steps are documented in the notebook:
```bash
open final_notebook.ipynb
```
The `main app/train_model.py` script provides a programmatic training path but is configured with Colab-style paths by default:
```python
# Inside main app/train_model.py
base_path = '/content'
# ... adjust to your local dataset root if not on Colab
```

#### Run Web App
```bash
cd "main app"
python app.py
```
Then open: `http://127.0.0.1:5000/`.

Model weights: place your best checkpoint in `main app/` as `sketch2image_legacy.h5` (the app loads this filename). You can rename your `.h5` or update the path in `app.py`.

### Training Details
- **Architecture**: compact U-Net variant (see `train_model.py`)
- **Input size**: 218×178×3
- **Loss**: MSE (baseline)
- **Checkpoints**: best model saved as `.h5`
- **History**: training history serialized to `.pkl`

Artifacts (by default in the Colab example):
- **Best model**: `sketch2image_best.h5`
- **History**: `sketch2image_training_history.pkl`

### Example Results
Input Sketch ➜ Generated Image (use the web app; outputs saved to `static/uploads/`).

### Future Work
- **Experiment with GAN-based models** for higher realism
- **Add hyperparameter tuning** support
- **Deploy as an online demo app**

### Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to improve.

### License
This project is licensed under the **MIT License**.

### Acknowledgements
- CelebA dataset authors
- OpenCV for preprocessing
- TensorFlow/Keras for model training 
