import os
import streamlit as st
from tensorflow.keras.models import load_model
import gdown  # For Google Drive download

# Define model path and download URL
model_path = "model.keras"
download_url = "https://drive.google.com/file/d/1lWxuqm2zDEfQwD4PJ-B2AqERuUoxITha/view?usp=sharing"

# Download the model if not already present
if not os.path.exists(model_path):
    with st.spinner("Downloading model... This may take a few minutes."):
        gdown.download(download_url, model_path, quiet=False)

# Load the model
model = load_model(model_path)


# Define class labels
class_labels = [
    'Bharatanatyam', 
    'Kathak', 
    'Odissi', 
    'Kuchipudi', 
    'Mohiniyattam', 
    'Manipuri', 
    'Sattriya', 
    'Kathakali'
]

# Streamlit app
st.title("Indian Dance Form Predictor")
st.write("Upload an image to predict the dance form.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join("temp_image.jpg")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load and preprocess the image
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict the class
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]
    
    # Display the prediction
    st.image(file_path, caption="Uploaded Image", use_column_width=True)
    st.write(f"**Predicted Dance Form:** {predicted_class}")
    
    # Optionally, provide descriptions for the dance forms
    descriptions = {
        'Bharatanatyam': 'Bharatanatyam is a classical dance form originating from Tamil Nadu, characterized by intricate footwork and expressive hand gestures.',
        'Kathak': 'Kathak is a North Indian classical dance that emphasizes storytelling through intricate footwork and spins.',
        'Odissi': 'Odissi is one of the oldest classical dance forms from Odisha, known for its grace and fluid movements.',
        'Kuchipudi': 'Kuchipudi is a dance-drama performance from Andhra Pradesh, featuring vibrant storytelling and expressive dance.',
        'Mohiniyattam': 'Mohiniyattam is a classical dance form from Kerala, characterized by graceful movements and feminine expressions.',
        'Manipuri': 'Manipuri is a classical dance form from Manipur, known for its graceful gestures and stylized movements.',
        'Sattriya': 'Sattriya is a classical dance form from Assam, rooted in the traditions of Vaishnavism and characterized by spiritual themes.',
        'Kathakali': 'Kathakali is a highly stylized classical dance-drama from Kerala, known for its elaborate costumes, intricate makeup, and expressive storytelling.'
    }
    st.write(f"**Description:** {descriptions.get(predicted_class, 'No description available.')}")
