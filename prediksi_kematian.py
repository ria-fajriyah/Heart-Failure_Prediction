import pickle
import streamlit as st
import pandas as pd 

st.title("Prediksi Kematian Pasien Penderita Penyakit Kardiovaskular")

# Membagi visualisasi menjadi 3 kolom
col1, col2, col3 = st.columns(3)

def user_input_features():
    with col1:
        age = st.number_input('enter your age')
    with col2:
        sex = st.selectbox('sex (0=Female, 1=Male)', (0,1))
    with col3:
        smoking = st.selectbox('do you smoking? (0=No, 1=Yes)', (0,1))    
    with col1:
        anaemia = st.selectbox('do you have anaemia? (0=No, 1=Yes)', (0,1))
    with col2:
        diabetes = st.selectbox('do you have diabetes? (0=No, 1=Yes)', (0,1))
    with col3:
        high_blood = st.selectbox('do you have high blood pressure (0=No, 1=Yes)', (0,1))
    with col1:
        cpk = st.number_input('CPK enzyme level (mcg/L)')
    with col2:
        creatinine = st.number_input('serum creatinine level in blood (mg/dL)')
    with col3:
        platelets = st.number_input('platelets in the blood (kiloplatelets/mL)')
  
    data = {'age':age,
            'sex':sex,
            'smoking':smoking,
            'anaemia':anaemia,
            'diabetes':diabetes,
            'high_blood_pressure':high_blood,
            'creatinine_phosphokinase':cpk,
            'serum_creatinine':creatinine,
            'platelets':platelets
           }   
    features = pd.DataFrame(data, index=[0])
    return features                              
input_df = user_input_features()

heart_dataset = pd.read_csv('heart_failure_clinical_records_dataset.csv')
heart_dataset = heart_dataset.drop(columns=['DEATH_EVENT'])
                                                       
df = pd.concat([input_df, heart_dataset], axis=0)                                    

# encode fitur                                   
df = pd.get_dummies(df, columns=['sex', 'smoking', 'anaemia', 'diabetes', 'high_blood_pressure'])  

# mengambil hanya baris pertama pada user input data                                   
df = df[:]                                   
                                   
st.write(input_df)

model = pickle.load(open('prediksi_kematian.sav', 'rb'))
predict = ''                             
if st.button("Prediksi Kematian Pasien"):
    predict = model.predict(data)
    if(predict[0]==1):
        death_predict = 'Pasien sudah meninggal sebelum waktu follow-up'
    else:
        death_predict = 'Pasien masih bertahan pada waktu follow-up'
    
    st.success(death_predict)
