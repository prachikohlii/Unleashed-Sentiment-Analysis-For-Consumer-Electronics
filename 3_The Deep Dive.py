import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title='The Deep Dive',page_icon="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm",layout="wide")
st.markdown(
    """
    <style>
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
      
        [data-testid="stSidebarNav"] a {
            color: #4a5568; /* Dark gray text */
            border-left: 3px solid transparent; /* Initially no left border */
        }
        [data-testid="stSidebarNav"] a:hover {
            background-color: #edf2f7; /* Lighter gray on hover */
            color: #2d3748; /* Darker text on hover */
            border-left-color:rgb(129, 78, 252); /* Blue left border on hover (example color) */
        }
   
    </style>
    """,
    unsafe_allow_html=True,
)
   
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: left;">
        <img src="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm" width="40" style="margin-right: 20px;">
        <h1 style="font-size: 2em; color: rgb(129, 78, 252); margin: 0;">Unleashed</h1>
    </div>
""", unsafe_allow_html=True)
    st.markdown("## **Sentiment Analysis For Consumer Electronics**")
    st.markdown("The Deep Dive",help='Deep insights into the data providing a detailed analysis')
    st.markdown("---")

df=pd.read_csv("main.csv")
del df['Unnamed: 0']
# Example counts for each sentiment category
review_counts = {
    "Total Sentiment Labels":5,
    "Total Positive": df['sentiment_label_textblob'][df['sentiment_label_textblob']=='Positive'].count(),
    "Total Slightly Positive":df['sentiment_label_textblob'][df['sentiment_label_textblob']=='Slightly Positive'].count() ,
    "Total Neutral": df['sentiment_label_textblob'][df['sentiment_label_textblob']=='Neutral'].count(),
    "Total Slightly Negative": df['sentiment_label_textblob'][df['sentiment_label_textblob']=='Slightly Negative'].count(),
    "Total Negative": df['sentiment_label_textblob'][df['sentiment_label_textblob']=='Negative'].count()
}
color=["#004d00","#219150","#2ecc71","#95a5a6","#e67e22","#e74c3c"]

st.markdown("""
    <style>
    .review-box {
        border-radius: 20px;
        padding: 10px 15px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .review-box:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Create columns and render the containers
cols = st.columns(6)
for i, (label, count) in enumerate(review_counts.items()):
    with cols[i]:
        st.markdown(f"""
            <div class="review-box" style="background-color:{color[i]};">
                <div style="font-size: 14px; color:white; white-space: normal; font-weight: bold;">{label}</div>
                <div style="font-size: 20px; color:white; font-weight: bold;">{count}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<h6>",unsafe_allow_html=True)

col1,col2,col3=st.columns([0.8,2.2,2.2])
with col2: 
      # ----------------------top 10 positive-------------
    df.drop_duplicates(subset=['reviews.text'],inplace=True)
    df_positive = df[df['sentiment_label_textblob'] == 'Positive']
    # Sort by Score in decreasing order
    df_positive_sorted = df_positive.sort_values(by='sentiment_score', ascending=False)
    top_10_positive_comments = df_positive_sorted.head(10)
    st.markdown("***Top 10 Most Positive Comments***")
    # Show the table in Streamlit
    st.dataframe(top_10_positive_comments[['sentiment_score','reviews.title','reviews.text']], use_container_width=True,hide_index=True)
with col3:
    # ----------------------top 10 negative-------------
    df_negative = df[df['sentiment_label_textblob'] == 'Negative']
    # Sort by Score in decreasing order
    df_negative_sorted = df_negative.sort_values(by='sentiment_score', ascending=True)
    top_10_negative_comments = df_negative_sorted.head(10)
    st.markdown("***Top 10 Most Negative Comments***")
    # Show the table in Streamlit
    st.dataframe(top_10_negative_comments[['sentiment_score','reviews.title','reviews.text']], use_container_width=True,hide_index=True)
with col1:
    review_count = {
    'Total Reviews Processed': df['reviews.text'].count(),
    'Total Brands': len(df['brand'].unique()),
    "Categories": len(df['categories'].unique()),
    }
    st.markdown("<h6>",unsafe_allow_html=True)
    for i, (label, count) in enumerate(review_count.items()):
        st.markdown(f"""
                <div class="review-box" style="background-color: #95a5a6;">
                    <div style="font-size: 14px; color:white; white-space: normal; font-weight: bold;">{label}</div>
                    <div style="font-size: 20px; color:white; font-weight: bold;">{count}</div>
                </div>
                <br>
            """, unsafe_allow_html=True)
        
st.markdown("<br>",unsafe_allow_html=True)

c1,c2,c3=st.columns([1.6,2.6,0.8])
dic={
 "Total Reviews":df.groupby('categories')['reviews.text'].count(),
    "Overall Rating":df.groupby('categories')['reviews.rating'].mean()}
data=pd.DataFrame(dic)
data=data.sort_values('Overall Rating',ascending=False)
with c1:
    # -------------------top categories-------------------
    st.markdown("***Top Categories***")
    st.dataframe(data.head(10))
with c2:
    category_counts = df.groupby('categories')['reviews.title'].count().reset_index(name='count')
    fig = px.pie(category_counts.head(10), names='categories', values='count',title='Review Count by Categories',hole=0.7,
                 color_discrete_sequence=["#4E79A7", 
    "#F28E2B",  
    "#E15759",  
    "#76B7B2",  
    "#59A14F",  
    "#EDC948",
    "#B07AA1",  
    "#FF9DA7",  
    "#9C755F",  
    "#BAB0AC" ])
    fig.update_traces(
        textinfo='percent')
    with st.container(border=True):
        st.write(fig)
with c3:
    data=pd.DataFrame()
    data['rating']=df.groupby('categories')['reviews.rating'].mean()
    data['review']=df.groupby('categories')['reviews.title'].count()
    review_count = {
        'Average Rating per Category':round(data['rating'].mean()),
        'Average Reviews per Category':round(data['review'].mean()),
        }
    st.markdown("<h1>",unsafe_allow_html=True)
    st.markdown("<h6>",unsafe_allow_html=True)
    for i, (label, count) in enumerate(review_count.items()):
        st.markdown(f"""
                <div class="review-box" style="background-color: #95a5a6;">
                    <div style="font-size: 14px; color:white; white-space: normal; font-weight: bold;">{label}</div>
                    <div style="font-size: 20px; color:white; font-weight: bold;">{count}</div>
                </div>
                <br>
            """, unsafe_allow_html=True)


t1,t2=st.columns([0.5,1.5])
df['reviews.date'] = pd.to_datetime(df['reviews.date'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['reviews.date'])
min_date = df['reviews.date'].min().date()
max_date = df['reviews.date'].max().date()
with t1:
    st.markdown("<h1>",unsafe_allow_html=True)
    st.markdown("<h6>",unsafe_allow_html=True)
    with st.container(border=True):
        st.write("***Date Filter***")
        start = datetime.date(2018, 2, 1)
        end = datetime.date(2018, 5, 21)
        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=start)
        end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=end)

with t2:
    # ---------trends--------
    with st.container(border=True):
        mask = (df['reviews.date'].dt.date >= start_date) & (df['reviews.date'].dt.date <= end_date)
        filtered_df = df.loc[mask]

        # Group by date and sentiment
        sentiment_trend = filtered_df.groupby([filtered_df['reviews.date'].dt.date, 'sentiment_label_textblob']).size().reset_index(name='count')

        # Pivot table for lineplot
        trend_pivot = sentiment_trend.pivot(index='reviews.date', columns='sentiment_label_textblob', values='count').fillna(0)

        # Plot using Seaborn
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=trend_pivot, ax=ax)
        ax.set_title("Sentiment Trends Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.legend(title="Sentiment")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display in Streamlit
        st.pyplot(fig)


    
        
