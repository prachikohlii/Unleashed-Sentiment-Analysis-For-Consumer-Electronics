import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go

st.set_page_config("Snapshot",page_icon="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm",layout="centered")
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


df=pd.read_csv("main.csv")
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: left;">
        <img src="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm" width="40" style="margin-right: 20px;">
        <h1 style="font-size: 2em; color: rgb(129, 78, 252); margin: 0;">Unleashed</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## **Sentiment Analysis For Consumer Electronics**")
    st.markdown("Snapshot",help='Concise overview featuring random examples, word clouds and sentiment counts')
    st.markdown("---")


    random=st.checkbox("**Show random sentiments**")
    sentiment_filter = st.radio(
        "Sentiment Type",
        ('positive','slightly positive', 'neutral','slightly negative', 'negative','none'),index=None
    )
    st.markdown("---")


    counts=st.checkbox("**Show Sentiment Label Counts**")
    visualization_type = st.radio(
        "Visualization type",
        ('Bar Chart', 'Pie Chart','None'),index=None
    )
    st.markdown("---")

    
    raw=st.checkbox("**Show Raw data based on Scores**")
    score = st.slider(
        "Score Range:", -0.9, 0.9,(-0.1, 0.1),step=0.1)
    show=st.checkbox("Show")
    st.markdown("---")


    group=st.checkbox("**Breakdown Brands by Sentiment**")
    brands = st.multiselect(
        "Select Brands (Upto 4)",
        options=df['brand'].unique()
    )
    st.markdown("---")


    word_cloud=st.checkbox("**Display Word Cloud for Sentiments**")
    sentiment_wordcloud = st.radio(
        "Sentiment Type", 
        ('positive','slightly positive', 'neutral','slightly negative', 'negative','None'),index=None
    )

    st.markdown("---")



# ------------main page-----------

if random:
    st.markdown('***Showing Random Sentiments...***')
    if sentiment_filter:
        if sentiment_filter=='positive':
            a=df['reviews.text'][df['sentiment_label_textblob']=='Positive']
            rev=np.random.choice(a)
            data={
                'Positive':rev
            }
            st.json(data)
        elif sentiment_filter=='slightly positive':
            a=df['reviews.text'][df['sentiment_label_textblob']=='Slightly Positive']
            rev=np.random.choice(a)
            data={
                'Slightly Positive':rev
            }
            st.json(data)
        elif sentiment_filter=='neutral':
            a=df['reviews.text'][df['sentiment_label_textblob']=='Neutral']
            rev=np.random.choice(a)
            data={
                'Neutral':rev
            }
            st.json(data)
        
        elif sentiment_filter=='slightly negative':
            a=df['reviews.text'][df['sentiment_label_textblob']=='Slightly Negative']
            rev=np.random.choice(a)
            data={
                'Slightly Negative':rev
            }
            st.json(data)

        elif sentiment_filter=='negative':
            a=df['reviews.text'][df['sentiment_label_textblob']=='Negative']
            rev=np.random.choice(a)
            data={
                'Negative':rev
            }
            st.json(data)
        else:
            st.caption('Select Sentiment Type')
    else:
        st.caption("Select Sentiment Type")




if counts:
    st.markdown('***Showing Sentiments counts...***')
    if visualization_type:
        if visualization_type=='Bar Chart':
            fig = px.bar(
            df,
            x=df['sentiment_label_textblob'].unique(),
            y=df['sentiment_label_textblob'].value_counts(),
            color=df['sentiment_label_textblob'].unique(),  # color bars based on sentiment categories
            color_discrete_sequence=['#388E3C','#81C784','#BDBDBD','#F57C00','#D32F2F'],
            title='Sentiment Distribution',
            labels={'x': 'Sentiment Category', 'y': 'Frequency'},
            text=df['sentiment_label_textblob'].value_counts()  # Show the count on top of each bar
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside', width=0.7) 
            fig.update_layout(
                showlegend=False,  # Hide the legend to avoid redundancy
                xaxis_title='Sentiment Category',
                yaxis_title='Frequency',
                plot_bgcolor='white',  # White background for a clean look
                font=dict(family='Arial', size=12)
            )
            fig.update_layout(
                    xaxis_tickangle=-45  # Rotate labels by -45 degrees
                )
            with st.container(border=True):
                st.write(fig)
                
        elif visualization_type=='Pie Chart':
            fig=px.pie(df, names=df['sentiment_label_textblob'].unique(),values=df['sentiment_label_textblob'].value_counts(),
                       color_discrete_sequence=['#388E3C','#81C784','#BDBDBD','#F57C00','#D32F2F'],title='Sentiment Distribution',hole=0.3)
            fig.update_traces(
                textinfo='label+percent+value')
            with st.container(border=True):
                st.write(fig)
        else:
            st.caption('Select Visualization Type')
    else:
        st.caption('Select Visualization Type')


if raw:
    st.markdown('***Displaying Raw Data based on Scores...***') 
    if show:
        if score: 
            lb=score[0]
            ub=score[1]
            del df['Unnamed: 0']
            st.dataframe(df[(df['sentiment_score'] >= lb) & (df['sentiment_score'] <= ub)],hide_index=True)
    else:
        st.caption('Adjust Range and click *Show*')

if group:
    st.markdown('***Breaking Down Brands by Sentiment...***')
    if brands:
        if len(brands)==1:
            my_data=df[df['brand'].isin(brands)]
            sentiment=my_data['sentiment_label_textblob'].unique()
            count=my_data['sentiment_label_textblob'].value_counts()
            fig = go.Figure(data=[
            go.Bar(name=brands[0], x=sentiment, y=count,marker={'color':'#ff3333'}),
            ])
            fig.update_layout(title='Sentiment Distribution Across Brands',
                barmode='group',xaxis_title='Sentiment Label',
                yaxis_title='Sentiment Count',
                title_x=0,
                legend_title='Brand',
                bargap=0.2,
                template='plotly_white',
                font=dict(size=16),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1))
            fig.update_layout(
                    xaxis_tickangle=-45  # Rotate labels by -45 degrees
                )
            with st.container(border=True):
                st.plotly_chart(fig)
            
          
        elif len(brands)==2:
            my_data1=df[df['brand'].isin([brands[0]])]
            my_data2=df[df['brand'].isin([brands[1]])]
            sentiment1=my_data1['sentiment_label_textblob'].unique()
            count1=my_data1['sentiment_label_textblob'].value_counts()
            sentiment2=my_data2['sentiment_label_textblob'].unique()
            count2=my_data2['sentiment_label_textblob'].value_counts()
            fig = go.Figure(data=[
            go.Bar(name=brands[0], x=sentiment1, y=count1,marker={'color':'#ff3333'}),
            go.Bar(name=brands[1], x=sentiment2, y=count2,marker={'color':'#3399ff'})
            ])
            fig.update_layout(title='Sentiment Distribution Across Brands',
                barmode='group',xaxis_title='Sentiment Label',
                yaxis_title='Sentiment Count',
                title_x=0,
                legend_title='Brand',
                bargap=0.2,
                template='plotly_white',
                font=dict(size=16),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1))
            fig.update_layout(
                    xaxis_tickangle=-45  # Rotate labels by -45 degrees
                )
            with st.container(border=True):
                st.plotly_chart(fig)

        elif len(brands)==3:
            my_data1=df[df['brand'].isin([brands[0]])]
            my_data2=df[df['brand'].isin([brands[1]])]
            my_data3=df[df['brand'].isin([brands[2]])]
            sentiment1=my_data1['sentiment_label_textblob'].unique()
            count1=my_data1['sentiment_label_textblob'].value_counts()
            sentiment2=my_data2['sentiment_label_textblob'].unique()
            count2=my_data2['sentiment_label_textblob'].value_counts()
            sentiment3=my_data3['sentiment_label_textblob'].unique()
            count3=my_data3['sentiment_label_textblob'].value_counts()
            fig = go.Figure(data=[
            go.Bar(name=brands[0], x=sentiment1, y=count1,marker={'color':'#ff3333'}),
            go.Bar(name=brands[1], x=sentiment2, y=count2,marker={'color':'#3399ff'}),
            go.Bar(name=brands[2], x=sentiment3, y=count3,marker={'color':'#33ff33'})
            ])
            fig.update_layout(title='Sentiment Distribution Across Brands',
                barmode='group',xaxis_title='Sentiment Label',
                yaxis_title='Sentiment Count',
                title_x=0,
                legend_title='Brand',
                bargap=0.2,
                template='plotly_white',
                font=dict(size=16),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1))
            fig.update_layout(
                    xaxis_tickangle=-45  # Rotate labels by -45 degrees
                )
            with st.container(border=True):
                st.plotly_chart(fig)

        elif len(brands)==4:
            my_data1=df[df['brand'].isin([brands[0]])]
            my_data2=df[df['brand'].isin([brands[1]])]
            my_data3=df[df['brand'].isin([brands[2]])]
            my_data4=df[df['brand'].isin([brands[3]])]
            sentiment1=my_data1['sentiment_label_textblob'].unique()
            count1=my_data1['sentiment_label_textblob'].value_counts()
            sentiment2=my_data2['sentiment_label_textblob'].unique()
            count2=my_data2['sentiment_label_textblob'].value_counts()
            sentiment3=my_data3['sentiment_label_textblob'].unique()
            count3=my_data3['sentiment_label_textblob'].value_counts()
            sentiment4=my_data4['sentiment_label_textblob'].unique()
            count4=my_data4['sentiment_label_textblob'].value_counts()
            fig = go.Figure(data=[
            go.Bar(name=brands[0], x=sentiment1, y=count1,marker={'color':'#ff3333'}),
            go.Bar(name=brands[1], x=sentiment2, y=count2,marker={'color':'#3399ff'}),
            go.Bar(name=brands[2], x=sentiment3, y=count3,marker={'color':'#33ff33'}),
            go.Bar(name=brands[3], x=sentiment4, y=count4,marker={'color':' #ff9933'}),
            ])
            fig.update_layout(title='Sentiment Distribution Across Brands',
                barmode='group',xaxis_title='Sentiment Label',
                yaxis_title='Sentiment Count',
                title_x=0,
                legend_title='Brand',
                bargap=0.2,
                template='plotly_white',
                font=dict(size=16),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1))
            fig.update_layout(
                    xaxis_tickangle=-45  # Rotate labels by -45 degrees
                )
            with st.container(border=True):
                st.plotly_chart(fig)

        elif len(brands)>=5:
            st.error('Only Upto 4 brands')
    else:
        st.caption('Select Brands')



if word_cloud:
    st.markdown('***Displaying Word Cloud...***')
    if sentiment_wordcloud:
        if sentiment_wordcloud=='positive':
            st.write("Sentiment Word Cloud for Positive Sentiment")
            text=str(df['reviews.text'][df['sentiment_label_textblob']=='Positive'])
            custom_wordcloud = WordCloud(width=800, height=500,
                                        background_color='#ffffff',
                                        stopwords=STOPWORDS.union({'used', 'can'}), # Adding more stopwords
                                        max_words=200,
                                        colormap='autumn_r',
                                        font_path='arial.ttf' if 'arial.ttf' in matplotlib.get_data_path() else None, # Example font path
                                        min_font_size=8).generate(text)
                

            fig, ax = plt.subplots(figsize=(12, 6), facecolor=None)
            ax.imshow(custom_wordcloud, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        
        
        elif sentiment_wordcloud=='slightly positive':
            st.write("Sentiment Word Cloud for Slightly Positive Sentiment")
            text=str(df['reviews.text'][df['sentiment_label_textblob']=='Slightly Positive'])
            custom_wordcloud = WordCloud(width=800, height=500,
                                        background_color='#ffffff',
                                        stopwords=STOPWORDS.union({'used', 'can'}), # Adding more stopwords
                                        max_words=200,
                                        colormap='gist_heat',
                                        font_path='arial.ttf' if 'arial.ttf' in matplotlib.get_data_path() else None, 
                                        min_font_size=8).generate(text)
        
            fig, ax = plt.subplots(figsize=(12, 6), facecolor=None)
            ax.imshow(custom_wordcloud, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        
        
            
        elif sentiment_wordcloud=='neutral':
            st.write("Sentiment Word Cloud for Neutral Sentiment")
            text=str(df['reviews.text'][df['sentiment_label_textblob']=='Neutral'])

            custom_wordcloud = WordCloud(width=800, height=500,
                                        background_color='#ffffff',
                                        stopwords=STOPWORDS.union({'used', 'can'}), # Adding more stopwords
                                        max_words=200,
                                        colormap='RdBu',
                                        font_path='arial.ttf' if 'arial.ttf' in matplotlib.get_data_path() else None, 
                                        min_font_size=8).generate(text)
                
            fig, ax = plt.subplots(figsize=(12, 6), facecolor=None)
            ax.imshow(custom_wordcloud, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        
            
        elif sentiment_wordcloud=='slightly negative':
            st.write("Sentiment Word Cloud for Slightly Negative Sentiment")
            text=str(df['reviews.text'][df['sentiment_label_textblob']=='Slightly Negative'])

            custom_wordcloud = WordCloud(width=800, height=500,
                                        background_color='#ffffff',
                                        stopwords=STOPWORDS.union({'used', 'can'}), 
                                        max_words=200,
                                        colormap='jet_r',
                                        font_path='arial.ttf' if 'arial.ttf' in matplotlib.get_data_path() else None, 
                                        min_font_size=8).generate(text)
                

            fig, ax = plt.subplots(figsize=(12, 6), facecolor=None)
            ax.imshow(custom_wordcloud, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        
            
        elif sentiment_wordcloud=='negative':
            st.write("Sentiment Word Cloud for Negative Sentiment")
            text=str(df['reviews.text'][df['sentiment_label_textblob']=='Negative'])
            custom_wordcloud = WordCloud(width=800, height=500,
                                        background_color='#ffffff',
                                        stopwords=STOPWORDS.union({'used', 'can'}), # Adding more stopwords
                                        max_words=200,
                                        colormap='seismic',
                                        font_path='arial.ttf' if 'arial.ttf' in matplotlib.get_data_path() else None, # Example font path
                                        min_font_size=8).generate(text)
                
            
            fig, ax = plt.subplots(figsize=(12, 6), facecolor=None)
            ax.imshow(custom_wordcloud, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        else:
            st.caption('Select Sentiment Type')
    else:
        st.caption('Select Sentiment Type')     


if random==False and raw==False and group==False and counts==False and word_cloud==False:
    st.write("Choose an option from Sidebar")


 



