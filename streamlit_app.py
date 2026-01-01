import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Chef Paul's Kitchen", page_icon="👨‍🍳", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 16px;}
    .stButton button {background-color: #2E4053; color: white; border-radius: 10px; padding: 10px 24px;}
    h1 {color: #800000;} 
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("👨‍🍳 Chef Paul's Kitchen")
st.markdown("""
**"I have spent a lifetime learning these secrets so you don't have to struggle."**  
Tell me what ingredients you have, and I will show you how to turn them into something special.
""")

# --- SIDEBAR: KNOWLEDGE BASE ---
with st.sidebar:
    st.header("🏠 Your Pantry Staples")
    st.info("I know you always have these in stock:")
    
    default_pantry = """Salt, Black Pepper, Olive Oil, Vegetable Oil, Butter
Plain Flour, Sugar, Honey, Soy Sauce
Dried Thyme, Dried Rosemary, Paprika, Cumin
Garlic, Onions, Stock Cubes
Rice, Pasta, Potatoes"""
    
    pantry_items = st.text_area("Edit Pantry List:", value=default_pantry, height=200)

    # --- API KEY LOGIC ---
    st.divider()
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        st.success("Secret Key Loaded 🟢")
    else:
        st.error("⚠️ Key Missing")
        st.info("Paul: Please add the API Key to the 'Secrets' settings to unlock the kitchen.")

# --- MAIN INPUTS ---
col1, col2 = st.columns([2, 1])

with col1:
    fresh_ingredients = st.text_area("🥩 What fresh ingredients do we have today?", height=100, 
                             placeholder="e.g., Topside beef, some sad looking carrots...")

with col2:
    energy_level = st.radio("🔋 How are you feeling?", ["I have energy to cook", "I'm tired / stressed"])
    serving_size = st.selectbox("👥 Cooking for:", ["1 Person", "2 People", "4 People", "Family Batch"])

# --- SYSTEM PROMPT (THE PERSONA) ---
system_prompt = """
You are "Chef Paul", a world-renowned chef famous for two things: 
1. Your incredible culinary knowledge.
2. Your kindness and willingness to share your "Chef's Secrets" with home cooks.

YOUR GOAL:
Take the user's humble ingredients and treat them with respect. Turn them into a proper dish.

YOUR TONE:
- Authoritative but Kind. Use phrases like "Here is my secret..." or "Most people do X, but I want you to do Y..."
- NO JARGON without explanation. If you use a chef term, explain it simply.
- If the user is TIRED: Be gentle. "Let's take the easy road today."

OUTPUT STRUCTURE:
1. THE DISH NAME: Create a appetizing, restaurant-style name for the dish. (e.g., "Chef Paul's Sunday Roast with Honey-Glazed Carrots").
2. THE INTRODUCTION: A warm welcome from Chef Paul explaining WHY this combination works.
3. THE SECRET: Share one specific "Chef's Secret" relevant to this dish (e.g., "The secret to crispy potatoes is shaking the colander...").
4. INGREDIENTS LIST: Combine Fresh + Pantry.
5. THE METHOD: Numbered steps. Focus on SENSORY details (Smell, Sound, Look).
6. SERVING: How to present it.
"""

# --- THE ACTION ---
if st.button("Ask Chef Paul"):
    if not api_key:
        st.warning("I cannot cook without the API Key.")
    elif not fresh_ingredients:
        st.warning("Please give me some ingredients to work with.")
    else:
        with st.spinner("Chef Paul is reviewing your ingredients..."):
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
                
                Please create a recipe as Chef Paul.
                """
                
                model = genai.GenerativeModel(valid_model_name, system_instruction=system_prompt)
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error("Something went wrong.")
                st.write(e)
