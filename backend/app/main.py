from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import pickle
import io
from sklearn.neighbors import NearestNeighbors
import keras
import logging
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print("Keras version:", keras.__version__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for communication with React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Load models and embeddings
models = {
    "resnet": pickle.load(open("app/models/resnet.pkl", "rb")),
    # "vgg": pickle.load(open("app/models/vgg.pkl", "rb")),
    "effnet": pickle.load(open("app/models/effnet.pkl", "rb")),
    # Add other models here
}
feature_list = np.load("app/embeddings/res.npy")
image_paths = pickle.load(open("app/embeddings/image_paths.pkl", "rb"))
nn_model = pickle.load(open("app/models/nearest_neighbors.pkl", "rb"))

def preprocess(image):
    # Implement preprocessing based on your model's requirements
    image = image.resize((224, 224))  # Example resizing for ResNet
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.post("/search/")
async def search_image(
    file: UploadFile = File(...),
    model_name: str = Form(...)
):
    logger.info("Search endpoint hit!")
    # Load and preprocess the image
    img = Image.open(io.BytesIO(await file.read())).convert("RGB")
    img = preprocess(img)

    # Extract features
    model = models[model_name]
    features = model.predict(img, batch_size=1).reshape(1, -1)

    similar_images = []
    # Find nearest neighbors
    distances, indices = nn_model.kneighbors(features, n_neighbors=5)
    for idx in indices[0]:
        print(idx)
        similar_images.append("101_ObjectCategories/" + image_paths[idx])

    # similar_images = [image_paths[idx] for idx in indices[0]]
    print(similar_images)

    return {"similar_images": similar_images}
