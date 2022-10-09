import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title = 'Survey Results',
                    page_icon = ':bar_chart:',
                    layout = 'wide'
)

# ------ Load Dataframe ------
@st.cache
def get_data_main():
    df = pd.read_excel(
        io = "Survey_Results.xlsx",
        engine = "openpyxl",
        skiprows = 3,
        usecols = "B:D"
    )
    return df

def get_data_participants():
    df = pd.read_excel(
        io = "Survey_Results.xlsx",
        engine = "openpyxl",
        skiprows = 3,
        usecols = "F:G",
        nrows = 5
    )
    return df

df = get_data_main()
df_participants = get_data_participants()

st.markdown("<h1 style = 'text-align: center; color: red;'> Survey Results 2021 </h1>", unsafe_allow_html = True)
st.markdown("<h2 style = 'text-align: center; color: orange;'> Please select the filters below </h1>", unsafe_allow_html = True)

# ------ Selection Area ------

department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value = min(ages),
                        max_value = max(ages),
                        value = (min(ages),max(ages)))

department_selection = st.multiselect('Department:',
                                    department,
                                    default = department)

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0] # Number of rows
st.markdown(f'*Availble Results: {number_of_result}*') # * can be used to make it italic

# st.dataframe(df)

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()

# ------ Plot Bar Chart ------
bar_chart = px.bar(df_grouped,
                   x = 'Rating',
                   y = 'Votes',
                   text = 'Votes',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template = 'plotly_white')
st.plotly_chart(bar_chart)

# ------ Display Image and Dataframe ------
col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
with col1:
    st.image(image,
        caption = 'Designed by Freepik',
        use_column_width = True
)
with col2:
    st.dataframe(df[mask])

# ------ Plot Pie Chart ------
pie_chart = px.pie(df_participants,
                title = 'Distribution of Participants',
                values = 'Participants',
                names = 'Departments')

st.plotly_chart(pie_chart)