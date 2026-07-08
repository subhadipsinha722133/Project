import streamlit as st 
import pickle
st.title("Lung Cancer Prediction")
st.write("Made By Subhadip")

model=pickle.load(open("model.pkl","rb"))

age = st.slider("Age", 0, 90, 5)
depth = st.slider("Depth", 0, 80, 60)


Gender_dict = {"Male":1,"Female":2}
quality = st.selectbox("Choose Quality", list(Gender_dict.keys()))
Gender_val = Gender_dict[quality]


Air_Pollution_dict = {"Good":1,"Satisfactory":2," Moderate":3,"Poor":4,"Very Poor":5," Severe":6," Unhealthy":7,"Very Unhealthy":8}
air = st.selectbox("Air Pollution", list(Air_Pollution_dict.keys()))
Air_Pollution_val = Air_Pollution_dict[air]


alcohol_dict = {"Initiation Stage":1,"Regular or Social Use Stage":2,"Early-Stage Dependence":3,"Problematic or Risky Use Stage":4,"Crisis or \"Hitting Bottom\" Stage":5,"Middle-Stage Dependence":6,"Late-Stage Dependence (Addiction)":7,"Recovery and Rehabilitation Stage":8,"Not Use":0}
alcohol = st.selectbox("Alcohol use", list(alcohol_dict.keys()))
alcohol_use_val = alcohol_dict[alcohol]




Genetic_Risk_dict = {"No Genetic Risk":0,"Increased Risk Due to Family History":2,"Suspected Genetic Condition (Pre-Testing)":3,"Identification of a Genetic Variant":4,"Confirmed Hereditary Risk (High-Risk Stratification)":5,"Clinical Manifestation (Symptomatic Stage)":6,"Proactive Management and Surveillance":7}
Genetic_Risk = st.selectbox("Genetic Risk", list(Genetic_Risk_dict.keys()))
Genetic_Risk_val = Genetic_Risk_dict[Genetic_Risk]



chronic__Lung_Disease_dict = {"No chronic Lung Disease ":0,"At-Risk (Pre-Disease Stage)":1,"Mild or Early-Stage Disease (GOLD 1 for COPD)":2,"Moderate Disease with Persistent Symptoms (GOLD 2 for COPD)":3,"Severe Disease with Lifestyle Limitation (GOLD 3 for COPD)":4,"Very Severe Disease with Respiratory Compromise (GOLD 4 for COPD)":5,"Advanced Disease with Complications (Respiratory Failure)":6,"End-Stage Disease (Palliative Care)":7}
chroni_cLung_Disease = st.selectbox("chronic Lung Disease", list(chronic__Lung_Disease_dict.keys()))
chronic_Lung_Disease_val = chronic__Lung_Disease_dict[chroni_cLung_Disease]


Smoking_dict = {"Initiation Stage":1,"Regular or Social Use Stage":2,"Early-Stage Dependence":3,"Problematic or Risky Use Stage":4,"Crisis or \"Hitting Bottom\" Stage":5,"Middle-Stage Dependence":6,"Late-Stage Dependence (Addiction)":7,"Recovery and Rehabilitation Stage":8,"Not Use":0}
Smoking = st.selectbox("Smoking", list(Smoking_dict.keys()))
Smoking_val = Smoking_dict[Smoking]
