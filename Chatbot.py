import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="PCOS Support Chatbot", page_icon="🤖")
st.title("💬 PCOS Information Chatbot")
st.caption("I'm here to help you with questions you may have  about Polycystic Ovary Syndrome (PCOS).")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# PCOS-related resources
pcos_resources = {
    "Mayo Clinic": "https://www.mayoclinic.org/diseases-conditions/pcos/symptoms-causes/syc-20353439",
    "PCOS Awareness Association": "https://www.pcosaa.org/",
    "NHS UK": "https://www.nhs.uk/conditions/polycystic-ovary-syndrome-pcos/",
    "PDF Guide": "https://cdn2.hubspot.net/hubfs/494075/PCOS%20Patient%20Handout.pdf",
    "PCOS Challenge Support": "https://pcoschallenge.org/"
}

# Check if input is related to PCOS
def is_pcos_related(text):
    keywords = ["pcos", "polycystic", "ovary", "syndrome", "menstrual", "hormone", "androgen", "fertility", "insulin"]
    return any(word in text.lower() for word in keywords)

# Display previous conversation
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a question about PCOS...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.history.append({"role": "user", "content": user_input})

    if is_pcos_related(user_input):

        gemini_response = model.generate_content(user_input)
        reply = gemini_response.text

        reply += "\n\n---\n**📚 Helpful PCOS Resources:**\n"
        for name, url in pcos_resources.items():
            reply += f"- [{name}]({url})\n"
    else:
        reply = "🙂 I can only help with PCOS-related topics. Please ask something related to Polycystic Ovary Syndrome."

    st.chat_message("assistant").markdown(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})

