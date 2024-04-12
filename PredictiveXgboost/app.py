import streamlit as st
from streamlit.components.v1 import components
import numpy as np
import xgboost as xgb
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib
import pickle

# Load stroke model
with open('xgb_classifier_model.pkl', 'rb') as model_file1:
    loaded_xgb_model_stroke = pickle.load(model_file1)

# Load heart attack model
with open('xgb_classifier_model_heart.pkl', 'rb') as model_file2:
    loaded_xgb_model_heart = pickle.load(model_file2)

model = tf.keras.models.load_model('diabetes-rbf.h5')

# Load the scaler
scaler = joblib.load('scaler_model1.joblib')

# Load the scaler
scaler1 = joblib.load('scaler_heart4.joblib')

# Load the scaler
scaler2 = joblib.load('scaler_stroke.joblib')

# Define the layout of the web application
st.title("Health Risk Prediction")

# Create buttons to navigate between pages
page = st.sidebar.selectbox("Select a Model", ["Heart Attack", "Stroke","Diabetes"])

if page == "Heart Attack":
    # Define the layout of the web application
    st.title("Heart Attack Risk Prediction")
    st.markdown("Enter the following information to predict your risk of a Heart Attack.")

    # Define the user input fields
    sex = st.selectbox("Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain", ["Typical Angina", "Atypical Angina", "Non-Anginal pain", "Asymptomatic"])
    Max_heartrate_achieved = st.number_input("Maximum Heartrate Achieved ")
    Exercice_angina = st.selectbox("Exercise Induced Angina", ["Yes", "No"])
    old_peak= st.number_input("Old Peak")
    slop = st.selectbox("Slope of the peak exercise ST segment", ["Unsloping", "flat", "Downsloping"])
    nb_vessels = st.selectbox("Number of major vessels", ["0", "1", "2", "3"])
    thal = st.selectbox("Thalassemia", ["Null", "Fixed defect", "Normal", "Reversible defect"])

    # Initialize prediction variable
    prediction = None

    # Define the predict button
    if st.button("Predict"):
        # Preprocess the user input
        sex = 1 if sex == "Male" else 0
        chest_pain = 0 if chest_pain == "Typical Angina" else 1 if chest_pain == "Atypical Angina" else 2 if chest_pain == "Non-Anginal pain" else 3
        Exercice_angina = 1 if Exercice_angina == "Yes" else 0
        slop = 0 if slop == "Unsloping" else 1 if slop == "flat" else 2 if slop == "Downsloping" else 0
        nb_vessels = 0 if nb_vessels == "0" else 1 if nb_vessels == "1" else 2 if nb_vessels == "2" else 3
        thal = 0 if thal == "Null" else 1 if thal == "Fixed defect" else 2 if thal == "Normal" else 3 if thal == "Reversible defect" else 0

        input_data = np.array([[sex, chest_pain, Max_heartrate_achieved, Exercice_angina, old_peak, slop, nb_vessels, thal]])
        #scaled_input1 = scaler1.transform(input_data)
        #dmatrix = xgb.DMatrix(scaled_input1)

        # Make a prediction on the user input
        prediction = loaded_xgb_model_heart.predict(input_data)

        # Display the prediction to the user
        if prediction is not None:
           if prediction == 0:
              st.markdown("### Result: **Low Risk** of a Heart Attack")
           else:
              st.markdown("### Result: **High Risk** of a Heart Attack")

elif page == "Stroke":
    # Define the layout of the web application
    st.title("Stroke Risk Prediction")
    st.markdown("Enter the following information to predict your risk of a Stroke.")

    # Define the user input fields
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    hypertension = st.selectbox("Hypertension", ["Yes", "No"])
    Heart_disease = st.selectbox("Heart_disease", ["Yes", "No"])
    ever_married = st.selectbox("Ever_married", ["Yes", "No"])
    avg_glucose_level = st.number_input("avg_glucose_level")

    # Define the predict button
    if st.button("Predict"):
        # Preprocess the user input
        hypertension = 1 if hypertension == "Yes" else 0
        Heart_disease = 1 if Heart_disease == "Yes" else 0
        ever_married = 1 if ever_married == "Yes" else 0
        input_data = np.array([[age, hypertension, Heart_disease, ever_married, avg_glucose_level]])
        #scaled_input1 = scaler2.transform(input_data)

        # Wrap the input data in a DMatrix for prediction
        #dmatrix = xgb.DMatrix(scaled_input1)

        # Make a prediction on the user input
        prediction =loaded_xgb_model_stroke.predict(input_data)

        # Display the prediction to the user
        if prediction == 0:
            st.markdown("### Result: **Low Risk** of a Stroke")
        else:
            st.markdown("### Result: **High Risk** of a Stroke")
elif page == "Diabetes":      
    # Force eager execution
    tf.config.run_functions_eagerly(True)
    
    # Define the layout of the web application
    st.title("Diabetes Risk Prediction")
    st.markdown("Enter the following information to predict your risk of having Diabetes.")
    
    # Define the user input fields
    Age = st.number_input("Age")
    hypertension = st.selectbox("hypertension", ["Yes", "No"])
    heartdisease = st.selectbox("heartdisease", ["Yes", "No"])
    bmi = st.number_input("BMI")
    hba1c = st.number_input("HBA1C_level")
    glucose = st.number_input("Blood_Glucose_Level")
    
    # Initialize prediction variable
    prediction = None
    
    if st.button("Predict"):
        hypertension = 1 if hypertension == "Yes" else 0
        heartdisease = 1 if heartdisease == "Yes" else 0
        # Create input array for the model
        input_data = np.array([[Age, hypertension, heartdisease, bmi, hba1c, glucose]])
        scaled_input = scaler.transform(input_data)
        
        # Make a prediction on the user input
        prediction_prob = model.predict(scaled_input) # Probability for class 1 (High Risk)
        
        # Set a threshold for binary prediction (adjust as needed)
        threshold = 0.5
        prediction = (prediction_prob[:, 1] > threshold).astype(int)
    
    # Display the prediction to the user
    if prediction is not None:
        if prediction == 0:
            st.markdown("### Result: **Low Risk** of having Diabetes")
        else:
            st.markdown("### Result: **High Risk** of having Diabetes")
