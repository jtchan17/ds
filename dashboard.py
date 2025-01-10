import pandas as pd
import streamlit as st
import plotly.express as px
import json

st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide")

#load dataset
@st.cache_data
def load_data():
    with open("Data Science Salary 2021 to 2023.json", "r") as json_file:
        financialnews_data = json.load(json_file)
    return financialnews_data

df_salary = load_data()
df_salary = pd.DataFrame(df_salary)

st.title('🌟 :rainbow[DataPay Insights]')

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
    