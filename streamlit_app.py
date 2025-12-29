import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
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
st.markdown("Enter what ingredients you have. I'll handle the rest.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google API Key", type="password")

# --- INPUTS ---
ingredients = st.text_area("What is in your fridge?", height=100, 
                         placeholder="e.g., Pasta, tomatoes. I am tired.")
energy_level = st.radio("Energy Level:", ["I have some energy", "I am tired / stressed"])

# --- SYSTEM PROMPT ---
system_prompt = """
You are a calm, supportive cooking companion. 
TONE: Gentle, encouraging, slow. ZERO JARGON.
STRUCTURE:
1. Reassurance
2. Prep Steps
3. Ingredients List
4. Method (Step-by-step with sensory checks)
5. Panic Button (Troubleshooting)
"""

# --- THE SMART ACTION ---
if st.button("Find a Recipe"):
    if not api_key:
        st.warning("Please enter your API Key.")
    elif not ingredients:
        st.warning("Please tell me what ingredients you have.")
    else:
        with st.spinner("Finding the right brain..."):
            try:
                genai.configure(api_key=api_key)
                
                # --- AUTO-DISCOVERY MAGIC ---
                # We ask Google: "What models do I have?"
                valid_model_name = ""
                
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            # We found a valid text model! Use it.
                            valid_model_name = m.name
                            break
                except:
                    # If listing fails, fallback to the safest old faithful
                    valid_model_name = "gemini-pro"

                # If we still have nothing, try 'gemini-pro'
                if not valid_model_name:
                    valid_model_name = "gemini-pro"

                # --- GENERATE RECIPE ---
                model = genai.GenerativeModel(valid_model_name, system_instruction=system_prompt)
                full_prompt = f"Ingredients: {ingredients}. Energy: {energy_level}"
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                st.success(f"Cooked using: {valid_model_name}")
                st.balloons()
                
            except Exception as e:
                st.error("Something went wrong.")
                st.write("Technical details:", e)
