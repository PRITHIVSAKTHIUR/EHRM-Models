import streamlit as st
import gradio as gr
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image

# Loading Models
braintumor_model = load_model('models/brain_tumor_binary.h5')

# Configuring Streamlit
st.set_page_config(
    page_title="Brain Tumor Prediction App",
    page_icon=":brain:",
    layout="centered",
)

# Streamlit app title and description
st.title("Brain Tumor Prediction App")
st.write(
    "Upload an image, and the app will predict whether a brain tumor is present or not."
)

# Add Streamlit sidebar for additional information or options
st.sidebar.title("About")
st.sidebar.info(
    "This app uses a trained model to predict brain tumors from images. "
    "The model is based on VGG16 architecture."
)

# Function to preprocess the image
def preprocess_image(img):
    # If it's a NumPy array, use it directly
    if isinstance(img, np.ndarray):
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        # Convert Gradio image data to bytes
        img_bytes = img.read()

        # Convert to NumPy array
        nparr = np.frombuffer(img_bytes, np.uint8)

        # Decode image
        img_gray = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # Crop and preprocess the grayscale image
    img_processed = preprocess_imgs([img_gray], (224, 224))

    return img_processed

# Handle binary decision
def binary_decision(confidence):
    return 1 if confidence >= 0.5 else 0

def predict_braintumor(img):
    # Preprocess the image
    img_processed = preprocess_image(img)

    # Make prediction
    pred = braintumor_model.predict(img_processed)

    # Handle binary decision
    confidence = pred[0][0]
    return "Brain Tumor Not Found!" if binary_decision(confidence) == 1 else "Brain Tumor Found!"

def preprocess_imgs(set_name, img_size):
    set_new = []
    for img in set_name:
        img = cv2.resize(img, dsize=img_size, interpolation=cv2.INTER_CUBIC)
        set_new.append(preprocess_input(img))
    return np.array(set_new)

def crop_imgs(set_name, add_pixels_value=0):
    set_new = []
    for img in set_name:
        gray = cv2.GaussianBlur(img, (5, 5), 0)
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        c = max(cnts, key=cv2.contourArea)
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        ADD_PIXELS = add_pixels_value
        new_img = img[extTop[1] - ADD_PIXELS:extBot[1] + ADD_PIXELS,
                      extLeft[0] - ADD_PIXELS:extRight[0] + ADD_PIXELS].copy()
        set_new.append(new_img)
    return np.array(set_new)

# Gradio interface
iface = gr.Interface(
    fn=predict_braintumor,
    inputs="image",
    outputs="text",
    examples=[["examples/1_no.jpeg"], ["examples/2_no.jpeg"], ["examples/3_no.jpg"], ["examples/Y1.jpg"], ["examples/Y2.jpg"], ["examples/Y3.jpg"]],
    live=True  # Allows real-time updates without restarting the app
)

# Display Gradio interface
iface.launch()

# Streamlit components below the Gradio interface
uploaded_file = st.file_uploader("Choose an MRI image", type=["jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded MRI Image.", use_column_width=True)
    
    # Perform prediction when the "Predict" button is clicked
    if st.button("Predict"):
        # Preprocess the image
        img_array = preprocess_image(uploaded_file)

        # Make prediction
        pred = braintumor_model.predict(img_array)

        # Handle binary decision
        confidence = pred[0][0]
        result = "Brain Tumor Not Found!" if binary_decision(confidence) == 1 else "Brain Tumor Found!"

        # Display the prediction result
        st.write(result)
