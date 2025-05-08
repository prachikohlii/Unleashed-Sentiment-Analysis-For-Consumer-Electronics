import streamlit as st
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pandas as pd
import io

st.set_page_config(page_title='Analysis Hub',page_icon="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm",layout="centered")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if isinstance(text, str): # Ensure it's a string
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
        return " ".join(words)
    return "" # Handle non-string cases

def get_sentiment_label(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity <= -0.2:
        return "Negative"
    elif -0.2 < polarity <=-0.1 :
        return "Slightly Negative"
    elif  -0.1< polarity <= 0.1:
        return "Neutral"
    elif 0.1< polarity <= 0.2:
        return "Slightly Positive"
    else:
        return "Positive"
    
def get_polarity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def get_subjectivity(text):
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity  


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
            border-left-color: rgb(129, 78, 252); /* Blue left border on hover (example color) */
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------button css-------------
st.markdown("""
    <style>
    .stButton > button {
        display: inline-block;
        background-color: rgb(129, 78, 252);
        color: white;
        padding: 0.75em 1.5em;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        text-align: center;
    }

    .stButton > button p{
            color: white;
    }     

    .stButton > button:hover {
        background-color: #A98BFF;
        transform: scale(1.03);
    }

    .stButton > button:active {
        background-color: rgb(96, 29, 252);
        transform: scale(0.98);
    }
    .stDownloadButton > button {
        display: inline-block;
        background-color: rgb(129, 78, 252);
        color: white;
        padding: 0.75em 1.5em;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
        text-align: center;
    }

    .stDownloadButton > button p{
            color: white;
    }     

    .stDownloadButton > button:hover {
        background-color: #A98BFF;
        transform: scale(1.03);
    }

    .stDownloadButton > button:active {
        background-color: rgb(96, 29, 252);
        transform: scale(0.98);
    } 

    [data-testid="stFileUploader"] button:hover{
            background-color: rgb(255, 255, 255);
            color: rgb(129, 78, 252);
            border-color: rgb(129, 78, 252);
    }
    [data-testid="stFileUploader"] button:active{
            background-color: rgb(255, 255, 255);
            color: grey;
            border-color: grey;
    }
    [data-testid="stFileUploader"] button:focus:not(:active){
            background-color: rgb(255, 255, 255);
            color: rgb(129, 78, 252);
            border-color: rgb(129, 78, 252);
    }
     [data-baseweb="textarea"]:active{
            border-color: rgb(129, 78, 252);
     }
    [data-baseweb="textarea"]:focus-within{
            border-color: rgb(129, 78, 252);
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
    st.markdown("Analysis Hub",help='Analyze text sentiment in real-time or via CSV upload')
    st.markdown("---")
    st.markdown("**Analyze your texts here!**")
    selected = st.radio(
        "",
        ('Analyze Text', 'Analyze CSV','None'),index=None
    )
   

if selected==None or selected=='None':
    st.write('Choose an option from Sidebar')
elif selected=='Analyze CSV':
    with st.container(border=True):
        st.markdown("***Analyze CSV***",unsafe_allow_html=True)
        file=st.file_uploader('Upload CSV file (containing only the text column)',type='csv',)
        if file:
            data=pd.read_csv(file)
            del data['Unnamed: 0']
            data.dropna(inplace=True)
            column_name=data.columns[0]
            df=pd.DataFrame()
            df['Text']=data[column_name]
            df['cleaned_text']=data[column_name].apply(preprocess_text)
            df['sentiment_label_textblob'] = df['cleaned_text'].apply(get_sentiment_label)
            df['sentiment_score']=df['cleaned_text'].apply(get_polarity)
            df['subjectivity_score']=df['cleaned_text'].apply(get_subjectivity)
            df_new=df.drop(columns='cleaned_text')
            st.dataframe(df_new.head(10))
            def convert_df_to_csv(df):
                # Use io.StringIO to create an in-memory text buffer
                output = io.StringIO()
                df.to_csv(output, index=False)  # Write DataFrame to the buffer
                csv_data = output.getvalue().encode('utf-8')  # Get the CSV data as a string and encode it
                return csv_data
            csv=convert_df_to_csv(df_new)
            st.warning('Number of rows in file may reduce if the column contains Null values')
            st.download_button('Download Data as CSV',data=csv,file_name='analyzed_data.csv',mime='text/csv') 
          
elif selected=='Analyze Text':
    with st.container(border=True):
        st.markdown("***Analyze Text***",unsafe_allow_html=True)
        text=st.text_area("Text Input",placeholder='Start Typing...')
        analyze=st.button("Analyze")
        if analyze:
            if text=='':
                st.error("Field must not be empty")
            else:
                emoji_images = {
                    "Positive": "https://em-content.zobj.net/source/animated-noto-color-emoji/356/grinning-face-with-big-eyes_1f603.gif",
                    "Slightly Positive": "https://em-content.zobj.net/source/animated-noto-color-emoji/356/slightly-smiling-face_1f642.gif",
                    "Neutral": "https://em-content.zobj.net/source/animated-noto-color-emoji/356/neutral-face_1f610.gif",
                    "Slightly Negative": "https://em-content.zobj.net/source/animated-noto-color-emoji/356/frowning-face_2639-fe0f.gif",
                    "Negative": "https://em-content.zobj.net/source/animated-noto-color-emoji/356/angry-face_1f620.gif"
                }
                process=preprocess_text(text)
                p=get_polarity(process)
                s=get_subjectivity(process)
                sentiment=get_sentiment_label(process)
                sentiment_data = {
                    "Polarity": p,
                    "Subjectivity": s,
                    "Sentiment": sentiment
                }

                # Display using st.json
                st.text("Sentiment Analysis...")
                col1, col2 = st.columns(2)

                with col1:
                    st.json(sentiment_data)

                with col2:
                    st.image(emoji_images[sentiment], width=120)  
                
              
        st.divider()
        raw_text=st.text_area("Clean Text:",placeholder='Start Typing...')      
        clean=st.button("Clean")   
        if clean:
            if raw_text=='':
                st.error("Field must not be empty")
            else:
                clean_text=preprocess_text(raw_text)
                new_text={
                    'Cleaned Text':clean_text
                }
                st.text("Cleaned Text...")
                st.json(new_text)

                

                  
