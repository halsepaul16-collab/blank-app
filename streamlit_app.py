import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="The Calm Cook", page_icon="🍳", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 16px;}
    .stButton button {background-color: #2E86C1; color: white; border-radius: 10px; padding: 10px 24px;}
    h1 {color: #2E4053;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🍳 The Calm Cook")
st.markdown("I am your friendly kitchen companion. Tell me what fresh food you have, and I'll combine it with your pantry staples.")

# --- SIDEBAR: KNOWLEDGE BASE ---
with st.sidebar:
    st.header("🏠 Your Knowledge Base")
    st.info("I assume you always have these.")
    
    default_pantry = """Salt, Black Pepper, Olive Oil, Vegetable Oil, Butter
Plain Flour, Sugar, Honey, Soy Sauce
Dried Thyme, Dried Rosemary, Paprika, Cumin
Garlic, Onions, Stock Cubes
Rice, Pasta, Potatoes"""
    
    pantry_items = st.text_area("My Staples:", value=default_pantry, height=200)

    # --- API KEY LOGIC (CRASH PROOF VERSION) ---
    # We use .get() so it doesn't crash if the key is missing
    api_key = st.secrets.get("GOOGLE_API_KEY")

    if api_key:
        st.success("Connected to Kitchen Brain")
    else:
        st.error("⚠️ The API Key is missing from Secrets.")
        st.info("Please tell Paul to add the key in the App Settings.")

# --- MAIN INPUTS ---
col1, col2 = st.columns([2, 1])

with col1:
    fresh_ingredients = st.text_area("🥩 What fresh ingredients do you have?", height=100, 
                             placeholder="e.g., Beef joint, carrots...")

with col2:
    energy_level = st.radio("🔋 Energy:", ["I'm okay", "I'm tired / stressed"])
    serving_size = st.selectbox("👥 Cooking for:", ["1 Person", "2 People", "4 People"])

# --- SYSTEM PROMPT ---
system_prompt = """
You are a friendly, supportive cooking companion.
TONE: Warm, encouraging. NO condescension. NO jargon.
STRUCTURE:
1. WELCOME: Reassuring sentence.
2. EQUIPMENT: Bullet points.
3. INGREDIENTS: Combine FRESH + PANTRY staples. Quantities based on serving size.
4. METHOD: Step-by-step with sensory checks.
5. SERVING: Simple plating.
If TIRED: Keep it simple.
"""

# --- THE ACTION ---
if st.button("Plan My Meal"):
    if not api_key:
        st.warning("I cannot cook without the API Key.")
    elif not fresh_ingredients:
        st.warning("Please enter fresh ingredients.")
    else:
        with st.spinner("Planning your meal..."):
            try:
                genai.configure(api_key=api_key)
                
                # Auto-find the right brain
                valid_model_name = "gemini-pro"
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            valid_model_name = m.name
                            break
                except:
                    pass

                # The Recipe Request
                full_prompt = f"""
                Fresh Ingredients: {fresh_ingredients}
                Pantry Staples: {pantry_items}
                Energy Level: {energy_level}
                Serving Size: {serving_size}
                
                Please create a recipe using these ingredients.
                """
                
                model = genai.GenerativeModel(valid_model_name, system_instruction=system_prompt)
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                st.balloons()
                
            except Exception as e:
                st.error("Something went wrong.")
                st.write(e)
