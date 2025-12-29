import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Calm Cook", page_icon="🍳")

# --- STYLE ---
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 16px;}
    .stButton button {background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 24px;}
    h1 {color: #2E4053;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🍳 The Calm Cook")
st.markdown("Enter what ingredients you have. I will find a way to make it work.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google API Key", type="password")

# --- INPUTS ---
ingredients = st.text_area("What is in your fridge?", height=100, 
                         placeholder="e.g., Pasta, tomatoes. I am tired.")
energy_level = st.radio("Energy Level:", ["I have some energy", "I am tired / stressed"])

# --- THE SYSTEM PROMPT ---
system_prompt = """
You are a calm, supportive cooking companion. 
TONE: Gentle, encouraging, slow. ZERO JARGON.
STRUCTURE:
1. Reassurance
2. Prep Steps (Mise-en-place)
3. Ingredients List
4. Method (Step-by-step with sensory checks)
5. Panic Button (Troubleshooting)
"""

# --- THE SMART ACTION ---
if st.button("Find a Recipe"):
    if not api_key:
        st.warning("Please enter your API Key on the left.")
    elif not ingredients:
        st.warning("Please tell me what ingredients you have.")
    else:
        with st.spinner("Checking the cupboards..."):
            try:
                genai.configure(api_key=api_key)
                
                # LIST OF BRAINS TO TRY (If one fails, it tries the next)
                models_to_try = ["gemini-1.5-flash", "gemini-pro", "models/gemini-1.5-flash"]
                
                response = None
                used_model = ""
                
                # The Loop: Try each brain
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
                        response = model.generate_content(f"Ingredients: {ingredients}. Energy: {energy_level}")
                        used_model = model_name
                        break # It worked! Stop looking.
                    except Exception:
                        continue # Didn't work, try the next one.

                # Did we get an answer?
                if response:
                    st.markdown("---")
                    st.markdown(response.text)
                    st.success("You can do this.")
                else:
                    st.error("I tried 3 different Google brains and none responded. Please check your API Key is correct.")
                    
            except Exception as e:
                st.error(f"Something went wrong: {e}")
