import streamlit as st
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import plotly.io as pio

st.set_page_config(page_title='Competitive Landscape',page_icon="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm",layout="wide")
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


with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: left;">
        <img src="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm" width="40" style="margin-right: 20px;">
        <h1 style="font-size: 2em; color: rgb(129, 78, 252); margin: 0;">Unleashed</h1>
    </div>
""", unsafe_allow_html=True)
    st.markdown("## **Sentiment Analysis For Consumer Electronics**")
    st.markdown("Competitive Landscape",help='Provides a comparative view of public sentiment across different brands, products, or competitors')
    st.markdown("---")

df=pd.read_csv("main.csv")
c1,c2,c3=st.columns([1,0.7,3])
with c1:
    # --------------------------top brands---------------
    dic={
        "Overall Rating":df.groupby('brand')['reviews.rating'].mean()}
    data=pd.DataFrame(dic)
    data=data.sort_values('Overall Rating',ascending=False)
    st.markdown("***Top Brands***")
    st.dataframe(data.head(10))
with c2:
    st.markdown("<h3>",unsafe_allow_html=True)
    data=pd.DataFrame()
    data['rating']=df.groupby('brand')['reviews.rating'].mean()
    data['review']=df.groupby('brand')['reviews.title'].count()
    review_count = {
    'Total Brands': len(df['brand'].unique()),
    'Average Rating per Brand':round(data['rating'].mean()),
    'Average Reviews per Brand':round(data['review'].mean()),
    }
    for i, (label, count) in enumerate(review_count.items()):
        st.markdown(f"""
                <div class="review-box" style="background-color: #95a5a6;">
                    <div style="font-size: 14px; color:white; white-space: normal; font-weight: bold;">{label}</div>
                    <div style="font-size: 20px; color:white; font-weight: bold;">{count}</div>
                </div>
                <br>
            """, unsafe_allow_html=True)
        
with c3:
    # ------------------brand wordcloud-------------
    st.markdown("***Word Cloud of Different brands***")
    text=str(df['brand'].unique())
    custom_wordcloud = WordCloud(width=700, height=300,
                                background_color='#ffffff',
                                stopwords=STOPWORDS.union({'used', 'can'}), # Adding more stopwords
                                max_words=80,
                                colormap='seismic',
                                font_path='arial.ttf' if 'arial.ttf' in matplotlib.get_data_path() else None, # Example font path
                                min_font_size=8).generate(text)
        
    fig, ax = plt.subplots(figsize=(10, 4), facecolor=None)
    ax.imshow(custom_wordcloud, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)

brands = df['brand'].unique()
selected_brands = st.multiselect("Select 5 Brands to Compare", brands, default=None)
brand_df=df[df['brand'].isin(selected_brands)]
if len(selected_brands) < 5:
    st.warning("Please select exactly 5 brands to compare")
else:
    s1,s2=st.columns([2,1])
    with s1:
        # ---------------------------stacked bar chart------------
        # Create horizontal stacked bar chart
        df_counts = brand_df.groupby(['brand', 'sentiment_label_textblob']).size().reset_index(name='count')
        fig = px.bar(
            df_counts,
            x='count',
            y='brand',
            color='sentiment_label_textblob',
            orientation='h',
            title='Sentiment Distribution by Brand',
            color_discrete_sequence=px.colors.qualitative.Set1  # Optional: better color distinction
        )
        fig.update_layout(barmode='stack')
        with st.container(border=True):
            st.write(fig)
     


    with s2:
        # -----------pie chart--------------
        brand_counts = brand_df.groupby('brand')['reviews.title'].count().reset_index(name='count')
        fig = px.pie(brand_counts.head(), names='brand', values='count',title='Review Count by Brands',hole=0.7,
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
            textinfo='value+percent')
        with st.container(border=True):
            st.write(fig)
    
    # -----------------overall sentiment score indicator--------------
    with st.container(border=True):
        st.markdown("<h5><i>Overall Sentiment Score Indicator",unsafe_allow_html=True)
        sentiment_weights = {
        'Very Positive': 2,
        'Positive': 1,
        'Neutral': 0,
        'Negative': -1,
        'Very Negative': -2
        }
        fig_list=[]
        for brand_name in selected_brands:
            brand_df = df[df['brand'] == brand_name]
            counts = brand_df['sentiment_label_textblob'].value_counts()
            count_df = counts.reset_index()
            count_df.columns = ['sentiment_label_textblob', 'count']
            count_df['weight'] = count_df['sentiment_label_textblob'].map(sentiment_weights)
            count_df['score'] = count_df['count'] * count_df['weight']

            net_score = count_df['score'].sum()
            total = count_df['count'].sum()
            nss = (net_score / (total * 2)) * 100 if total > 0 else 0

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=nss,
                title={'text': f"{brand_name}"},
                gauge={
                    'axis': {'range': [-100, 100]},
                    'bar': {'color': "black"},
                    'steps': [
                        {'range': [-100, -60], 'color': '#ff4d4d'},
                        {'range': [-60, -20], 'color': '#ff9999'},
                        {'range': [-20, 20],  'color': '#dddddd'},
                        {'range': [20, 60],   'color': '#aaffaa'},
                        {'range': [60, 100],  'color': '#4dff4d'},
                    ]
                }
            ))
            fig_list.append(fig)

        if len(fig_list)==5:
            cols = st.columns(5)
            for i, fig in enumerate(fig_list):  # fig_list is a list of figures
                cols[i].plotly_chart(fig, use_container_width=True, key=f"figure_{i}")
        else:
            st.warning("Only Upto 5 Brands")
            
    
