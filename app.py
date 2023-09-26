import streamlit as st
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from scipy.stats import poisson




def fetch_sorted_results(data, position: str, metric:str):
    position_df = data[data['position'] == position]
    sorted_df = position_df.sort_values(by=metric, ascending=False)
    final_df = sorted_df[['playerName', 'teamName', metric, 'minutesPlayed']]
    return final_df


def get_scores():
    ''' Display results'''
    ### Translate Position
    if position == 'Goalkeeper':
        position_app = 'G'
    if position == 'Defender':
        position_app = 'D'
    if position == 'Midfielder':
        position_app = 'M'
    if position == 'Forward':
        position_app = 'F'
    ### Translate Metric
    if metric == 'Goals Scored':
        metric_app = 'goalsScored'
    if metric == 'Shots on Target':
        metric_app = 'shotsOnTarget'
    if metric == 'Assists':
        metric_app = 'goalsAssisted'
    if metric == 'Yellow Cards':
        metric_app = 'totalYellowCards'
    if metric == 'Red Cards':
        metric_app = 'totalRedCards'
    if metric == 'Offsides':
        metric_app = 'offsides'
    if metric == 'Accurate Passes':
        metric_app = 'AccuratePasses'
    
    user_data = fetch_sorted_results(app_data, position_app, metric_app)
    return user_data


left_co, cent_co,last_co = st.columns(3)
with last_co:
    st.image('https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/420px-Premier_League_Logo.svg.png')


#image = 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/420px-Premier_League_Logo.svg.png'
### Initial layout
#st.image(image, width=200)
st.header('English Premier League Player Performance')
position = st.sidebar.selectbox('Select Position', ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'])

metric = st.sidebar.selectbox('Select Metric', ['Goals Scored', 'Shots on Target', 'Assists', 'Accurate Passes', 'Yellow Cards', 'Red Cards', 'Offsides'])

button = st.sidebar.button('Fetch Results')

# Data Functionality

data = pd.read_excel('for_app_test.xlsx')
app_data = data[['playerName', 'position', 'teamName', 'minutesPlayed', 'starter', 'goalsScored', 'goalsAssisted', 'shotsOnTarget', 'AccuratePasses', 'passAccuracy', 'totalYellowCards', 'totalRedCards', 'offsides']]
app_data.fillna(0, inplace=True)
#app_data_final = app_data.to_dict("records")
# Convert relevant columns to integers
app_data['goalsScored'] = app_data['goalsScored'].astype(int)
app_data['minutesPlayed'] = app_data['minutesPlayed'].astype(int)
app_data['passAccuracy'] = app_data['passAccuracy'].astype(int)

if button:
    data = get_scores()
    st.dataframe(data)
    #st.line_chart(data.minutesPlayed)