import streamlit as st
import google.generativeai as genai

st.title("👨‍⚕️ The Doctor is In")

# 1. Check the Library Version
try:
    version = genai.__version__
    st.write(f"Library Version: {version}")
except:
    st.write("Library Version: Unknown (Very Old)")

# 2. Key Input
api_key = st.text_input("Enter Key", type="default") # Shows the text so you can check it!

if st.button("Test Connection"):
    if not api_key:
        st.error("No key entered")
    else:
        try:
            # Setup
            genai.configure(api_key=api_key)
            
            # Simple Test - No System Instructions (which break old versions)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content("Say Hello")
            
            st.success("✅ IT WORKED!")
            st.write(response.text)
            
        except Exception as e:
            st.error("❌ IT FAILED.")
            st.write("Here is the exact error:")
            st.code(e) # This will print the technical reason
