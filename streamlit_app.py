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
st.markdown("Enter what ingredients you have, and I'll help you make a meal step-by-step. No jargon. No stress.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google API Key", type="password")
    st.info("Your key is safe and not saved.")

# --- INPUTS ---
ingredients = st.text_area("What is in your fridge/cupboard?", height=100, 
                         placeholder="e.g., Pasta, a tin of tomatoes, onion. I am exhausted.")
energy_level = st.radio("How are you feeling?", ["I have some energy", "I am tired / stressed"])

# --- THE BRAIN ---
system_prompt = """
You are a calm, supportive cooking companion for someone who is anxious, tired, or cooking out of necessity.
YOUR TONE: Gentle, encouraging, slow. ZERO JARGON.
OUTPUT STRUCTURE:
1. THE REASSURANCE: Validate their ingredients.
2. THE GET READY: List 3-4 prep steps.
3. THE INGREDIENTS: Simple list.
4. THE METHOD: Numbered steps with Action, Sensory Check, and Safety Note.
5. THE PANIC BUTTON: 3 "What if" solutions.
If user is TIRED: Use fewest pans and easiest method.
"""

# --- ACTION ---
if st.button("Find a Recipe"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar on the left.")
    elif not ingredients:
        st.warning("Please tell me what ingredients you have.")
    else:
        with st.spinner("Thinking of a calm recipe..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-pro", system_instruction=system_prompt)
                response = model.generate_content(f"Ingredients: {ingredients}. Energy Level: {energy_level}")
                st.markdown("---")
                st.markdown(response.text)
                st.success("You can do this.")
            except Exception as e:
                st.error(f"Error: {e}")
