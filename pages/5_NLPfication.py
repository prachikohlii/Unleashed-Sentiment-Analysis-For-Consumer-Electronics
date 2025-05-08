import streamlit as st
import spacy
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
st.set_page_config(page_title='NLPfication',page_icon="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm",layout="centered")
st.markdown('***Natural Language Processing On the Go...***')

nlp = spacy.load("en_core_web_sm")



with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: left;">
        <img src="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm" width="40" style="margin-right: 20px;">
        <h1 style="font-size: 2em; color: rgb(129, 78, 252); margin: 0;">Unleashed</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## **Sentiment Analysis For Consumer Electronics**")
    st.markdown("NLPfication",help='NLP Operations: instantly receive tokenized, lemmatized, POS, and NER forms of text')
    st.markdown("---")

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
            
    [data-baseweb="textarea"]:active{
            border-color: rgb(129, 78, 252);
     }
    [data-baseweb="textarea"]:focus-within{
            border-color: rgb(129, 78, 252);
     }
    [data-baseweb="select"]>div:active{
            border-color: rgb(129, 78, 252);
     }
    [data-baseweb="select"]>div:focus-within{
            border-color: rgb(129, 78, 252);
     }
    [data-testid="stExpander"] summary:hover{
            color: rgb(129, 78, 252);
            }
  
     </style>
""",unsafe_allow_html=True)




with st.expander('Tokens and Lemma'):
    text=st.text_area('',placeholder='Start typing...')
    option=st.selectbox("",options=('Sentence Tokenize','Word Tokenize'),index=None,placeholder='Type')
    token=st.button('Tokenize')
    if token:
        if text=='':
            st.error('Field must not be empty')
        else:
            doc=nlp(text)
            if option == "Word Tokenize":
                # Word tokenization: Tokens, Lemmas, POS
                word_data = [
                    {
                "token": token.text,
                "lemma": token.lemma_,
                    }
                    for token in doc
                    if not token.is_space  # skip pure whitespace
                ]
                st.text("Word Tokens")
                st.json(word_data)

            elif option == "Sentence Tokenize":
                # Sentence tokenization
                sentence_data = [{"sentence": sent.text.strip()} for sent in doc.sents]
                st.text("Sentences")
                st.json(sentence_data)

           


with st.expander('Named Entities'):
    text=st.text_area('  ',placeholder='Start typing...')
    named=st.button('Show Named Entities')
    if named:
        if text=='':
            st.error('Field must not be empty')
        else:
            st.text("Showing named entities...")
            doc = nlp(text)
            entity_data = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
            st.json(entity_data)
            
           
with st.expander('Parts of Speech'):
    text=st.text_area('    ',placeholder='Start typing...')
    summary=st.button("Show POS")
    if summary:
        if text=='':
            st.error('Field must not be empty')
        else:
            st.text("Parts of Speech...")
            doc=nlp(text)
            pos_data = [{"text": token.text, "pos": token.pos_, "tag": token.tag_} for token in doc]
            st.json(pos_data)
            
            
           
           









