import pandas as pd
import streamlit as st
import plotly.express as px
import json
import joblib
import os
import gdown

st.set_page_config(
    page_title="DataPay",
    page_icon="📈",
    layout="wide")

#load dataset
@st.cache_data
def load_data():
    with open("ds_salary_data.json", "r") as json_file:
        financialnews_data = json.load(json_file)
    return financialnews_data

df_salary = load_data()
df_salary = pd.DataFrame(df_salary)

st.title('🌟 :rainbow[DataPay Insights]')
tab1, tab2 = st.tabs(['Dashboard', 'Prediction'])
with tab1:
    r1c1, r1c2, r1c3 = st.columns((2.5, 3, 2), gap='medium')
    with r1c1:
        #Salary Trend over Time
        st.markdown('#### 📈 Salary Trend over Time')
        avg_salary_year = df_salary.groupby('work_year')['salary_in_usd'].mean().reset_index()
        chart_avg_salary = px.line(avg_salary_year, x='work_year', y='salary_in_usd')
        st.plotly_chart(chart_avg_salary)

    with r1c2:
        #Top 10 High-Paying Job Designations
        st.markdown('#### 🏆 Top 10 High-Paying Job')
        xdf=df_salary.groupby(['job_title'])['salary_in_usd'].median().sort_values(ascending=False).head(10)
        # Create the bar chart
        chart_job_title = px.bar(
            x=xdf.index,
            y=xdf,
            # title='Top 10 High-Paying Job Designations',
            labels={'y': 'Median Salary (USD)', 'x': 'Job Designations'},
            text=xdf,  # Add values on top of each bar
            color=xdf,  # Color based on salary values
            color_continuous_scale='Blues'  # Color scheme for a more dynamic look
        )

        # Customize the text on bars
        chart_job_title.update_traces(texttemplate='%{text:.2s}', textposition='outside')

        # Remove grid lines for a cleaner look
        chart_job_title.update_xaxes(showgrid=False)
        chart_job_title.update_yaxes(showgrid=False)

        # Show the figure
        st.plotly_chart(chart_job_title)

    with r1c3:
        st.markdown('#### 💰 Salary Distribution by Experience Level')
        fig = px.box(df_salary, x='experience_level', y='salary_in_usd', color='experience_level')
        st.plotly_chart(fig)

    r2c1, r2c2 = st.columns((6, 3), gap='small')

    with r2c1:
        #Job Title Distribution
        st.markdown('#### 📋 Job Title Distribution')
        # Calculate frequency of each job title
        job_title_counts = df_salary['job_title'].value_counts()

        # Determine titles below the threshold, e.g., less than N occurrences
        N=50
        low_frequency_titles = job_title_counts[job_title_counts < N].index

        # Replace these titles in the dataframe with "Others"
        df_salary['adjusted_job_title'] = df_salary['job_title'].apply(lambda x: "Others" if x in low_frequency_titles else x)

        # Recalculate the frequency
        adjusted_counts = df_salary['adjusted_job_title'].value_counts()

        #Plot
        df_salary1 = df_salary.groupby('adjusted_job_title').size().reset_index(name='Total')
        chart_job_title = px.pie(df_salary1, values='Total', names='adjusted_job_title', color='adjusted_job_title', hole=0.5, template='plotly_dark')
        st.plotly_chart(chart_job_title)

    with r2c2:
        #Top 10 Most Popular Job Designations
        st.markdown('#### 🏅 Top 10 Popular Job')
        #Table form
        df_pop = df_salary.groupby('job_title').size().reset_index(name='Total')
        table_Popular = (df_pop.sort_values(by="Total", ascending=False)).head(10)
        
        df = st.dataframe(table_Popular,
                    column_order=("job_title", "Total"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "job_title": st.column_config.TextColumn("Job Designations",),
                        "Total": st.column_config.ProgressColumn("No. of Posts",format="%f",min_value=0,max_value=max(df_pop.Total),)
                        }
                    )
with tab2:
    col1, col2 = st.columns([1, 5])
    with col1:
        st.subheader('Select Features', divider=True)

        year = [2020, 2021, 2022, 2023]
        year_selection = st.selectbox('Year', options=year, index=0)

        explvl = {
            'Entry-Level':0, 
            'Experienced':1, 
            'Mid-Level':2, 
            'Senior':3
            }

        explvl_selection = st.selectbox('Experience Level', options=list(explvl.keys()), index=0)

        emptype = {
            'Full-Time': 2, 
            'Part-Time': 3, 
            'Contractor': 0,
            'Freelancer': 1
        }
        emptype_selection = st.selectbox('Employment Type', options=list(emptype.keys()), index=0)

        compsize = {
            'Small': 2, 
            'Medium': 1, 
            'Large': 0
        }
        compsize_selection = st.selectbox('Company Size', options=list(compsize.keys()), index=0)

        comploc = {
            'US': 70, 'NG': 53, 'IN': 38, 'CA':12, 'ES':25, 'GH':29, 'DE':20, 'CH':14, 'AU':6, 'SE':63, 'BR':10,
        'GB':28, 'VN': 71, 'BA':7, 'GR':30, 'HK':31, 'NL':54, 'FI':26, 'IE':36, 'SG':64, 'SI':65, 'MX':51,
        'FR':27, 'HR':33, 'AM':2, 'KE':43, 'RO':61, 'TH':67, 'CF':13, 'UA':69, 'IL':37, 'CO':17, 'PT':60,
        'EE':23, 'LV':46, 'MK':49, 'PK':57, 'IT':41, 'MA':47, 'AR':3, 'CR':18, 'IR':40, 'HU':34, 'AS':4,
        'BE':8, 'AT':5, 'ID':35, 'LU':45, 'MY':52, 'CZ':19, 'DZ':22, 'RU':62, 'PL':58, 'LT':44, 'TR':68,
        'BO':9, 'EG':24, 'AL':1, 'SK':66, 'PR':59, 'AE':0, 'DK':21, 'IQ':39, 'CN':16, 'BS':11, 'JP':42,
        'CL':15, 'MD':48, 'MT':50, 'PH':56, 'HN':32, 'NZ':55
        }
        comploc_selection = st.selectbox('Company Location', options=list(comploc.keys()), index=0)

        jobtitle = {
            'Analytics Engineer': 0, 
            'Applied Scientist': 1, 
            'Data Analyst': 2,
            'Data Architect': 3,
            'Data Engineer': 4,
            'Data Science Manager': 5,
            'Data Scientist': 6,
            'Machine Learning Engineer': 7,
            'Research Scientist': 9,
            'Others': 8
        }
        jobtitle_selection = st.selectbox('Job Title', options=list(jobtitle.keys()), index=0)

        sf_col1, sl_col2, sl_col3 = st.columns(3)
        with sl_col2:
            predict_button = st.button('Predict')

    with col2: 
        modelgb_dir = './model'
        modelgb_url = 'https://drive.google.com/drive/folders/175Skml7CqvbfgS14oOctFzx-7go72jak?usp=drive_link'
        st.write('reached here')
        if not os.path.exists(modelgb_dir):
            gdown.download_folder(modelgb_url, output=modelgb_dir)

        @st.cache_resource
        def load_model():
            model = joblib.load(modelgb_dir) 
            return model
        
        user_input = {
            'company_location': comploc[comploc_selection],
            'company_size': compsize[compsize_selection],
            'work_year': year_selection,
            'experience_level': explvl[explvl_selection],
            'employment_type': emptype[emptype_selection],
            'adjusted_job_title': jobtitle[jobtitle_selection]
        }

        st.subheader('Prediction', divider=True)

        if predict_button:
            with st.container(border=True):
                model_gb = load_model()
                predicted_salary = model_gb.predict(user_input)
                st.write(f'The predicted salary for {jobtitle_selection} with {explvl_selection} is')
                st.write(f'USD ${predicted_salary[0]:,.2f}')
        else:
            st.write('Please select your desired features and click on \'Predict\' button.')