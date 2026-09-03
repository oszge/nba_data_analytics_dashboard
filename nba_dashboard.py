import pandas as pd
import numpy as np
import streamlit as st
import millify
import matplotlib.pyplot as plt
import seaborn as sns

#DATA COLLECTING, READING
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\oszge\Documents\CodeCool\python\envPython\nba\nba.csv")

def conversion(x):

    height = str(x).split("-")
    return int(height[0])*12 + int(height[1])

data = load_data()

st.set_page_config(
    page_title="Dashboard",
    layout="centered",
    
)
st.title("NBA Dashboard")
st.subheader("Key Performance of NBA players")

##DATA CLEANING
#replace missing values in the college column with "None"
data["College"].fillna("None", inplace=True)
#drop rows where salary is missing or zero
data = data.dropna(subset=["Salary"])
data = data[data["Salary"] > 0]
data["Salary"] = data["Salary"].astype("int32")
#convert the height column from feet-inches to total inches  
data["Height"] = data["Height"].apply(conversion)
data["Age"] = data["Age"].astype("i1")

st.sidebar.subheader("Filter")
teams = st.sidebar.multiselect(label="Teams", options=data["Team"].unique(), default=data["Team"].unique())
positions = st.sidebar.multiselect(label="Positions", options=data["Position"].unique(), default=data["Position"].unique())
age_selects = st.sidebar.slider("Age", min_value=data["Age"].min() , max_value=data["Age"].max(), value=[data["Age"].min(), data["Age"].max()], step=1)

filtered_data = data[ 

    (data["Team"].isin(teams)) & 
    (data["Position"].isin(positions)) & 
    (data["Age"] > age_selects[0]) &
    (data["Age"] < age_selects[1])]


avg_salary = 0 if filtered_data.empty else filtered_data["Salary"].mean()
youngest_player = "unknown" if filtered_data.empty else filtered_data["Name"][filtered_data["Age"]==filtered_data["Age"].min()].iloc[0]
avg_age = 0 if filtered_data.empty else filtered_data["Age"].mean().round(0)

with st.container(border=True, horizontal=True, horizontal_alignment="distribute"):
    c1, c2, c3 = st.columns([2.3,3,1])

    c1.metric("Avg Salary", millify.millify(avg_salary, precision=2))
    c2.metric("Youngest Player", youngest_player)
    c3.metric("Avg Age", int(avg_age))

st.dataframe(filtered_data)

st.markdown("""
<style>
.stMultiSelect [data-baseweb="tag"] span {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)


avg_team_salaries = filtered_data.groupby("Team")["Salary"].mean()

fig, ax = plt.subplots()
sns.barplot(x=avg_team_salaries.index, y=avg_team_salaries.values, color="Black", ax=ax)
sns.barplot(x=[avg_team_salaries.idxmax()], y=[avg_team_salaries.max()], color="#858592", ax=ax)
ax.tick_params(axis="x", rotation=90)
ax.text(avg_team_salaries.index.get_loc(avg_team_salaries.idxmax()), avg_team_salaries.max(), s=avg_team_salaries.idxmax())
ax.set_title(f"The highest avarage salary's team: {avg_team_salaries.idxmax()}")
st.pyplot(fig)
plt.close(fig)


highest_avg_weight = filtered_data.groupby("Position")["Weight"].mean()

fig, ax = plt.subplots()
sns.barplot(x=highest_avg_weight.index, y=highest_avg_weight.values, color="Black", ax=ax)
sns.barplot(x=[highest_avg_weight.idxmax()], y=[highest_avg_weight.max()], color="#858592", ax=ax)
ax.tick_params(axis="x", rotation=90)
ax.text(x=highest_avg_weight.index.get_loc(highest_avg_weight.idxmax()), y=highest_avg_weight.max(), s=highest_avg_weight.idxmax())
ax.set_title(f"The highest avarage weight's position: {highest_avg_weight.idxmax()}")
st.pyplot(fig)
plt.close(fig)


highest_paid_top5 = filtered_data.sort_values("Salary", ascending=False).head()

fig,ax=plt.subplots()
sns.barplot(data=highest_paid_top5, x="Salary", y="Name", color="Black", ax=ax)
ax.set_title(f"The highest paid player is: {highest_paid_top5['Name'].iloc[0]}")
st.pyplot(fig)
plt.close(fig)


fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x="Height", y="Salary", hue="Position", palette=["#111010", "#88818F", "#5C5663","#64596E","#DED5E7"], ax=ax)
st.pyplot(fig)
plt.close(fig)


filtered_corr = filtered_data[['Height', 'Salary']]

fig, ax = plt.subplots()
sns.heatmap(filtered_corr.corr(), cmap="Greys", annot=True, ax=ax)
st.pyplot(fig)
plt.close(fig)

st.dataframe(filtered_corr.corr())

filtered_nba_data = data[(data["Salary"] > 5_000_000) & (data["Age"] < 30)]

st.write(f"Players with a salary above 5M")
st.dataframe(filtered_nba_data)

filtered_nba_data.to_csv(r"C:\Users\oszge\Documents\CodeCool\python\envPython\filtered_nba_data.csv",index=False)