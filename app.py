#importing the important libraries
from keras.models import load_model
import streamlit as st
import pandas as pd
import sklearn.preprocessing

#Writing the to-do's and basic info about the app
st.image('i.jpg')
st.title("COVID 19 ICU Admission Prediction")
st.write("Based on the various medical parametres available, it is feasible to predict which patients will need intensive care unit support"
       "The aim is to provide tertiary and quarternary hospitals with the most accurate answer, "
        "so ICU resources can be arranged or patient transfer can be scheduled.")
st.write("Provide us with your accurate medical details and let us handle the rest!")
st.write("Please provide the latest values of the following medical parameters.")

#Taking input from the user
st.header("Enter your name :")
name = st.text_input("")

st.header("Is your age above 65 ?")
AGE_ABOVE_65 = st.radio("",("Yes", "No"))
if(AGE_ABOVE_65=="Yes"):
    AGE_ABOVE_65=1.0
    AGE_ABOVE_65 = float(AGE_ABOVE_65)
else:
    AGE_ABOVE_65=0.0
    AGE_ABOVE_65 = float(AGE_ABOVE_65)

st.header("Enter your gender :")
GENDER = st.radio("", ("Male","Female"))
if(GENDER=="Male"):
    GENDER=1.0
    GENDER = float(GENDER)
else:
    GENDER=0.0
    GENDER = float(GENDER)

st.header("Do you have any of the following diseases ?")
disease_grouping = st.selectbox("",("None", "Diabetes", "Blood Pressure", "Fever/Cough", "Allergy of any kind", "Asthma", "You Smoke"))
if(disease_grouping=="None"):
    DISEASEGROUPING_1=0.0
    DISEASEGROUPING_2=0.0
    DISEASEGROUPING_3=0.0
    DISEASEGROUPING_4=0.0
    DISEASEGROUPING_5=0.0
    DISEASEGROUPING_6=0.0
elif(disease_grouping=="Diabetes"):
    DISEASEGROUPING_1 = 1.0
    DISEASEGROUPING_2 = 0.0
    DISEASEGROUPING_3 = 0.0
    DISEASEGROUPING_4 = 0.0
    DISEASEGROUPING_5 = 0.0
    DISEASEGROUPING_6 = 0.0
elif(disease_grouping=="Blood Pressure"):
    DISEASEGROUPING_1 = 0.0
    DISEASEGROUPING_2 = 1.0
    DISEASEGROUPING_3 = 0.0
    DISEASEGROUPING_4 = 0.0
    DISEASEGROUPING_5 = 0.0
    DISEASEGROUPING_6 = 0.0
elif(disease_grouping=="Fever/Cough"):
    DISEASEGROUPING_1 = 0.0
    DISEASEGROUPING_2 = 0.0
    DISEASEGROUPING_3 = 1.0
    DISEASEGROUPING_4 = 0.0
    DISEASEGROUPING_5 = 0.0
    DISEASEGROUPING_6 = 0.0
elif(disease_grouping=="Allergy of any kind"):
    DISEASEGROUPING_1 = 0.0
    DISEASEGROUPING_2 = 0.0
    DISEASEGROUPING_3 = 0.0
    DISEASEGROUPING_4 = 1.0
    DISEASEGROUPING_5 = 0.0
    DISEASEGROUPING_6 = 0.0
elif(disease_grouping=="Asthma"):
    DISEASEGROUPING_1 = 0.0
    DISEASEGROUPING_2 = 0.0
    DISEASEGROUPING_3 = 0.0
    DISEASEGROUPING_4 = 0.0
    DISEASEGROUPING_5 = 1.0
    DISEASEGROUPING_6 = 0.0
elif(disease_grouping=="You Smoke"):
    DISEASEGROUPING_1 = 0.0
    DISEASEGROUPING_2 = 0.0
    DISEASEGROUPING_3 = 0.0
    DISEASEGROUPING_4 = 0.0
    DISEASEGROUPING_5 = 0.0
    DISEASEGROUPING_6 = 1.0

st.header("Enter your Glucose Level :")
GLUCOSE_MEDIAN = st.slider("",100,400,175)
GLUCOSE_MEDIAN = float(GLUCOSE_MEDIAN)


st.header("Enter your Systolic blood Pressure :")
BLOODPRESSURE_SISTOLIC_MEDIAN = st.slider("",50,200,120)
BLOODPRESSURE_SISTOLIC_MEDIAN = float(BLOODPRESSURE_SISTOLIC_MEDIAN)

st.header("Enter your Diastolic blood Pressure :")
BLOODPRESSURE_DIASTOLIC_MEDIAN = st.slider("",30,200,80)
BLOODPRESSURE_DIASTOLIC_MEDIAN = float(BLOODPRESSURE_DIASTOLIC_MEDIAN)

st.header("Enter your Heart Rate :")
HEART_RATE_MEDIAN = st.slider("",50,400,120)
HEART_RATE_MEDIAN = float(HEART_RATE_MEDIAN)

st.header("Enter your Respiratory Rate :")
RESPIRATORY_RATE_MEDIAN = st.slider("",10,50,25)
RESPIRATORY_RATE_MEDIAN = float(RESPIRATORY_RATE_MEDIAN)

st.header("Enter your Body Temperature :")
TEMPERATURE_MEDIAN = st.slider("",30,50,37)
TEMPERATURE_MEDIAN = float(TEMPERATURE_MEDIAN)

st.header("Enter your SpO2 Level :")
OXYGEN_SATURATION_MEDIAN = st.slider("",1,100,50)
OXYGEN_SATURATION_MEDIAN = float(OXYGEN_SATURATION_MEDIAN)

st.header("How long has it been, since you are admitted to the hospital ?")
WINDOW = st.selectbox("", ("0-2 hours",
"2-4 hours",
"4-6 hours",
"6-12 hours",
"Above 12 hours"))
if(WINDOW=="0-2 hours"):
    WINDOW = 1.0
elif(WINDOW=="2-4 hours"):
    WINDOW = 2.0
elif(WINDOW=="4-6 hours"):
    WINDOW = 3.0
elif(WINDOW=="6-12 hours"):
    WINDOW = 4.0
elif(WINDOW=="Above 12 hours"):
    WINDOW = 5.0
WINDOW = float(WINDOW)

#ASking the user to upload the medical documents
st.header("Please upload the following files for Hospital Use :")
st.write("Please upload your Blood Test Report :")
st.set_option('deprecation.showfileUploaderEncoding', False)
blood_report = st.file_uploader("",type=['pdf','docx'])
st.write("Please upload your COVID19-POSITIVE Report :")
covid_report = st.file_uploader(" ",type=['pdf','docx'])

#Adjusting the scale of the input values as the model was trained on scaled values
X = [AGE_ABOVE_65, GENDER, DISEASEGROUPING_1, DISEASEGROUPING_2, DISEASEGROUPING_3, DISEASEGROUPING_4, DISEASEGROUPING_5
     ,DISEASEGROUPING_6, GLUCOSE_MEDIAN, BLOODPRESSURE_DIASTOLIC_MEDIAN, BLOODPRESSURE_SISTOLIC_MEDIAN, HEART_RATE_MEDIAN
     ,RESPIRATORY_RATE_MEDIAN, TEMPERATURE_MEDIAN, OXYGEN_SATURATION_MEDIAN, WINDOW]
AGE_ABOVE_65 = (((AGE_ABOVE_65 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
GENDER = (((GENDER - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
DISEASEGROUPING_6= (((DISEASEGROUPING_6 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
DISEASEGROUPING_5= (((DISEASEGROUPING_5 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
DISEASEGROUPING_4= (((DISEASEGROUPING_4 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
DISEASEGROUPING_3= (((DISEASEGROUPING_3 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
DISEASEGROUPING_2= (((DISEASEGROUPING_2 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
DISEASEGROUPING_1= (((DISEASEGROUPING_1 - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
GLUCOSE_MEDIAN= (((GLUCOSE_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
BLOODPRESSURE_SISTOLIC_MEDIAN= (((BLOODPRESSURE_SISTOLIC_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
BLOODPRESSURE_DIASTOLIC_MEDIAN= (((BLOODPRESSURE_DIASTOLIC_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
HEART_RATE_MEDIAN= (((HEART_RATE_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
RESPIRATORY_RATE_MEDIAN= (((RESPIRATORY_RATE_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
TEMPERATURE_MEDIAN= (((TEMPERATURE_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
OXYGEN_SATURATION_MEDIAN= (((OXYGEN_SATURATION_MEDIAN - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)
WINDOW= (((WINDOW - min(X))/(max(X) - min(X))) * (1 - (-1))) + (-1)

#Using the average values of the following parametres as these are available only after testing
HTN  = 0.23
IMMUNOCOMPROMISED = 0.18
OTHER  = 0.83
ALBUMIN_MEDIAN = 0.53
BE_ARTERIAL_MEDIAN  = -0.95
BE_VENOUS_MEDIAN = -0.92
BIC_ARTERIAL_MEDIAN = -0.303
BIC_VENOUS_MEDIAN = -0.303
BILLIRUBIN_MEDIAN = -0.93
BLAST_MEDIAN = -0.98
CALCIUM_MEDIAN = 0.33
CREATININ_MEDIAN = -0.88
FFA_MEDIAN = -0.71
GGT_MEDIAN = -0.9
HEMATOCRITE_MEDIAN = -0.14
HEMOGLOBIN_MEDIAN = -0.18
INR_MEDIAN = -0.92
LACTATE_MEDIAN = 0.28
LEUKOCYTES_MEDIAN = -0.72
LINFOCITOS_MEDIAN = -0.69
NEUTROPHILES_MEDIAN = -0.79
P02_ARTERIAL_MEDIAN = -0.16
P02_VENOUS_MEDIAN = -0.65
PC02_ARTERIAL_MEDIAN = -0.76
PC02_VENOUS_MEDIAN = -0.73
PCR_MEDIAN = -0.82
PH_ARTERIAL_MEDIAN = 0.25
PH_VENOUS_MEDIAN = 0.38
PLATELETS_MEDIAN = -0.39
POTASSIUM_MEDIAN = -0.505
SAT02_ARTERIAL_MEDIAN = 0.93
SAT02_VENOUS_MEDIAN = 0.35
SODIUM_MEDIAN = -0.03
TGO_MEDIAN = -0.96
TGP_MEDIAN = -0.95
TTPA_MEDIAN = -0.79
UREA_MEDIAN = -0.806
DIMER_MEDIAN = -0.92

#Loading the best saved model
model = load_model("model-147.model")

#Using the model to predict the answer
prediction = model.predict([[
AGE_ABOVE_65,
GENDER,
DISEASEGROUPING_1,
DISEASEGROUPING_2,
DISEASEGROUPING_3,
DISEASEGROUPING_4,
DISEASEGROUPING_5,
DISEASEGROUPING_6,
HTN,
IMMUNOCOMPROMISED,
OTHER,
ALBUMIN_MEDIAN,
BE_ARTERIAL_MEDIAN,
BE_VENOUS_MEDIAN,
BIC_ARTERIAL_MEDIAN,
BIC_VENOUS_MEDIAN,
BILLIRUBIN_MEDIAN,
BLAST_MEDIAN,
CALCIUM_MEDIAN,
CREATININ_MEDIAN,
FFA_MEDIAN,
GGT_MEDIAN,
GLUCOSE_MEDIAN,
HEMATOCRITE_MEDIAN,
HEMOGLOBIN_MEDIAN,
INR_MEDIAN,
LACTATE_MEDIAN,
LEUKOCYTES_MEDIAN,
LINFOCITOS_MEDIAN,
NEUTROPHILES_MEDIAN,
P02_ARTERIAL_MEDIAN,
P02_VENOUS_MEDIAN,
PC02_ARTERIAL_MEDIAN,
PC02_VENOUS_MEDIAN,
PCR_MEDIAN,
PH_ARTERIAL_MEDIAN,
PH_VENOUS_MEDIAN,
PLATELETS_MEDIAN,
POTASSIUM_MEDIAN,
SAT02_ARTERIAL_MEDIAN,
SAT02_VENOUS_MEDIAN,
SODIUM_MEDIAN,
TGO_MEDIAN,
TGP_MEDIAN,
TTPA_MEDIAN,
UREA_MEDIAN,
DIMER_MEDIAN,
BLOODPRESSURE_DIASTOLIC_MEDIAN,
BLOODPRESSURE_SISTOLIC_MEDIAN,
HEART_RATE_MEDIAN,
RESPIRATORY_RATE_MEDIAN,
TEMPERATURE_MEDIAN,
OXYGEN_SATURATION_MEDIAN,
WINDOW
]])
prediction = (prediction > 0.5)

#Deployment of a button trigger
if st.button('Get my info'):
    if(prediction == 0):
        st.header("According to the above data, you are NOT SUPPOSED TO BE ADMITTED in an ICU.")
        st.header("Please do take a proper consultation from your doctor.")
        st.header("Follow the safety protocols for COVID19 as advised by Central Government.")
    elif(prediction == 1):
        st.header("According to the above data, you are SUPPOSED TO BE ADMITTED in an ICU.")
        st.header("You are advised to consult your doctor IMMEDIATELY.")
        st.header("Follow the safety protocols for COVID19 as advised by Central Government.")

st.text("© Kartik Tripathi | Uday Dasari | Shreay Mittal")
st.text("2021")
