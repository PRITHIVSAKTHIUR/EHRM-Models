import numpy as np
import pickle
import streamlit as st

# loading the saved model
loaded_model = pickle.load(open('medical_insurance_model.sav', 'rb'))


def insurance_prediction(input_data):
    # changing input_data to a numpy array
    input_data_as_numpy_array = np.asarray(input_data)
    # reshape the array
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return float(prediction[0])


def main():
    st.title('Medical Insurance Cost Prediction')
    st.markdown(
        'This app predicts the **Medical Insurance Cost** based on the input parameters')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("What is your Age",
                              min_value=0, max_value=100, step=1)
        gender = st.radio("What is your Gender", ('Male', 'Female'))

    with col2:
        bmi = st.number_input("What is your BMI",
                              min_value=0.0, max_value=100.0, step=0.1)
        children = st.number_input(
            "How many Children do you have", min_value=0, max_value=10, step=1)

    with col3:
        smoker = st.radio("Do you Smoke", ('No', 'Yes'))
        region = st.radio("What is your Region", ('Southwest',
                          'Southeast', 'Northwest', 'Northeast'))

    # Convert inputs to appropriate formats
    age = int(age)
    bmi = float(bmi)
    children = int(children)

    # encoding gender, smoker, region
    gender = 0 if gender == 'Male' else 1
    smoker = 0 if smoker == 'Yes' else 1

    if region == 'Southwest':
        region = 1
    elif region == 'Southeast':
        region = 0
    elif region == 'Northwest':
        region = 3
    else:  # 'Northeast'
        region = 2

    # Calculate Insurance Button
    if st.button("Calculate Insurance"):
        predicted_value = insurance_prediction(
            [age, gender, bmi, children, smoker, region])
        st.write('The Insurance Cost is ', predicted_value)


if __name__ == '__main__':
    main()
