import sys
import os
import joblib
import base64
import pandas as pd
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ai_advice import generate_business_advice

# App Color Setup
st.markdown("""
<style>

/* Main app gradient */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #29298a); !important;
    background-attachment: fixed !important;
}
            
/* Selectbox */
div[data-baseweb="select"] > div {
    background: linear-gradient(135deg, #2BC0E4, #101f5c);  !important;    
    color: #000000 !important;                 
    border-radius: 8px !important;
    border: 1px solid #cccccc !important;
}
            
/* Drop-down arrow */
div[data-baseweb="select"] svg {
    color: #000000 !important;                 
}
            
/* Sidebar gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #2BC0E4, #101f5c);  !important; 
    background-attachment: fixed !important;
}

/*  Number Input */   
div[data-testid="stNumberInput"] input {
    background: linear-gradient(135deg, #2BC0E4, #101f5c);  !important;    
    color: #000000 !important;                
    border: 1px solid #cccccc !important;     
    border-radius: 8px !important;             
    padding: 8px !important;                 
}
            
/* Label styling */
div[data-testid="stNumberInput"] label {
    color: #ffffff !important;                
    font-weight: 500 !important;
}

 /*  Text Input */                     
div[data-testid="stTextInput"] input {
    background: linear-gradient(135deg, #2BC0E4, #101f5c);  !important;     
    color: #000000 !important;                
    border: 1px solid #cccccc !important;  
    border-radius: 8px !important;             
    padding: 8px !important;                  
}

/* Label styling */
div[data-testid="stTextInput"] label {
    color: #ffffff !important;                 
    font-weight: 500 !important;
}

/* Buttons */          
div.stButton > button {
    background: linear-gradient(135deg, #91246b, #1a2bab) !important; 
    color: white !important;                                          
    border: none !important;                                         
    padding: 10px 18px !important;                                     
    border-radius: 10px !important;                                    
    font-size: 16px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: 0.2s ease-in-out !important;                          
}

/* Hover effect */
div.stButton > button:hover {
    background: linear-gradient(135deg, #2BC0E4, #101f5c);  !important; 
    transform: translateY(-2px) !important;                           
}

/* Active (click) effect */
div.stButton > button:active {
    transform: translateY(0px) !important;
    background: linear-gradient(135deg, #199eab, #147d88) !important;
}

/* Chat box place holder */
textarea::placeholder {
    color: #000000 !important;  
    opacity: 0.7;                    
    font-size: 15px !important;
    font-family: 'Segoe UI', sans-serif !important;
}

textarea {
    background: linear-gradient(135deg, #2BC0E4, #101f5c);  !important; 
    color: #000000 !important;
    border: 2px solid #4be1ec !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-size: 16px !important;
    font-family: 'Segoe UI', sans-serif !important;
    transition: 0.2s ease-in-out !important;
}

textarea:focus {
    border-color: #2ab5c4 !important;
    box-shadow: 0 0 8px rgba(75, 225, 236, 0.4) !important;
}

/* Header / toolbar */
header[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background: transparent !important;
}
            
/* Number input */
[data-testid="stNumberInput"] button {
    background: linear-gradient(135deg, #91246b, #1a2bab) !important;  
    color: #000000 !important;                 
    border-radius: 6px !important;          
    padding: 4px 8px !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: #e6e6e6 !important;   
}

</style>
""", unsafe_allow_html=True)


# Top-left Logo
with open("App/assets/logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

# Styling top Logo
st.markdown("""
<style>

.top-left-brand {
    position: fixed;
    top: 70px;
    left: 30px;
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 9999;
}

.top-left-brand img {
    width: 100px;
    border-radius: 8px;
}

.brand-title {
    font-size: 25px;
    font-weight: 700;
    color: #4be1ec;
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# Render Logo 
st.markdown(f"""
<div class="top-left-brand">
    <img src="data:image/png;base64,{logo_b64}">
    <div>
        <div class="brand-title">BizBuddy AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Robot 
robot_path = "App/assets/robot.png"   

# Convert robot image to Base64
with open(robot_path, "rb") as f:
    robot_data = f.read()
robot_b64 = base64.b64encode(robot_data).decode()

# Hero Layout Styling
st.markdown("""
<style>

.main-block {
    # background: linear-gradient(180deg, #000000, #0d1b2a);
    background: transparent;
    padding: 40px 20px;
    border-radius: 25px;
    text-align: center;
    margin-top: -20px;
    margin-bottom: 30px;
}

.main-title {
    font-size: 38px;
    color: #4be1ec;
    font-weight: 700;
    margin-top: 15px;
}

.main-subtitle {
    font-size: 22px;
    color: #cc4444;
    font-weight: 500;
    margin-bottom: 10px;
}

.main-description {
    font-size: 15px;
    color: #d8e3e7;
    padding: 0 12px;
}

.hero-robot {
    width: 240px;
    margin-bottom: -5px;
    animation: floatRobot 3s ease-in-out infinite;
}

@keyframes floatRobot {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

</style>
""", unsafe_allow_html=True)

# Render robot image 
with open("App/assets/robot.png", "rb") as img_file:
    encoded = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
<div class="main-block">
<img src="data:image/png;base64,{encoded}" class="hero-robot">

<div class="main-title">BizBuddy AI</div>
<div class="main-subtitle">Your Business Growth Partner</div>

<p class="main-description">
"From Beginner to Business Owner — One Mentor Away."
</p>
</div>
""", unsafe_allow_html=True)

# UI Styling
st.markdown("""
    <style>
    div[data-baseweb="select"] * {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True) 

st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .prediction-card {
        border:1px solid #B3001B; 
        padding:15px; 
        border-radius:10px; 
        background: #b17ed6;
        margin-bottom:15px;
    }
    </style>
""", unsafe_allow_html=True)


# Project root path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Import utility functions
from utils.predict import prepare_input, predict_profit, predict_failure, predict_business_idea  

# Model & dataset paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
profit_model_path = os.path.join(BASE_DIR, "Models_Files", "profit_model.pkl")
failure_model_path = os.path.join(BASE_DIR, "Models_Files", "failure_model.pkl")
encoder_path = os.path.join(BASE_DIR, "Models_Files", "encoder.pkl")
DATA_PATH = os.path.join(BASE_DIR, "Dataset_Generation", "micro_business_dataset_500.csv")

# Load dataset & models
df = pd.read_csv(os.path.abspath(DATA_PATH))
profit_model = joblib.load(os.path.abspath(profit_model_path))
failure_model = joblib.load(os.path.abspath(failure_model_path))
encoder = joblib.load(os.path.abspath(encoder_path))

# Language selection (Main page, top-right corner)
with st.container():
    col1, col2 = st.columns([6, 1]) 
    col1.empty()
    with col2:
        language = st.selectbox("", ["English", "Urdu"], key="language_selector")

# Translation dictionary
labels = {
    "English": {
        "instructions": "Enter details to predict monthly profit and failure risk for your micro-business.",
        "city": "City",
        "business": "Business Type",
        "product": "Product / Service",
        "marketing": "Marketing Channel",
        "startup_cost": "Startup Cost (PKR)",
        "cost_per_unit": "Cost per Unit (PKR)",
        "price_per_unit": "Price per Unit (PKR)",
        "predict": "Predict",
        "suggest_idea": "Suggest Business Ideas",
        "profit": "Estimated Monthly Profit",
        "failure": "Failure Risk Probability",
        "ideas": "Suggested Business Ideas",
        "no_ideas": "No suitable business ideas found."
    },
    "Urdu": {
        "instructions": "اپنے مائیکرو کاروبار کے ماہانہ منافع اور ناکامی کے خطرے کی پیش گوئی کے لیے تفصیلات درج کریں۔",
        "city": "شہر",
        "business": "کاروبار کی قسم",
        "product": "مصنوع / سروس",
        "marketing": "مارکیٹنگ چینل",
        "startup_cost": "آغاز لاگت (PKR)",
        "cost_per_unit": "فی یونٹ لاگت (PKR)",
        "price_per_unit": "فی یونٹ قیمت (PKR)",
        "predict": "پیش گوئی کریں",
        "suggest_idea": "کاروباری آئیڈیاز تجویز کریں",
        "profit": "تخمینی ماہانہ منافع",
        "failure": "ناکامی کے خطرے کا امکان",
        "ideas": "تجویز کردہ کاروباری آئیڈیاز",
        "no_ideas": "کوئی مناسب کاروباری آئیڈیاز نہیں ملے۔"
    }
}

lang = labels[language]
st.write(lang["instructions"])

# User Inputs
city = st.selectbox(lang["city"], df['City'].unique())
business = st.selectbox(lang["business"], df['Business'].unique())
product = st.selectbox(lang["product"], df['Product/Service'].unique())
marketing_channel = st.selectbox(lang["marketing"], df['Marketing_Channel'].unique())
startup_cost = st.number_input(lang["startup_cost"], min_value=0)
cost_per_unit = st.number_input(lang["cost_per_unit"], min_value=0)
price_per_unit = st.number_input(lang["price_per_unit"], min_value=0)
interest = st.text_input("Your Interest / Business Focus", "")

sample = {
    "Business": business,
    "City": city,
    "Product/Service": product,
    "Marketing_Channel": marketing_channel,
    "Startup_Cost_PKR": startup_cost,
    "Cost_per_Unit": cost_per_unit,
    "Price_per_Unit": price_per_unit
}

# Suggest Business Ideas button 
if st.button(lang["suggest_idea"]):
    suggested_ideas = predict_business_idea(startup_cost, city)

    st.markdown(f"<h3 style='color:#4CAF50;'>💡 {lang['ideas']}</h3>", unsafe_allow_html=True)

    if not suggested_ideas:
        st.write(lang["no_ideas"])
    else:
        for idea in suggested_ideas:
            st.markdown("""
                <div style="
                    background-color:#006992; 
                    padding:5px; 
                    margin-bottom:12px; 
                    border-radius:10px; 
                    border-left-right:5px solid #4CAF50;
                ">
            """, unsafe_allow_html=True)

            if isinstance(idea, dict):
                st.markdown(f"""
                    <b>📌 Business:</b> {idea['Business']}<br>
                    <b>💰 Avg Startup:</b> {int(idea['Avg_Startup'])} PKR<br>
                    <b>📈 Estimated Monthly Profit:</b> {int(idea['Est_Monthly_Profit'])} PKR<br>
                    <b>⚠️ Avg Failure Risk:</b> {int(idea['Avg_Failure_Risk'] * 100)}%
                """, unsafe_allow_html=True)
            else:
                st.write(idea)

            st.markdown("</div>", unsafe_allow_html=True)

# Predict button
if st.button(lang["predict"]):
    profit = predict_profit(sample, profit_model, encoder)
    failure = predict_failure(sample, failure_model, encoder)
    failure_percentage = int(round(failure * 100, 0))

    # Display results in a styled card
    st.markdown(f"""
    <div class='prediction-card'>
        💰 <b>{lang['profit']}:</b> {int(round(profit, 0))} PKR<br><br>
        ⚠️ <b>{lang['failure']}:</b> {failure_percentage}%
    </div>
    """, unsafe_allow_html=True)

# AI Micro-Entrepreneur Advice Chat Box
st.markdown("### 💬 Ask BizBuddy AI Anything About Your Business")

# Chat input field
user_query = st.text_area(
    "Type your question here(Enter with a question mark(?) please):",
    placeholder="e.g., How can I improve sales for my clothing business?"
)

if st.button("Ask AI"):
    if user_query.strip() == "":
        st.warning("Please enter a question for the AI.")
    else:
        # Show loading spinner while generating response
        with st.spinner("🤖 Generating AI advice ... .It might take some minutes. Kindly wait!"):
            ai_response = generate_business_advice(
                city,
                startup_cost,
                interest=user_query
            )

        # Display response
        st.markdown("### 🤖 BizBuddy AI Response")
        st.write(ai_response)
