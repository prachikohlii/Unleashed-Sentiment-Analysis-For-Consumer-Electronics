import streamlit as st
import time
st.set_page_config(page_title="Welcome Aboard", page_icon="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm", layout="wide")


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

# CSS Styling
st.markdown("""
    <style>
    h1 {
        font-size: 3.5em;
        margin-bottom: 10px;
        color: #2e4053;
    }
    .typewriter h2 {
        overflow: hidden;
        border-right: .15em solid rgb(129, 78, 252);
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .1em;
        animation: 
            typing 12s steps(40, end) infinite alternate,
            blink-caret .75s step-end infinite;      
    }

    /* Main typing keyframes */
    @keyframes typing {
    0% {
        width: 0;
    }
    50% {
        width: 100%;
    }
    80% {
        width: 100%;
    }
    100% {
        width: 0;
    }
    }

    /* Caret blinking */
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: rgb(129, 78, 252); }
    }
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 20px;
    }

    .social-icons img {
        width: 32px;
        height: 32px;
        transition: transform 0.2s;
    }

    .social-icons img:hover {
        transform: scale(1.1);
    }
   
    </style>
""", unsafe_allow_html=True)

# ------------button css-------------
st.markdown("""
    <style>
    .stButton > button {
        display: inline-block;
        background-color: rgb(129, 78, 252);
        color: white;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease; 
        text-align: center;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 30px;
       
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
    </style>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown("<h2 style='text-align:center;'><b>The Home to Unleashed",unsafe_allow_html=True,help='introduction and overview of the functionalities offered in the project')
    st.markdown("---")
    st.markdown("""
    <div class='social-icons'>
        <a href="https://www.linkedin.com/in/prachikohli00" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn"></a>
        <a href="https://github.com/prachikohlii" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub"></a>
    </div>
   
    """, unsafe_allow_html=True)

# Main container content
st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown("""
    <div style="display: flex; align-items: center; justify-content: left;">
        <img src="https://drive.google.com/thumbnail?id=1LhqJDkJF8J8_J7_9VT12-L8Fk4q6htYm" width="70" style="margin-right: 20px;">
        <h1 style="font-size: 3.5em; color: rgb(129, 78, 252); margin: 0;">Unleashed</h1>
    </div>
""", unsafe_allow_html=True)




# Typing effect headline
st.markdown("""
    <div class="typewriter">
        <h2>Sentiment Analysis for Consumer Electronics</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown('''This project delves into the vast landscape of customer reviews for electronics products,  <br>
aiming to uncover the underlying opinions and emotions expressed by users.''',unsafe_allow_html=True)


st.markdown("""
    <style>
    .intro-box {
        background:linear-gradient(135deg, #fdfbfb, #ebedee);
        border-left: 5px solid rgb(129, 78, 252);
        padding: 1.5rem;
        border-radius: 12px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.05rem;
        margin-top: 1rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        white-space: pre-wrap;
    }
    .intro-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #0077b6;
        margin-bottom: 0.5rem;
    }
    .stProgress > div > div > div > div {
        background-color:rgb(129, 78, 252) ;
    }
    </style>
""", unsafe_allow_html=True)

def badge(number):
    return f"""<span style="background-color:#814EFC; color:white; padding:2px 8px; border-radius:8px; font-weight:bold; font-size:0.9rem;">{number}</span>"""
# --- Description text to animate ---
description = f"""

<b>What is Sentiment Analysis? 
 Sentiment analysis, also known as opinion mining, is a natural language processing (NLP) technique used to determine the emotional tone expressed in a piece of text.

<div style="line-height: 0.4;"> 
**Why is Sentiment Analysis for Consumer Electronics important?**
▪️Understand Customer Feedback
▪️Monitor Brand Reputation
▪️Improve Products and Services
▪️Enhance Customer Service
▪️Gain Competitive Intelligence
</div>

<div style="line-height: 0.6;">
**Unleashed Offers:**
{badge(1)} **Snapshot** — Concise overview featuring random examples, word clouds and sentiment counts.  
{badge(2)} **The Deep Dive** — Deep insights into the data providing a detailed analysis. 
{badge(3)} **Competitive Landscape** — Provides a comparative view of public sentiment across different brands, products,or competitors. 
{badge(4)} **NLPfication** — Perform NLP: instantly receive tokenized, lemmatized, POS, and NER forms of text.   
{badge(5)} **Analysis Hub** — Analyze text sentiment in real-time or via CSV upload.
</div>
<div style="line-height: 0.3;">
Ideal for students, researchers, or businesses curious about public opinion towards consumer electronics.
"""

# --- Generator function to yield animated text ---
def stream_description(text, delay=0.03):
    lines = text.strip().splitlines()
    output = ""
    total_lines = len([l for l in lines if l.strip()])
    line_count = 0
    for line in lines:
        if not line.strip():
            output += "\n\n"
            yield output, line_count, total_lines
            continue
        words = line.strip().split()
        line_output = ""
        for word in words:
            line_output += word + " "
            current = output + line_output
            yield current, line_count, total_lines
            time.sleep(delay)
        output += line_output + "\n\n"
        line_count += 1
        yield output, line_count, total_lines

# --- Main interaction ---
if st.button("Get Started"):
    placeholder = st.empty()
    progress_bar = st.progress(0)

    for partial_text, line_index, total in stream_description(description):
        placeholder.markdown(f'<div class="intro-box">{partial_text}</div>', unsafe_allow_html=True)
        progress = min((line_index + 1) / total, 1.0)
        progress_bar.progress(progress)

    time.sleep(0.3)


st.markdown('</div>', unsafe_allow_html=True)



