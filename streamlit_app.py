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
    .reportview-container .main .block-container{padding-top: 2rem;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🍳 The Calm Cook")
st.markdown("I am your friendly kitchen companion. Tell me what fresh food you have, and I'll combine it with your pantry staples to make something good.")

# --- SIDEBAR: SETTINGS & KNOWLEDGE BASE ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Google API Key", type="password")
    
    st.divider()
    
    st.header("🏠 Your Knowledge Base")
    st.info("I assume you always have these at home. Edit them if you run out!")
    
    # Pre-filled with common items (You can change this list!)
    default_pantry = """Salt, Black Pepper, Olive Oil, Vegetable Oil, Butter
Plain Flour, Sugar, Honey, Soy Sauce
Dried Thyme, Dried Rosemary, Paprika, Cumin
Garlic, Onions, Stock Cubes (Chicken/Beef)
Rice, Pasta, Potatoes"""
    
    pantry_items = st.text_area("My Pantry Staples:", value=default_pantry, height=200)

# --- MAIN INPUTS ---
col1, col2 = st.columns([2, 1])

with col1:
    fresh_ingredients = st.text_area("🥩 What fresh ingredients do you have today?", height=100, 
                             placeholder="e.g., Topside beef joint, some carrots that need using up...")

with col2:
    energy_level = st.radio("🔋 Energy Level:", ["I'm okay", "I'm tired / stressed"])
    serving_size = st.selectbox("👥 Cooking for:", ["1 Person", "2 People", "4 People", "Batch Cooking"])

# --- SYSTEM PROMPT (The Personality) ---
system_prompt = """
You are a friendly, supportive, and non-judgmental home cooking companion.
Your goal is to give the user confidence.

RULES FOR TONE:
- Be warm and encouraging (like a kind friend, not a strict professor).
- NO condescending phrases like "Chef's Tip" or "It's simple."
- NO jargon. Don't say "sear," say "brown the meat." Don't say "julienne," say "cut into thin strips."
- Focus on SENSORY CHECKS: Describe what things should smell like, sound like, or look like.

RECIPE STRUCTURE:
1. THE WELCOME: A reassuring sentence about the dish.
2. EQUIPMENT LIST: Bullet points of what pots/pans are needed.
3. INGREDIENTS LIST: combine the user's FRESH ingredients with their PANTRY staples. Give estimated quantities based on the serving size.
4. THE METHOD: Numbered steps.
   - For every step involving heat or cutting, add a "Safety/Confidence Note" (e.g., "It might smoke a little, that's normal.")
5. SERVING: How to plate it up simply.

IMPORTANT: If the user is TIRED, choose the simplest possible method (one pot if possible) and skip fancy garnishes.
"""

# --- THE ACTION ---
if st.button("Plan My Meal"):
    if not api_key:
        st.warning("Please enter your API Key in the sidebar.")
    elif not fresh_ingredients:
        st.warning("Please tell me what fresh food you have.")
    else:
        with st.spinner("Looking through your pantry and planning a calm meal..."):
            try:
                genai.configure(api_key=api_key)
                
                # Smart Model Selector (The fix we made earlier)
                valid_model_name = "gemini-pro" # Fallback
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            valid_model_name = m.name
                            break
                except:
                    pass

                # Build the Prompt
                full_prompt = f"""
                USER SITUATION:
                Fresh Ingredients: {fresh_ingredients}
                Pantry Staples Available: {pantry_items}
                Energy Level: {energy_level}
                Serving Size: {serving_size}
                
                Please create a recipe using these ingredients.
                """

                # Generate
                model = genai.GenerativeModel(valid_model_name, system_instruction=system_prompt)
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                st.success("You've got this. Take it one step at a time.")
                
            except Exception as e:
                st.error("Something went wrong. Please check your API Key.")
                st.error(e)
